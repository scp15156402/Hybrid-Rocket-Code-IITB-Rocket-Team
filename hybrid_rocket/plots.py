"""
plots.py

Visualization tools for hybrid rocket simulation results.
Uses Flask-Caching + BytesIO for in-memory image caching.
"""

import matplotlib.pyplot as plt
from io import BytesIO
from flask_caching import Cache

cache: Cache = None  # Will be initialized from the Flask app

def init_plot_cache(app):
    """
    Initializes Flask-Caching with SimpleCache.
    This should be called once in app.py.
    """
    global cache
    cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
    cache.init_app(app)


def _save_to_cache(fig, cache_key: str) -> str:
    """
    Save a matplotlib figure to a BytesIO buffer and store it in Flask cache.

    Returns:
        str: cache key (used to fetch via Flask route).
    """
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    cache.set(cache_key, buf, timeout=300)  # Cache for 5 minutes
    return cache_key


def plot_thrust_vs_time(time, thrust) -> str:
    fig, ax = plt.subplots()
    ax.plot(time, thrust, label='Thrust')
    ax.set(xlabel='Time (s)', ylabel='Thrust (N)', title='Thrust vs Time')
    ax.grid(True)
    ax.legend()
    return _save_to_cache(fig, "thrust_plot")


def plot_radius_vs_time(time, radius) -> str:
    fig, ax = plt.subplots()
    ax.plot(time, radius, label='Port Radius')
    ax.set(xlabel='Time (s)', ylabel='Radius (m)', title='Port Radius vs Time')
    ax.grid(True)
    ax.legend()
    return _save_to_cache(fig, "radius_plot")


def plot_of_vs_time(time, of) -> str:
    fig, ax = plt.subplots()
    ax.plot(time, of, label='O/F Ratio')
    ax.set(xlabel='Time (s)', ylabel='O/F Ratio', title='O/F Ratio vs Time')
    ax.grid(True)
    ax.legend()
    return _save_to_cache(fig, "of_plot")


def plot_gox_vs_time(time, G_ox) -> str:
    fig, ax = plt.subplots()
    ax.plot(time, G_ox, label='G_ox')
    ax.set(xlabel='Time (s)', ylabel='Oxidizer Mass Flux (kg/m²/s)', title='G_ox vs Time')
    ax.grid(True)
    ax.legend()
    return _save_to_cache(fig, "gox_plot")


def plot_isp_vs_time(time, isp) -> str:
    fig, ax = plt.subplots()
    ax.plot(time, isp, label='Specific Impulse')
    ax.set(xlabel='Time (s)', ylabel='Isp (s)', title='Specific Impulse vs Time')
    ax.grid(True)
    ax.legend()
    return _save_to_cache(fig, "isp_plot")


def save_all_plots(results: dict) -> list:
    """
    Generate all plots and store them in Flask's memory cache.

    Returns:
        List of cache keys (used as identifiers for /plot/<cache_key> route).
    """
    time = results["time"]
    thrust = results["thrust"]
    radius = results["radius"]
    of = results["of"]
    G_ox = results["G_ox"]
    isp = results.get("isp")

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
    Retrieves a BytesIO plot from the cache.

    Returns:
        BytesIO or None
    """
    return cache.get(cache_key)
