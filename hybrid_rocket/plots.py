# hybrid_rocket/plots.py

"""
plots.py

Visualization tools for hybrid rocket simulation results.
- Saves only the default plots to static/plots at init for fast load.
- Uses Flask-Caching + BytesIO for all custom-parameter runs.
Derived from integrated_code_HRM(4)_omn.ipynb.
"""

import os
import matplotlib
# Force non-interactive Agg backend to avoid GUI/thread issues
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from io import BytesIO
from flask_caching import Cache

from hybrid_rocket.solver import simulate_burn
from hybrid_rocket.slider_config import slider_config

# Directory where default static plots live
PLOTS_DIR = os.path.join(os.getcwd(), "static", "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

cache: Cache = None  # Initialized via init_plot_cache()


def init_plot_cache(app):
    """
    Initializes Flask-Caching with SimpleCache (for custom plots).
    Also ensures default plots are generated on disk.
    """
    global cache
    cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
    cache.init_app(app)

    # Generate default plots once
    _generate_default_plots()


def _save_to_cache(fig, cache_key: str) -> str:
    """
    Save a matplotlib figure to BytesIO and store in Flask cache.
    """
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    cache.set(cache_key, buf, timeout=300)
    return cache_key


def _save_default_to_disk(fig, filename: str):
    """
    Save a matplotlib figure directly to static/plots/<filename>.png
    """
    path = os.path.join(PLOTS_DIR, f"{filename}.png")
    fig.savefig(path, format='png', bbox_inches='tight')
    plt.close(fig)


def _generate_default_plots():
    """
    Runs one simulation with all slider defaults and writes those plots
    out to disk so they load instantly via static files.
    """
    # Extract default values from slider_config
    defaults = {k: v["default"] for k, v in slider_config.items()}
    # simulate_burn expects: r1, r2, L, mdot_ox, rho_fuel
    results = simulate_burn(
        r1=defaults["r1"],
        r2=defaults["r2"],
        L=defaults["L"],
        mdot_ox=defaults["mdot_ox"],
        rho_fuel=defaults["rho_fuel"]
    )

    time   = results["time"]
    thrust = results["thrust"]
    radius = results["radius"]
    of     = results["of"]
    G_ox   = results["G_ox"]
    isp    = results.get("isp")

    # Create & save each default plot to disk
    fig, ax = plt.subplots()
    ax.plot(time, thrust, label='Thrust')
    ax.set(xlabel='Time (s)', ylabel='Thrust (N)', title='Thrust vs Time')
    ax.grid(True); ax.legend()
    _save_default_to_disk(fig, "thrust_plot")

    fig, ax = plt.subplots()
    ax.plot(time, radius, label='Port Radius')
    ax.set(xlabel='Time (s)', ylabel='Radius (m)', title='Port Radius vs Time')
    ax.grid(True); ax.legend()
    _save_default_to_disk(fig, "radius_plot")

    fig, ax = plt.subplots()
    ax.plot(time, of, label='O/F Ratio')
    ax.set(xlabel='Time (s)', ylabel='O/F Ratio', title='O/F Ratio vs Time')
    ax.grid(True); ax.legend()
    _save_default_to_disk(fig, "of_plot")

    fig, ax = plt.subplots()
    ax.plot(time, G_ox, label='Oxidizer Flux')
    ax.set(xlabel='Time (s)', ylabel='Oxidizer Mass Flux (kg/m²/s)', title='G_ox vs Time')
    ax.grid(True); ax.legend()
    _save_default_to_disk(fig, "gox_plot")

    if isp is not None:
        fig, ax = plt.subplots()
        ax.plot(time, isp, label='Specific Impulse')
        ax.set(xlabel='Time (s)', ylabel='Isp (s)', title='Specific Impulse vs Time')
        ax.grid(True); ax.legend()
        _save_default_to_disk(fig, "isp_plot")


def plot_thrust_vs_time(time, thrust) -> str:
    fig, ax = plt.subplots()
    ax.plot(time, thrust, label='Thrust')
    ax.set(xlabel='Time (s)', ylabel='Thrust (N)', title='Thrust vs Time')
    ax.grid(True); ax.legend()
    return _save_to_cache(fig, "thrust_plot")


def plot_radius_vs_time(time, radius) -> str:
    fig, ax = plt.subplots()
    ax.plot(time, radius, label='Port Radius')
    ax.set(xlabel='Time (s)', ylabel='Radius (m)', title='Port Radius vs Time')
    ax.grid(True); ax.legend()
    return _save_to_cache(fig, "radius_plot")


def plot_of_vs_time(time, of) -> str:
    fig, ax = plt.subplots()
    ax.plot(time, of, label='O/F Ratio')
    ax.set(xlabel='Time (s)', ylabel='O/F Ratio', title='O/F Ratio vs Time')
    ax.grid(True); ax.legend()
    return _save_to_cache(fig, "of_plot")


def plot_gox_vs_time(time, G_ox) -> str:
    fig, ax = plt.subplots()
    ax.plot(time, G_ox, label='Oxidizer Flux')
    ax.set(xlabel='Time (s)', ylabel='Oxidizer Mass Flux (kg/m²/s)', title='G_ox vs Time')
    ax.grid(True); ax.legend()
    return _save_to_cache(fig, "gox_plot")


def plot_isp_vs_time(time, isp) -> str:
    fig, ax = plt.subplots()
    ax.plot(time, isp, label='Specific Impulse')
    ax.set(xlabel='Time (s)', ylabel='Isp (s)', title='Specific Impulse vs Time')
    ax.grid(True); ax.legend()
    return _save_to_cache(fig, "isp_plot")


def save_all_plots(results: dict) -> list:
    """
    Generate all plots and store them in Flask's in-memory cache
    (custom runs only). Default plots already live in static/plots.
    """
    time   = results["time"]
    thrust = results["thrust"]
    radius = results["radius"]
    of     = results["of"]
    G_ox   = results["G_ox"]
    isp    = results.get("isp")

    keys = [
        plot_thrust_vs_time(time, thrust),
        plot_radius_vs_time(time, radius),
        plot_of_vs_time(time, of),
        plot_gox_vs_time(time, G_ox),
    ]
    if isp is not None:
        keys.append(plot_isp_vs_time(time, isp))
    return keys


def get_cached_image(cache_key: str) -> BytesIO | None:
    """
    Retrieves a BytesIO image from the cache by key.
    Returns None if not found.
    """
    return cache.get(cache_key)
