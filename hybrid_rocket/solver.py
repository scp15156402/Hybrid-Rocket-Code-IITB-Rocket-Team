'''
solver.py

Time-stepping hybrid rocket burn simulation engine.
Migrated and modularized from integrated_code_HRM(4)_omn.ipynb.
'''

import numpy as np
from .geometry import port_area, update_port_radius
from .combustion import (regression_rate, oxidizer_flux, fuel_mass_flow_rate,
                         of_ratio, thrust, specific_impulse)


def simulate_burn(
    mdot_ox: float,
    rho_fuel: float,
    r1_init: float,
    L_grain: float,
    dt: float = 0.01,
    t_final: float = 5.0,
    pe: float = 1e5,
    pa: float = 1e5,
    Ae: float = 1e-4,
    Ve: float = 1800.0,
    r2_limit: float = None  # Optional radius limit (grain outer boundary)
):
    '''
    Runs a forward-time simulation of hybrid burn.

    Parameters
    ----------
    mdot_ox : float
        Oxidizer mass flow rate (kg/s)
    rho_fuel : float
        Fuel density (kg/m^3)
    r1_init : float
        Initial port radius (m)
    L_grain : float
        Grain length (m)
    dt : float
        Time step (s)
    t_final : float
        Total simulation time (s)
    pe, pa, Ae, Ve : float
        Nozzle exit pressure, ambient pressure, area, and velocity
    r2_limit : float
        Outer radius limit (m), simulation stops if radius exceeds this

    Returns
    -------
    dict : Simulation results history
    '''
    times, r_hist, thrust_hist, OF_hist, G_ox_hist, Isp_hist = [], [], [], [], [], []

    radius = r1_init
    t = 0.0
    while t <= t_final:
        A_port = port_area(radius)
        G_ox = oxidizer_flux(mdot_ox, A_port)
        r_dot = regression_rate(G_ox)
        mdot_fuel = fuel_mass_flow_rate(r_dot, rho_fuel, radius, L_grain)
        mdot_total = mdot_ox + mdot_fuel
        OF = of_ratio(mdot_ox, mdot_fuel)
        T = thrust(mdot_total, Ve, pe, pa, Ae)
        Isp = specific_impulse(T, mdot_total)

        # Record
        times.append(t)
        r_hist.append(radius)
        thrust_hist.append(T)
        OF_hist.append(OF)
        G_ox_hist.append(G_ox)
        Isp_hist.append(Isp)

        # Advance
        radius = update_port_radius(radius, r_dot, dt)
        t += dt

        # Stop if port radius exceeds fuel outer radius
        if r2_limit is not None and radius > r2_limit:
            break

    return {
        'time': np.array(times),
        'radius': np.array(r_hist),
        'thrust': np.array(thrust_hist),
        'OF': np.array(OF_hist),
        'G_ox': np.array(G_ox_hist),
        'Isp': np.array(Isp_hist)
    }
