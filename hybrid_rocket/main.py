"""
main.py

Command-line interface for the Hybrid Rocket Simulation.
Uses all modules to run a simulation and display results.
"""

import argparse
from hybrid_rocket.solver import simulate_burn
from hybrid_rocket.plots import plot_all
from hybrid_rocket.export import export_simulation_data, print_summary

def run():
    parser = argparse.ArgumentParser(description="Hybrid Rocket Motor Burn Simulation")
    parser.add_argument("--mdot_ox", type=float, default=0.05, help="Oxidizer mass flow rate (kg/s)")
    parser.add_argument("--rho_fuel", type=float, default=930, help="Fuel density (kg/m^3)")
    parser.add_argument("--r1", type=float, default=0.01, help="Initial port radius (m)")
    parser.add_argument("--L", type=float, default=0.1, help="Grain length (m)")
    parser.add_argument("--dt", type=float, default=0.01, help="Time step (s)")
    parser.add_argument("--t_final", type=float, default=3.0, help="Final burn time (s)")
    parser.add_argument("--Ve", type=float, default=1800.0, help="Nozzle exit velocity (m/s)")
    parser.add_argument("--pe", type=float, default=1e5, help="Nozzle exit pressure (Pa)")
    parser.add_argument("--pa", type=float, default=1e5, help="Ambient pressure (Pa)")
    parser.add_argument("--Ae", type=float, default=1e-4, help="Nozzle exit area (m^2)")
    parser.add_argument("--export", action="store_true", help="Export results to CSV")
    
    args = parser.parse_args()

    results = simulate_burn(
        mdot_ox=args.mdot_ox,
        rho_fuel=args.rho_fuel,
        r1_init=args.r1,
        L_grain=args.L,
        dt=args.dt,
        t_final=args.t_final,
        Ve=args.Ve,
        pe=args.pe,
        pa=args.pa,
        Ae=args.Ae,
    )

    # Visualize
    plot_all(results["time"], results["thrust"], results["radius"], results["OF"], results["G_ox"])

    # Summary
    print_summary(results)

    # Optional export
    if args.export:
        export_simulation_data(results)

if __name__ == "__main__":
    run()
