"""
Entry point for simulation.
"""

import argparse
from .solver import simulate_burn
from .plots import plot_radius_vs_time, plot_area_vs_time

def run():
    parser = argparse.ArgumentParser(description="Hybrid Rocket Simulation")
    parser.add_argument("--time", type=float, default=10.0, help="Total burn time (s)")
    parser.add_argument("--dt",   type=float, default=0.1,  help="Time step (s)")
    parser.add_argument("--flux", type=float, default=50.0, help="Oxidizer mass flux (kg/m²/s)")
    args = parser.parse_args()

    times, radii, areas = simulate_burn(args.time, args.dt, args.flux)

    plot_radius_vs_time(times, radii)
    plot_area_vs_time(times, areas)

if __name__ == "__main__":
    run()
