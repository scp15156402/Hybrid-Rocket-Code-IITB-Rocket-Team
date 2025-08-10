# rocket_simulations/hybrid_rocket/routes.py

from flask import Blueprint, render_template, request, current_app
from rocket_simulations.hybrid_rocket.slider_config import slider_config, dropdown_config
from rocket_simulations.hybrid_rocket.logic.solver import simulate_burn
from rocket_simulations.hybrid_rocket.logic.export import get_summary_dict, compute_structural_metrics
from rocket_simulations.hybrid_rocket.logic.plots import save_all_plots, get_cached_image

bp = Blueprint(
    "hybrid",  # Blueprint name (used in url_for)
    __name__,
    template_folder="templates",
    static_folder="static",
)

# Define rocket-specific tabs and their parameters here for dynamic UI rendering
rocket_tabs = {
    'tab1': {'label': "Combustion", 'fields': ["r1", "r2", "L", "mdot_ox", "rho_fuel"]},
    'tab2': {'label': "Casing", 'fields': ["safety_factor", "insul_grain_thk", "insul_prepost_thk", "casing_wall_thk", "pre_comb_len", "post_comb_len"]},
    'tab3': {'label': "Nozzle", 'fields': ["converge_half_angle", "throat_diameter", "throat_length", "diverge_half_angle"]},
    'tab4': {'label': "Retainer", 'fields': ["retainer_length", "retainer_inner_radius", "frontcap_length"]},
    'tab5': {'label': "Bolts", 'fields': ["frontcap_bolt_diameter", "frontcap_num_bolts", "nozzle_bolt_diameter", "nozzle_num_bolts", "ox_tank_bolt_diameter", "ox_tank_num_bolts"]},
    'tab6': {'label': "Tank", 'fields': ["ox_tank_safety_factor", "ox_tank_outer_diameter", "ox_tank_wall_thk", "ox_tank_length", "ox_tank_temp", "ox_tank_frontcap_thk", "ox_tank_backcap_thk", "motor_ox_gap"]},
    'tab7': {'label': "Materials", 'fields': list(dropdown_config.keys())}
}


@bp.route("/", methods=["GET", "POST"])
def index():
    """
    Main UI page for the Hybrid rocket simulation.
    Handles form input and runs simulation on POST.
    """

    # Initialize with default current values
    current_values = {k: v["default"] for k, v in slider_config.items()}
    current_values.update({k: v["default"] for k, v in dropdown_config.items()})

    summary = None
    plot_keys = []

    if request.method == "POST":
        try:
            # Validate slider inputs (floats)
            for key in slider_config:
                raw_val = request.form.get(key)
                if raw_val is None:
                    raise ValueError(f"Missing input: {key}")
                try:
                    current_values[key] = float(raw_val)
                except ValueError:
                    raise ValueError(f"Invalid numeric value for {key}: {raw_val}")

            # Validate dropdown selections (strings)
            for key in dropdown_config:
                sel_val = request.form.get(key)
                if sel_val is None:
                    raise ValueError(f"Missing selection: {key}")
                current_values[key] = sel_val

            # Run the hybrid rocket simulation
            results = simulate_burn(
                r1=current_values["r1"],
                r2=current_values["r2"],
                L=current_values["L"],
                mdot_ox=current_values["mdot_ox"],
                rho_fuel=current_values["rho_fuel"],
                current_values=current_values,
            )

            # Generate summary and plots
            summary = get_summary_dict(results, current_values)
            plot_keys = save_all_plots(results, current_values)

        except Exception as e:
            summary = {
                "Error": {
                    "Message": str(e),
                    "Advice": "Please check your input parameters and try again.",
                }
            }
            plot_keys = []

    return render_template(
        "hybrid_index.html",
        rocket_tabs=rocket_tabs,
        slider_config=slider_config,
        dropdown_config=dropdown_config,
        current_values=current_values,
        summary=summary,
        plot_keys=plot_keys,
        plot_route="hybrid.serve_plot",  # Explicit blueprint plot route for url_for in templates
    )


@bp.route("/plot/<key>")
def serve_plot(key):
    """
    Serves cached plot images by key.
    """
    buf = get_cached_image(key)
    if buf is None:
        return "Plot not found", 404
    buf.seek(0)
    return current_app.response_class(buf, mimetype="image/png")

# Additional API routes can be defined here as needed
