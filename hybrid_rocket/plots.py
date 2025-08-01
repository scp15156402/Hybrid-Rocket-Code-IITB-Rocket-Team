"""
plots.py

Visualization tools for hybrid rocket simulation results.
Modified for use with Flask: saves plots to static/plots/ directory.
"""

import os
import matplotlib.pyplot as plt
from datetime import datetime

# Directory where plots will be saved
PLOT_DIR = "static/plots"
os.makedirs(PLOT_DIR, exist_ok=True)


def save_plot(fig, name_prefix):
    """
    Saves the given matplotlib figure to the static/plots directory
    with a unique timestamped filename.
    
    Returns:
        str: Relative path to the saved image.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = f"{name_prefix}_{timestamp}.png"
    path = os.path.join(PLOT_DIR, filename)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return filename  # Return just the filename for use in url_for()


def plot_thrust_vs_time(time, thrust):
    fig, ax = plt.subplots()
    ax.plot(time, thrust, label='Thrust')
    ax.set(xlabel='Time (s)', ylabel='Thrust (N)', title='Thrust vs Time')
    ax.grid(True)
    ax.legend()
    return save_plot(fig, "thrust")


def plot_radius_vs_time(time, radius):
    fig, ax = plt.subplots()
    ax.plot(time, radius, label='Port Radius')
    ax.set(xlabel='Time (s)', ylabel='Radius (m)', title='Port Radius vs Time')
    ax.grid(True)
    ax.legend()
    return save_plot(fig, "radius")


def plot_of_vs_time(time, of):
    fig, ax = plt.subplots()
    ax.plot(time, of, label='O/F Ratio')
    ax.set(xlabel='Time (s)', ylabel='O/F Ratio', title='O/F Ratio vs Time')
    ax.grid(True)
    ax.legend()
    return save_plot(fig, "of")


def plot_gox_vs_time(time, G_ox):
    fig, ax = plt.subplots()
    ax.plot(time, G_ox, label='G_ox')
    ax.set(xlabel='Time (s)', ylabel='Oxidizer Mass Flux (kg/m²/s)', title='Oxidizer Mass Flux vs Time')
    ax.grid(True)
    ax.legend()
    return save_plot(fig, "gox")


def plot_isp_vs_time(time, isp):
    fig, ax = plt.subplots()
    ax.plot(time, isp, label='Specific Impulse')
    ax.set(xlabel='Time (s)', ylabel='Isp (s)', title='Specific Impulse vs Time')
    ax.grid(True)
    ax.legend()
    return save_plot(fig, "isp")


def save_all_plots(results, save_dir=PLOT_DIR):
    """
    Wrapper to generate and save all relevant plots using the simulation results.

    Args:
        results (dict): Dictionary containing time-series data like thrust, radius, etc.
        save_dir (str): Directory to save plots (default is static/plots)

    Returns:
        list[str]: List of saved image filenames (for use with url_for)
    """
    time = results["time"]
    thrust = results["thrust"]
    radius = results["radius"]
    of = results["of"]
    G_ox = results["G_ox"]
    isp = results.get("isp")  # Optional

    filenames = [
        plot_thrust_vs_time(time, thrust),
        plot_radius_vs_time(time, radius),
        plot_of_vs_time(time, of),
        plot_gox_vs_time(time, G_ox)
    ]

    if isp is not None:
        filenames.append(plot_isp_vs_time(time, isp))

    return filenames
