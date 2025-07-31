'''
export.py

Handles result exports and tabular summaries.
Derived from integrated_code_HRM(4)_omn.ipynb.
'''

import pandas as pd
import numpy as np


def export_simulation_data(results: dict, filename: str = "simulation_results.csv"):
    '''
    Exports time-series data (thrust, radius, OF, G_ox, Isp) to CSV.

    Parameters
    ----------
    results : dict
        Output from solver.simulate_burn()
    filename : str
        Output CSV file name
    '''
    df = pd.DataFrame({
        'Time (s)': results['time'],
        'Thrust (N)': results['thrust'],
        'Port Radius (m)': results['radius'],
        'O/F Ratio': results['OF'],
        'Oxidizer Mass Flux (kg/m^2/s)': results['G_ox'],
        'Specific Impulse (s)': results.get('Isp', [np.nan]*len(results['time']))
    })
    df.to_csv(filename, index=False)
    print(f"[INFO] Exported simulation data to {filename}")


def print_summary(results: dict) -> str:
    '''
    Returns a summary of key performance metrics as a string.
    '''
    total_impulse = np.trapz(results['thrust'], results['time'])
    avg_thrust = np.mean(results['thrust'])
    peak_thrust = np.max(results['thrust'])
    avg_OF = np.mean(results['OF'])
    avg_isp = np.mean(results['Isp']) if 'Isp' in results else np.nan

    summary = f"""
=== SIMULATION SUMMARY ===
Total Burn Time:     {results['time'][-1]:.2f} s
Total Impulse:       {total_impulse:.2f} Ns
Average Thrust:      {avg_thrust:.2f} N
Peak Thrust:         {peak_thrust:.2f} N
Average O/F Ratio:   {avg_OF:.2f}
Average Isp:         {avg_isp:.2f} s
"""
    return summary
