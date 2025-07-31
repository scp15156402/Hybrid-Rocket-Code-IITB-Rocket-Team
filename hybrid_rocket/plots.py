"""
Plotting utilities using matplotlib.
"""

import matplotlib.pyplot as plt

def plot_radius_vs_time(times, radii):
    """
    Plot port radius evolution.
    """
    plt.figure()
    plt.plot(times, radii)
    plt.xlabel("Time (s)")
    plt.ylabel("Port Radius (m)")
    plt.title("Port Radius vs Time")
    plt.grid(True)
    plt.show()

def plot_area_vs_time(times, areas):
    """
    Plot port area evolution.
    """
    plt.figure()
    plt.plot(times, areas)
    plt.xlabel("Time (s)")
    plt.ylabel("Port Area (m²)")
    plt.title("Port Area vs Time")
    plt.grid(True)
    plt.show()
