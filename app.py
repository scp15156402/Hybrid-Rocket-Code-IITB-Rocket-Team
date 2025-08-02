# app.py

"""
app.py

Enhanced Flask application with complete notebook implementation.
EXACT integration of all missing features from integrated_code_HRM(4)_omn.ipynb.
"""

import os
from flask import Flask, render_template, request, send_file
from flask_caching import Cache

# ✅ Absolute imports with enhanced modules
from hybrid_rocket.solver import simulate_burn
from hybrid_rocket.export import print_summary, compute_structural_metrics
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
    # Start with defaults for all controls (EXACT notebook defaults)
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

            # 3. Run the ENHANCED burn simulation with all parameters
            results = simulate_burn(
                r1=current_values["r1"],            # cm
                r2=current_values["r2"],            # cm
                L=current_values["L"],              # cm
                mdot_ox=current_values["mdot_ox"],  # g/s
                rho_fuel=current_values["rho_fuel"], # kg/m³
                current_values=current_values       # Pass all parameters for advanced modeling
            )

            # 4. Generate comprehensive textual summary (EXACT notebook output)
            summary = print_summary(results, current_values)

            # 5. Generate & cache all plots including motor assembly and nozzle profile
            plot_keys = save_all_plots(results, current_values)

            # 6. Add performance warnings (EXACT notebook warnings)
            warnings = []
            
            # Check for high chamber pressure (notebook: > 40 bar)
            if 'p_c' in results and len(results['p_c']) > 0:
                max_pc = max(results['p_c'])
                if max_pc > 40e5:  # 40 bar in Pa
                    warnings.append("*** WARNING: Peak chamber pressure exceeds 40 bar! ***")
            
            # Check for low pressure warning
            if results.get('low_pressure_warning', False):
                warnings.append("*** WARNING: Chamber pressure dropped below 2 bar. Nozzle may not be choked. ***")
            
            # Add structural warnings if applicable
            if current_values:
                try:
                    struct_metrics = compute_structural_metrics(current_values, results)
                    
                    # Casing pressure check
                    if 'p_c' in results and len(results['p_c']) > 0:
                        max_pc = max(results['p_c'])
                        if max_pc > struct_metrics['max_pressure_design_casing']:
                            warnings.append("*** WARNING: Chamber pressure exceeds casing design pressure! ***")
                    
                    # Tank pressure check  
                    if struct_metrics['n2o_vapor_pressure'] > struct_metrics['max_pressure_design_ox_tank']:
                        warnings.append("*** WARNING: N₂O vapor pressure exceeds tank design pressure! ***")
                        
                except Exception as e:
                    warnings.append(f"*** WARNING: Could not verify structural safety: {str(e)} ***")
            
            # Append warnings to summary
            if warnings:
                summary += "\n\n--- SAFETY WARNINGS ---\n" + "\n".join(warnings)

        except Exception as e:
            summary = f"Error: {e}\n\nPlease check your input parameters and try again."
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
    """
    Serves cached plot images.
    Enhanced to handle all plot types including motor assembly.
    """
    buf = get_cached_image(key)
    if buf is None:
        return "Plot not found", 404
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

# Additional route for exporting simulation data (future enhancement)
@app.route("/export")
def export_data():
    """
    Route for exporting simulation data to CSV.
    Currently returns instructions - could be enhanced to export last simulation.
    """
    return """
    <h2>Data Export</h2>
    <p>To export simulation data:</p>
    <ol>
        <li>Run a simulation using the main interface</li>
        <li>Use the command line version: <code>python -m hybrid_rocket.main --export</code></li>
        <li>Check the generated CSV file in your working directory</li>
    </ol>
    <a href="/">← Back to Simulator</a>
    """

if __name__ == "__main__":
    # Disable the reloader on Windows to avoid socket/thread issues
    # Enable debug mode for development
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)