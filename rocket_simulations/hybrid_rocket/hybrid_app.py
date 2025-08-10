import os
import numpy as np
from flask import Blueprint, Flask, render_template, request, send_file
from flask_caching import Cache

from rocket_simulations.hybrid_rocket.logic.solver import simulate_burn
from rocket_simulations.hybrid_rocket.logic.export import get_summary_dict, compute_structural_metrics
from rocket_simulations.hybrid_rocket.data.slider_config import slider_config, dropdown_config
from rocket_simulations.hybrid_rocket.logic.plots import init_plot_cache, save_all_plots, get_cached_image

# Create the blueprint
hybrid_bp = Blueprint(
    "hybrid",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/hybrid_simulations/static"
)


# Cache variable will be set in create_app
cache = None

# Define rocket-specific tabs for UI rendering
rocket_tabs = {
    'tab1': {'label': "Combustion", 'fields': ["r1", "r2", "L", "mdot_ox", "rho_fuel"]},
    'tab2': {'label': "Casing", 'fields': ["safety_factor", "insul_grain_thk", "insul_prepost_thk", "casing_wall_thk", "pre_comb_len", "post_comb_len"]},
    'tab3': {'label': "Nozzle", 'fields': ["converge_half_angle", "throat_diameter", "throat_length", "diverge_half_angle"]},
    'tab4': {'label': "Retainer", 'fields': ["retainer_length", "retainer_inner_radius", "frontcap_length"]},
    'tab5': {'label': "Bolts", 'fields': ["frontcap_bolt_diameter", "frontcap_num_bolts", "nozzle_bolt_diameter", "nozzle_num_bolts", "ox_tank_bolt_diameter", "ox_tank_num_bolts"]},
    'tab6': {'label': "Tank", 'fields': ["ox_tank_safety_factor", "ox_tank_outer_diameter", "ox_tank_wall_thk", "ox_tank_length", "ox_tank_temp", "ox_tank_frontcap_thk", "ox_tank_backcap_thk", "motor_ox_gap"]},
    'tab7': {'label': "Materials", 'fields': list(dropdown_config.keys())}
}


@hybrid_bp.route("/", methods=["GET", "POST"])
def index():
    # Initialize defaults
    current_values = {k: v["default"] for k, v in slider_config.items()}
    current_values.update({k: v["default"] for k, v in dropdown_config.items()})
    summary = None
    plot_keys = []

    if request.method == "POST":
        try:
            cache.clear()

            # Validate sliders
            for key in slider_config:
                raw = request.form.get(key)
                if raw is None:
                    raise ValueError(f"Missing input: {key}")
                try:
                    current_values[key] = float(raw)
                except ValueError:
                    raise ValueError(f"Invalid numeric value for {key}: {raw}")

            # Validate dropdowns
            for key in dropdown_config:
                sel = request.form.get(key)
                if sel is None:
                    raise ValueError(f"Missing selection: {key}")
                current_values[key] = sel

            # Run simulation
            results = simulate_burn(
                r1=current_values["r1"],
                r2=current_values["r2"],
                L=current_values["L"],
                mdot_ox=current_values["mdot_ox"],
                rho_fuel=current_values["rho_fuel"],
                current_values=current_values,
            )

            # Generate summary
            summary = get_summary_dict(results, current_values)

            # Generate plots
            plot_keys = save_all_plots(results, current_values)

            # Build safety warnings
            warnings = []
            p_c = results.get("p_c", [])
            low_warn = results.get("low_pressure_warning", False)
            if isinstance(p_c, (list, tuple, np.ndarray)) and len(p_c) > 0:
                if max(p_c) > 40e5:
                    warnings.append("Peak chamber pressure exceeds 40 bar")
            if low_warn:
                warnings.append("Chamber pressure dropped below 2 bar")

            try:
                struct = compute_structural_metrics(current_values, results)
                if len(p_c) > 0 and max(p_c) > struct["max_pressure_design_casing"]:
                    warnings.append("Chamber pressure exceeds casing design pressure")
                if struct["n2o_vapor_pressure"] > struct["max_pressure_design_ox_tank"]:
                    warnings.append("N₂O vapor pressure exceeds tank design pressure")
            except Exception as e:
                warnings.append(f"Structural check failed: {e}")

            if warnings:
                summary["Safety Warnings"] = {
                    f"Warning {i+1}": msg for i, msg in enumerate(warnings)
                }

        except Exception as e:
            summary = {
                "Error": {
                    "Message": str(e),
                    "Advice": "Please check your input parameters and try again."
                }
            }
            plot_keys = []

    return render_template(
        "simulations/hybrid_index.html",
        rocket_tabs=rocket_tabs,
        slider_config=slider_config,
        dropdown_config=dropdown_config,
        current_values=current_values,
        summary=summary,
        plot_keys=plot_keys,
        plot_route="hybrid.serve_plot"
    )


@hybrid_bp.route("/plot/<key>")
def serve_plot(key):
    buf = get_cached_image(key)
    if buf is None:
        return "Plot not found", 404
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@hybrid_bp.route("/export")
def export_data():
    return """
    <h2>Data Export</h2>
    <p>To export simulation data:</p>
    <ol>
      <li>Run a simulation using the main interface</li>
      <li>Use the command line version: <code>python -m rocket_simulations.hybrid_rocket.main --export</code></li>
      <li>Check the generated CSV file in your working directory</li>
    </ol>
    <a href='/hybrid/'>← Back to Hybrid Simulator</a>
    """


def create_app():
    global cache
    app = Flask(__name__)
    app.config["CACHE_TYPE"] = "SimpleCache"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300

    cache = Cache(app)
    init_plot_cache(app)

    # Register the hybrid blueprint
    app.register_blueprint(hybrid_bp)

    return app


if __name__ == "__main__":
    create_app().run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)
