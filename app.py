import os
from flask import Flask, render_template, request, url_for
from hybrid_rocket.solver import simulate_burn
from hybrid_rocket.export import print_summary
from hybrid_rocket.slider_config import slider_config
from hybrid_rocket.plots import save_all_plots  # ✅ Now defined in plots.py

app = Flask(__name__)

# Ensure plots directory exists
PLOTS_DIR = os.path.join("static", "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    plot_urls = []

    if request.method == "POST":
        try:
            # Extract all slider values from the POST request
            inputs = {key: float(request.form[key]) for key in slider_config}

            # Run the rocket simulation
            results = simulate_burn(
                mdot_ox=inputs["mdot_ox"],
                rho_fuel=inputs["rho_fuel"],
                r1_init=inputs["r1"],
                L_grain=inputs["L"],
                dt=inputs["dt"],
                t_final=inputs["t_final"],
                Ve=inputs["Ve"],
                pe=inputs["pe"],
                pa=inputs["pa"],
                Ae=inputs["Ae"]
            )

            # Generate summary
            summary = print_summary(results)

            # Generate and save plots, get back file paths
            filepaths = save_all_plots(results, save_dir=PLOTS_DIR)

            # Convert full file paths to relative URLs Flask can serve
            plot_urls = [url_for("static", filename=os.path.relpath(path, "static")) for path in filepaths]

        except Exception as e:
            summary = f"Error: {e}"

    return render_template(
        "index.html",
        slider_config=slider_config,
        summary=summary,
        plot_urls=plot_urls
    )

if __name__ == "__main__":
    app.run(debug=True)
