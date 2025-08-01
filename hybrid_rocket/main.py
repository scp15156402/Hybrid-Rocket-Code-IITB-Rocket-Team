# main.py

"""
main.py

Command-line interface for the Hybrid Rocket Simulation.
Uses all modules to run a simulation and display results.
Derived from integrated_code_HRM(4)_omn.ipynb.
"""

import argparse
from hybrid_rocket.solver import simulate_burn
from hybrid_rocket.plots import save_all_plots
from hybrid_rocket.export import export_simulation_data, print_summary

def run():
    parser = argparse.ArgumentParser(description="Hybrid Rocket Motor Burn Simulation")
    # Simulation geometry & propellant inputs (mirror notebook defaults: r1=0.7 cm, r2=1.9 cm, L=6 cm, mdot_ox=47 g/s, rho_fuel=930 kg/m³)
    parser.add_argument("--r1_init",    type=float, default=0.007,  help="Initial port radius r1 (m)")
    parser.add_argument("--r2_final",   type=float, default=0.019,  help="Final port radius r2 (m)")
    parser.add_argument("--L_fuel",     type=float, default=0.06,   help="Grain length L (m)")
    parser.add_argument("--mdot_ox",    type=float, default=0.047,  help="Oxidizer mass flow rate mdot_ox (kg/s)")
    parser.add_argument("--rho_fuel",   type=float, default=930.0,  help="Fuel density rho_fuel (kg/m³)")
    parser.add_argument("--export",     action="store_true",        help="Export results to CSV")
    args = parser.parse_args()

    # Convert SI inputs to the units expected by simulate_burn (cm, g/s)
    r1_cm    = args.r1_init  * 100.0    # m → cm
    r2_cm    = args.r2_final * 100.0    # m → cm
    L_cm     = args.L_fuel   * 100.0    # m → cm
    mdot_gps = args.mdot_ox  * 1000.0   # kg/s → g/s

    # Run simulation
    results = simulate_burn(
        r1=r1_cm,
        r2=r2_cm,
        L=L_cm,
        mdot_ox=mdot_gps,
        rho_fuel=args.rho_fuel
    )

    # Display summary to console
    print(print_summary(results))

    # Generate and cache plots
    cache_keys = save_all_plots(results)
    print(f"[INFO] Generated plots with cache keys: {cache_keys}")

    # Optionally export to CSV
    if args.export:
        export_simulation_data(results)
        print("[INFO] Simulation data exported.")

if __name__ == "__main__":
    run()
