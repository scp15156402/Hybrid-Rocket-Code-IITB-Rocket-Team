"""
main.py

Command-line interface for the Hybrid Rocket Simulation.
Uses all modules to run a simulation and display results.
"""

import argparse
from hybrid_rocket.solver import simulate_burn
from hybrid_rocket.plots import save_all_plots
from hybrid_rocket.export import export_simulation_data, print_summary


def run():
    parser = argparse.ArgumentParser(description="Hybrid Rocket Motor Burn Simulation")
    parser.add_argument("--mdot_ox", type=float, default=0.05, help="Oxidizer mass flow rate (kg/s)")
    parser.add_argument("--rho_fuel", type=float, default=930, help="Fuel density (kg/m³)")
    parser.add_argument("--r1_init", type=float, default=0.01, help="Initial port radius (m)")
    parser.add_argument("--L_fuel", type=float, default=0.1, help="Grain length (m)")
    parser.add_argument("--export", action="store_true", help="Export results to CSV")

    args = parser.parse_args()

    # ✅ Strictly mirrors solver.py and notebook input
    results = simulate_burn(
        mdot_ox=args.mdot_ox,
        rho_fuel=args.rho_fuel,
        r1_init=args.r1_init,
        L_fuel=args.L_fuel
    )

    print(print_summary(results))
    save_all_plots(results)

    if args.export:
        export_simulation_data(results)


if __name__ == "__main__":
    run()
