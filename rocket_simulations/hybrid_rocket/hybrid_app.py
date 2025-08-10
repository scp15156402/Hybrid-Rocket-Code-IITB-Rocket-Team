# rocket_simulations/hybrid_rocket/hybrid_app.py

"""
hybrid_app.py

Flask application for Hybrid Rocket Simulation.
Handles form input validation, simulation runs,
plot generation, summary creation, and error handling gracefully.
"""

import os
import numpy as np
from flask import Flask, render_template, request, send_file
from flask_caching import Cache

# Updated absolute imports to new package structure
from rocket_simulations.hybrid_rocket.logic.solver import simulate_burn
from rocket_simulations.hybrid_rocket.logic.export import get_summary_dict, compute_structural_metrics
from rocket_simulations.hybrid_rocket.slider_config import slider_config, dropdown_config
from rocket_simulations.hybrid_rocket.logic.plots import init_plot_cache, save_all_plots, get_cached_image


def create_app():
    app = Flask(__name__)
    app.config["CACHE_TYPE"] = "SimpleCache"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300  # 5 minutes

    cache = Cache(app)
    init_plot_cache(app)

    # Define rocket-specific tabs and their parameters for dynamic UI rendering
    rocket_tabs = {
        'tab1': {'label': "Combustion", 'fields': ["r1", "r2", "L", "mdot_ox", "rho_fuel"]},
        'tab2': {'label': "Casing", 'fields': ["safety_factor", "insul_grain_thk", "insul_prepost_thk", "casing_wall_thk", "pre_comb_len", "post_comb_len"]},
        'tab3': {'label': "Nozzle", 'fields': ["converge_half_angle", "throat_diameter", "throat_length", "diverge_half_angle"]},
        'tab4': {'label': "Retainer", 'fields': ["retainer_length", "retainer_inner_radius", "frontcap_length"]},
        'tab5': {'label': "Bolts", 'fields': ["frontcap_bolt_diameter", "frontcap_num_bolts", "nozzle_bolt_diameter", "nozzle_num_bolts", "ox_tank_bolt_diameter", "ox_tank_num_bolts"]},
        'tab6': {'label': "Tank", 'fields': ["ox_tank_safety_factor", "ox_tank_outer_diameter", "ox_tank_wall_thk", "ox_tank_length", "ox_tank_temp", "ox_tank_frontcap_thk", "ox_tank_backcap_thk", "motor_ox_gap"]},
        'tab7': {'label': "Materials", 'fields': list(dropdown_config.keys())}
    }

    @app.route("/", methods=["GET", "POST"])
    def index():
        # 1) Initialize with defaults
        current_values = {k: v["default"] for k, v in slider_config.items()}
        current_values.update({k: v["default"] for k, v in dropdown_config.items()})
        summary = None
        plot_keys = []

        if request.method == "POST":
            try:
                cache.clear()

                # 2) Read & validate all slider inputs (floats)
                for key in slider_config:
                    raw = request.form.get(key)
                    if raw is None:
                        raise ValueError(f"Missing input: {key}")
                    try:
                        current_values[key] = float(raw)
                    except ValueError:
                        raise ValueError(f"Invalid numeric value for {key}: {raw}")

                # 3) Read dropdowns (strings)
                for key in dropdown_config:
                    sel = request.form.get(key)
                    if sel is None:
                        raise ValueError(f"Missing selection: {key}")
                    current_values[key] = sel

                # 4) Run simulation
                results = simulate_burn(
                    r1=current_values["r1"],
                    r2=current_values["r2"],
                    L=current_values["L"],
                    mdot_ox=current_values["mdot_ox"],
                    rho_fuel=current_values["rho_fuel"],
                    current_values=current_values,
                )

                # 5) Generate nested-dict summary
                summary = get_summary_dict(results, current_values)

                # 6) Generate all plots
                plot_keys = save_all_plots(results, current_values)

                # 7) Build safety warnings list and insert into summary dict
                warnings = []

                # Pull out the arrays/lists once
                p_c = results.get("p_c", [])
                low_warn = results.get("low_pressure_warning", False)

                # Chamber pressure > 40 bar?
                if isinstance(p_c, (list, tuple, np.ndarray)) and len(p_c) > 0:
                    if max(p_c) > 40e5:
                        warnings.append("Peak chamber pressure exceeds 40 bar")

                # Low‐pressure warning flag
                if low_warn:
                    warnings.append("Chamber pressure dropped below 2 bar")

                # Structural checks
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
                # Any missing/invalid input or simulation error ends up here
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
            plot_route="hybrid.serve_plot"  # blueprint plot route name for url_for in templates
        )

    @app.route("/plot/<key>")
    def serve_plot(key):
        buf = get_cached_image(key)
        if buf is None:
            return "Plot not found", 404
        buf.seek(0)
        return send_file(buf, mimetype="image/png")

    @app.route("/export")
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

    return app


if __name__ == "__main__":
    create_app().run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)
