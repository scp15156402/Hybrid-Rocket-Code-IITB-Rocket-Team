# hybrid_rocket/main.py

"""
main.py

Enhanced command-line interface for the Hybrid Rocket Simulation.
EXACT implementation from integrated_code_HRM(4)_omn.ipynb with all features.
Includes structural analysis, comprehensive output, and export capabilities.
"""

import argparse
from hybrid_rocket.solver import simulate_burn
from hybrid_rocket.plots import save_all_plots
from hybrid_rocket.export import export_simulation_data, print_summary, compute_structural_metrics
from hybrid_rocket.slider_config import slider_config, dropdown_config

def run():
    parser = argparse.ArgumentParser(description="Enhanced Hybrid Rocket Motor Burn Simulation")
    
    # Core simulation parameters (EXACT notebook defaults)
    parser.add_argument("--r1_init",    type=float, default=0.7,   help="Initial port radius r1 (cm)")
    parser.add_argument("--r2_final",   type=float, default=1.9,   help="Final port radius r2 (cm)")
    parser.add_argument("--L_fuel",     type=float, default=6.0,   help="Grain length L (cm)")
    parser.add_argument("--mdot_ox",    type=float, default=47.0,  help="Oxidizer mass flow rate (g/s)")
    parser.add_argument("--rho_fuel",   type=float, default=930.0, help="Fuel density (kg/m³)")
    
    # Enhanced parameters (notebook structural/tank parameters)
    parser.add_argument("--throat_diameter", type=float, default=6.0, help="Throat diameter (mm)")
    parser.add_argument("--casing_wall_thk", type=float, default=3.0, help="Casing wall thickness (mm)")
    parser.add_argument("--safety_factor",   type=float, default=2.0, help="Casing safety factor")
    parser.add_argument("--ox_tank_temp",    type=float, default=25.0, help="Oxidizer tank temperature (°C)")
    parser.add_argument("--ox_tank_length",  type=float, default=30.0, help="Oxidizer tank length (cm)")
    parser.add_argument("--ox_tank_diameter", type=float, default=10.0, help="Oxidizer tank diameter (cm)")
    
    # Material selections
    parser.add_argument("--casing_material", type=str, default="SS304", help="Casing material")
    parser.add_argument("--tank_material",   type=str, default="SS304", help="Tank material")
    
    # Output options
    parser.add_argument("--export",         action="store_true", help="Export results to CSV")
    parser.add_argument("--detailed",       action="store_true", help="Show detailed structural analysis")
    parser.add_argument("--warnings",       action="store_true", help="Show safety warnings")
    
    args = parser.parse_args()

    # Build current_values dict for enhanced simulation (EXACT notebook parameter names)
    current_values = {
        # Core parameters
        "r1": args.r1_init,
        "r2": args.r2_final,
        "L": args.L_fuel,
        "mdot_ox": args.mdot_ox,
        "rho_fuel": args.rho_fuel,
        
        # Enhanced parameters (using slider_config defaults where not specified)
        "throat_diameter": args.throat_diameter,
        "casing_wall_thk": args.casing_wall_thk,
        "safety_factor": args.safety_factor,
        "ox_tank_temp": args.ox_tank_temp,
        "ox_tank_length": args.ox_tank_length,
        "ox_tank_outer_diameter": args.ox_tank_diameter,
        "casing_material": args.casing_material,
        "ox_tank_material": args.tank_material,
        
        # Use defaults for other parameters
        **{k: v["default"] for k, v in slider_config.items() if k not in [
            "r1", "r2", "L", "mdot_ox", "rho_fuel", "throat_diameter", 
            "casing_wall_thk", "safety_factor", "ox_tank_temp", 
            "ox_tank_length", "ox_tank_outer_diameter"
        ]},
        **{k: v["default"] for k, v in dropdown_config.items() if k not in [
            "casing_material", "ox_tank_material"
        ]}
    }

    print("=== ENHANCED HYBRID ROCKET SIMULATION ===")
    print(f"Configuration: r1={args.r1_init}cm, r2={args.r2_final}cm, L={args.L_fuel}cm")
    print(f"Oxidizer flow: {args.mdot_ox} g/s, Fuel density: {args.rho_fuel} kg/m³")
    print(f"Throat: {args.throat_diameter}mm, Tank temp: {args.ox_tank_temp}°C")
    print("")

    # Run enhanced simulation
    print("Running enhanced simulation with dynamic chamber pressure...")
    results = simulate_burn(
        r1=args.r1_init,
        r2=args.r2_final,
        L=args.L_fuel,
        mdot_ox=args.mdot_ox,
        rho_fuel=args.rho_fuel,
        current_values=current_values  # Enable advanced modeling
    )

    # Display comprehensive summary
    print("\n" + "="*60)
    print("SIMULATION RESULTS")
    print("="*60)
    print(print_summary(results, current_values))

    # Show enhanced metrics if available
    if 'Tc' in results and len(results['Tc']) > 0:
        print(f"\n--- ENHANCED METRICS ---")
        print(f"Peak Combustion Temperature: {max(results['Tc']):.0f} K")
        
    if 'p_c' in results and len(results['p_c']) > 0:
        print(f"Peak Chamber Pressure: {max(results['p_c'])/1e5:.2f} bar")
        print(f"Final Chamber Pressure: {results['p_c'][-1]/1e5:.2f} bar")

    # Detailed structural analysis
    if args.detailed:
        try:
            print(f"\n--- DETAILED STRUCTURAL ANALYSIS ---")
            struct_metrics = compute_structural_metrics(current_values, results)
            
            print(f"Casing Inner Diameter: {struct_metrics['casing_inner_diameter']*1000:.1f} mm")
            print(f"Casing Allowable Pressure: {struct_metrics['max_pressure_design_casing']/1e5:.2f} bar")
            print(f"Tank Allowable Pressure: {struct_metrics['max_pressure_design_ox_tank']/1e5:.2f} bar")
            print(f"Total Structural Mass: {struct_metrics['total_motor_structure_mass']:.3f} kg")
            print(f"Total Vehicle Mass: {struct_metrics['total_mass']:.3f} kg")
            print(f"Thrust-to-Weight: {struct_metrics['thrust_to_weight_ratio']:.2f}")
            
        except Exception as e:
            print(f"Could not compute detailed structural analysis: {e}")

    # Safety warnings
    if args.warnings:
        print(f"\n--- SAFETY ANALYSIS ---")
        warnings = []
        
        if 'p_c' in results and len(results['p_c']) > 0:
            max_pc = max(results['p_c'])
            if max_pc > 40e5:
                warnings.append("*** WARNING: Peak chamber pressure exceeds 40 bar! ***")
                
        if results.get('low_pressure_warning', False):
            warnings.append("*** WARNING: Chamber pressure dropped below 2 bar ***")
            
        if results.get('stop_reason') == "Reached 90% oxidizer consumption":
            warnings.append("*** INFO: Simulation ended due to oxidizer depletion ***")
            
        if warnings:
            for warning in warnings:
                print(warning)
        else:
            print("No safety warnings detected.")

    # Generate plots (console can't display, but files are created)
    print(f"\n--- GENERATING PLOTS ---")
    try:
        # Note: CLI version can't display plots but can save them
        cache_keys = save_all_plots(results, current_values)
        print(f"Generated {len(cache_keys)} plot files in static/plots/")
        print("Available plots:", ", ".join(cache_keys))
    except Exception as e:
        print(f"Error generating plots: {e}")

    # Export to CSV if requested
    if args.export:
        print(f"\n--- EXPORTING DATA ---")
        filename = f"hybrid_rocket_simulation_{args.r1_init}cm_to_{args.r2_final}cm.csv"
        export_simulation_data(results, filename)
        print(f"Data exported to: {filename}")

    print(f"\n--- SIMULATION COMPLETE ---")
    print(f"Burn time: {results['time'][-1]:.3f} s")
    print(f"Total impulse: {results.get('total_impulse', 'N/A')} Ns")
    print(f"Data points: {len(results['time'])}")

if __name__ == "__main__":
    run()