'''
combustion.py

Combustion and regression calculations.
Includes regression rate, OF ratio, thrust, pressure.
Derived from integrated_code_HRM(4)_omn.ipynb.
'''

import numpy as np
from .constants import REG_A, REG_N, GRAVITY, R_UNIVERSAL


def regression_rate(G_ox: float) -> float:
    '''
    Fuel regression rate: r = a * G^n

    Parameters
    ----------
    G_ox : float
        Oxidizer mass flux (kg/m^2/s)

    Returns
    -------
    float
        Regression rate (m/s)
    '''
    return REG_A * G_ox**REG_N


def oxidizer_flux(mdot_ox: float, port_area: float) -> float:
    '''
    Computes oxidizer mass flux G = mdot / A
    '''
    return mdot_ox / port_area if port_area > 0 else 0.0


def fuel_mass_flow_rate(r: float, rho_fuel: float, port_radius: float, grain_length: float) -> float:
    '''
    Computes fuel mass flow rate based on regression speed and grain surface area.
    '''
    burning_area = 2 * np.pi * port_radius * grain_length
    return rho_fuel * burning_area * r


def of_ratio(mdot_ox: float, mdot_fuel: float) -> float:
    '''
    Oxidizer-to-Fuel Ratio
    '''
    return mdot_ox / mdot_fuel if mdot_fuel > 0 else 0


def thrust(mdot_total: float, Ve: float, pe: float, pa: float, Ae: float) -> float:
    '''
    Computes thrust based on ideal rocket equation.
    '''
    return mdot_total * Ve + (pe - pa) * Ae


def specific_impulse(thrust: float, mdot_total: float) -> float:
    '''
    Computes Isp = T / (mdot * g)
    '''
    return thrust / (mdot_total * GRAVITY) if mdot_total > 0 else 0
