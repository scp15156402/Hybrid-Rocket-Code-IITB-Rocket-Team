import os
from flask import Flask, render_template, request, send_file
from flask_caching import Cache

# ✅ Absolute imports
from hybrid_rocket.solver import simulate_burn
from hybrid_rocket.export import print_summary
from hybrid_rocket.slider_config import slider_config, dropdown_config
from hybrid_rocket.plots import init_plot_cache, save_all_plots, get_cached_image

app = Flask(__name__)
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300  # 5 minutes
cache = Cache(app)

# Initialize the in-memory plot cache (and default static plots)
init_plot_cache(app)

@app.route("/", methods=["GET", "POST"])
def index():
    # Start with defaults for all controls
    current_values = {k: v["default"] for k, v in slider_config.items()}
    current_values.update({k: v["default"] for k, v in dropdown_config.items()})

    summary = None
    plot_keys = []

    if request.method == "POST":
        try:
            # Clear old plot buffers
            cache.clear()

            # 1. Read all slider inputs (values are strings, convert to float)
            for key in slider_config:
                current_values[key] = float(request.form[key])

            # 2. Read dropdown selections
            for key in dropdown_config:
                current_values[key] = request.form[key]

            # 3. Run the burn simulation with the submitted values
            results = simulate_burn(
                r1=current_values["r1"],            # cm
                r2=current_values["r2"],            # cm
                L=current_values["L"],              # cm
                mdot_ox=current_values["mdot_ox"],  # g/s
                rho_fuel=current_values["rho_fuel"] # kg/m³
            )

            # 4. Generate textual summary
            summary = print_summary(results)

            # 5. Generate & cache all plots
            plot_keys = save_all_plots(results)

        except Exception as e:
            summary = f"Error: {e}"
            plot_keys = []

    return render_template(
        "index.html",
        slider_config=slider_config,
        dropdown_config=dropdown_config,
        current_values=current_values,
        summary=summary,
        plot_keys=plot_keys
    )

@app.route("/plot/<key>")
def serve_plot(key):
    buf = get_cached_image(key)
    if buf is None:
        return "Plot not found", 404
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

if __name__ == "__main__":
    # Disable the reloader on Windows to avoid socket/thread issues
    app.run(debug=True, use_reloader=False)
