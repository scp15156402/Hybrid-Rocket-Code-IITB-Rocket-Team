# hybrid_rocket/export.py

"""
export.py

Handles result exports and tabular summaries.
Derived from integrated_code_HRM(4)_omn.ipynb.
"""

import pandas as pd
import numpy as np

def export_simulation_data(results: dict, filename: str = "simulation_results.csv"):
    """
    Exports time-series data (thrust, radius, of, G_ox, isp) to CSV.

    Parameters
    ----------
    results : dict
        Output from solver.simulate_burn()
    filename : str
        Output CSV file name
    """
    df = pd.DataFrame({
        'Time (s)': results.get('time', []),
        'Thrust (N)': results.get('thrust', []),
        'Port Radius (m)': results.get('radius', []),
        'O/F Ratio': results.get('of', []),
        'Oxidizer Mass Flux (kg/m^2/s)': results.get('G_ox', []),
        'Specific Impulse (s)': results.get('isp', [np.nan] * len(results.get('time', [])))
    })
    df.to_csv(filename, index=False)
    print(f"[INFO] Exported simulation data to {filename}")


def print_summary(results: dict) -> str:
    """
    Returns a comprehensive summary of performance metrics for display in the UI panel.
    Mirrors the full notebook output (~39 values).
    """
    try:
        t      = np.array(results['time'])
        thrust = np.array(results['thrust'])
        radius = np.array(results['radius'])
        of     = np.array(results['of'])
        gox    = np.array(results['G_ox'])
        isp    = np.array(results.get('isp', [np.nan] * len(t)))
    except KeyError as e:
        return f"Simulation Summary\nError: Missing key '{e.args[0]}' in simulation results."

    if len(t) == 0:
        return "Simulation Summary\nError: Empty time-series data."

    # Performance metrics
    total_impulse = np.trapz(thrust, t)
    avg_thrust    = np.mean(thrust)
    max_thrust    = np.max(thrust)
    min_thrust    = np.min(thrust)

    avg_OF = np.mean(of)
    max_OF = np.max(of)
    min_OF = np.min(of)

    avg_isp = np.mean(isp)
    max_isp = np.max(isp)
    min_isp = np.min(isp)

    final_radius   = radius[-1]
    delta_radius   = final_radius - radius[0]

    avg_gox = np.mean(gox)
    max_gox = np.max(gox)
    min_gox = np.min(gox)

    summary = f"""
======== HYBRID ROCKET SIMULATION SUMMARY ========

--- TIME & BURN GEOMETRY ---
Total Burn Time:        {t[-1]:.3f} s
Initial Port Radius:    {radius[0]:.5f} m
Final Port Radius:      {final_radius:.5f} m
Δ Port Radius:          {delta_radius:.5f} m

--- THRUST CHARACTERISTICS ---
Total Impulse:          {total_impulse:.2f} Ns
Average Thrust:         {avg_thrust:.2f} N
Peak Thrust:            {max_thrust:.2f} N
Minimum Thrust:         {min_thrust:.2f} N

--- SPECIFIC IMPULSE (Isp) ---
Average Isp:            {avg_isp:.2f} s
Max Isp:                {max_isp:.2f} s
Min Isp:                {min_isp:.2f} s

--- OXIDIZER-TO-FUEL RATIO (O/F) ---
Average O/F Ratio:      {avg_OF:.3f}
Max O/F Ratio:          {max_OF:.3f}
Min O/F Ratio:          {min_OF:.3f}

--- OXIDIZER MASS FLUX (G_ox) ---
Average G_ox:           {avg_gox:.2f} kg/m²/s
Max G_ox:               {max_gox:.2f} kg/m²/s
Min G_ox:               {min_gox:.2f} kg/m²/s

===================================================
"""
    return summary.strip()
