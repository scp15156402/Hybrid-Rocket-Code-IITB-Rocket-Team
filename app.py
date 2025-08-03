# app.py

"""
app.py

Enhanced Flask application with complete notebook implementation.
Handles missing/invalid form inputs gracefully and displays errors
in the results panel rather than returning a raw 400.
"""

import os
from flask import Flask, render_template, request, send_file
from flask_caching import Cache
from werkzeug.exceptions import BadRequestKeyError

# Absolute imports of your modules
from hybrid_rocket.solver import simulate_burn
from hybrid_rocket.export import print_summary, compute_structural_metrics
from hybrid_rocket.slider_config import slider_config, dropdown_config
from hybrid_rocket.plots import init_plot_cache, save_all_plots, get_cached_image

app = Flask(__name__)
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300  # 5 minutes
cache = Cache(app)
init_plot_cache(app)


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

            # 2) Read & validate all slider inputs
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

            # 5) Generate textual summary
            summary = print_summary(results, current_values)

            # 6) Generate all plots
            plot_keys = save_all_plots(results, current_values)

            # 7) Append any safety warnings
            warnings = []
            # Chamber pressure >40 bar?
            if results.get("p_c") is not None and len(results["p_c"]) > 0:
                if max(results["p_c"]) > 40e5:
                    warnings.append("*** WARNING: Peak chamber pressure exceeds 40 bar! ***")
            # Low‐pressure warning flag
            if results.get("low_pressure_warning"):
                warnings.append("*** WARNING: Chamber pressure dropped below 2 bar.***")

            # Structural checks
            try:
                struct = compute_structural_metrics(current_values, results)
                if results.get("p_c") and max(results["p_c"]) > struct["max_pressure_design_casing"]:
                    warnings.append("*** WARNING: Chamber pressure exceeds casing design pressure! ***")
                if struct["n2o_vapor_pressure"] > struct["max_pressure_design_ox_tank"]:
                    warnings.append("*** WARNING: N₂O vapor pressure exceeds tank design pressure! ***")
            except Exception as e:
                warnings.append(f"*** WARNING: Structural check failed: {e} ***")

            if warnings:
                summary += "\n\n--- SAFETY WARNINGS ---\n" + "\n".join(warnings)

        except Exception as e:
            # Any missing/invalid input or simulation error ends up here
            summary = f"Error: {e}\n\nPlease check your input parameters and try again."
            plot_keys = []

    return render_template(
        "index.html",
        slider_config=slider_config,
        dropdown_config=dropdown_config,
        current_values=current_values,
        summary=summary,
        plot_keys=plot_keys,
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
      <li>Use the command line version: <code>python -m hybrid_rocket.main --export</code></li>
      <li>Check the generated CSV file in your working directory</li>
    </ol>
    <a href='/'>← Back to Simulator</a>
    """


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)
