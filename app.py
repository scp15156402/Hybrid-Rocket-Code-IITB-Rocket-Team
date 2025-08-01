import os
from flask import Flask, render_template, request, send_file
from flask_caching import Cache

# ✅ Absolute imports instead of relative
from hybrid_rocket.solver import simulate_burn
from hybrid_rocket.export import print_summary
from hybrid_rocket.slider_config import slider_config, dropdown_config
from hybrid_rocket.plots import init_plot_cache, save_all_plots, get_cached_image

app = Flask(__name__)
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300  # 5 minutes
cache = Cache(app)

# Initialize the plotting cache
init_plot_cache(app)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    plot_keys = []

    if request.method == "POST":
        try:
            cache.clear()  # flush old plots

            # Read slider inputs
            inputs = {key: float(request.form[key]) for key in slider_config}

            # Read dropdown inputs
            for key in dropdown_config:
                inputs[key] = request.form[key]

            # ✅ Call simulate_burn using correct arguments
            results = simulate_burn(
                mdot_ox=inputs["mdot_ox"],
                rho_fuel=inputs["rho_fuel"],
                r1=inputs["r1"],     # UI uses cm
                L=inputs["L"]        # UI uses cm
            )

            # Generate summary text
            summary = print_summary(results)

            # Generate and cache plots
            plot_keys = save_all_plots(results)

        except Exception as e:
            summary = f"Error: {e}"
            plot_keys = []

    return render_template(
        "index.html",
        slider_config=slider_config,
        dropdown_config=dropdown_config,
        summary=summary,
        plot_keys=plot_keys
    )

@app.route("/plot/<key>")
def serve_plot(key):
    """
    Serve a cached plot image for the given cache key.
    """
    buf = get_cached_image(key)
    if buf is None:
        return "Plot not found", 404
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
