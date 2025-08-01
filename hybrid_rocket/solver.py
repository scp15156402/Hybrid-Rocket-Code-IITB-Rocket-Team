# hybrid_rocket/solver.py

"""
solver.py

Time-stepping hybrid rocket burn simulation engine.
Faithfully mirrors integrated_code_HRM(4)_omn.ipynb.
"""

import numpy as np
from hybrid_rocket.geometry import port_area, update_port_radius
from hybrid_rocket.combustion import (
    regression_rate,
    oxidizer_flux,
    fuel_mass_flow_rate,
    of_ratio,
    thrust,
    specific_impulse
)

def simulate_burn(
    r1: float,
    r2: float,
    L: float,
    mdot_ox: float,
    rho_fuel: float
) -> dict:
    """
    Simulates hybrid rocket motor burn from initial to final port radius.

    Parameters:
        r1 (float): Initial port radius (cm)
        r2 (float): Final port radius (cm)
        L (float): Grain length (cm)
        mdot_ox (float): Oxidizer mass flow rate (g/s)
        rho_fuel (float): Fuel density (kg/m³)

    Returns:
        dict: Time-series results for plotting and export
    """
    # Convert inputs to SI units
    r = r1 / 100.0               # cm → m
    r_max = r2 / 100.0           # cm → m
    L_m = L / 100.0              # cm → m
    mdot_ox_si = mdot_ox / 1000.0  # g/s → kg/s

    # Time stepping parameters
    t = 0.0
    dt = 0.01

    time_hist = []
    radius_hist = []
    thrust_hist = []
    of_hist = []
    G_ox_hist = []
    isp_hist = []

    # Main burn loop
    while r <= r_max:
        A_port = port_area(r)
        G = oxidizer_flux(mdot_ox_si, A_port)
        r_dot = regression_rate(G)
        mdot_fuel = fuel_mass_flow_rate(r_dot, rho_fuel, r, L_m)
        mdot_total = mdot_ox_si + mdot_fuel
        OF = of_ratio(mdot_ox_si, mdot_fuel)
        # Using fixed nozzle params from notebook
        T = thrust(mdot_total, Ve=1800.0, pe=1e5, pa=1e5, Ae=1e-4)
        Isp = specific_impulse(T, mdot_total)

        # Record history
        time_hist.append(t)
        radius_hist.append(r)
        thrust_hist.append(T)
        of_hist.append(OF)
        G_ox_hist.append(G)
        isp_hist.append(Isp)

        # Advance state
        r = update_port_radius(r, r_dot, dt)
        t += dt

    return {
        "time":   np.array(time_hist),
        "radius": np.array(radius_hist),
        "thrust": np.array(thrust_hist),
        "of":     np.array(of_hist),
        "G_ox":   np.array(G_ox_hist),
        "isp":    np.array(isp_hist)
    }
