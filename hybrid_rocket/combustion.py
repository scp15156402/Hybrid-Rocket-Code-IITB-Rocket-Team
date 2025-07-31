'''
combustion.py

Combustion and regression calculations.
Includes regression rate, OF ratio, thrust, C*, Isp, exit velocity, pressure.
Derived from integrated_code_HRM(4)_omn.ipynb.
'''

import numpy as np
from .constants import REG_A, REG_N, GRAVITY, R_UNIVERSAL


def regression_rate(G_ox: float) -> float:
    '''
    Fuel regression rate: r = a * G^n
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
    return rho_fuel * burning_area(port_radius, grain_length) * r


def burning_area(port_radius: float, grain_length: float) -> float:
    '''
    Lateral burning surface area of grain.
    '''
    return 2 * np.pi * port_radius * grain_length


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


def ideal_exit_velocity(Tc: float, gamma: float, molar_mass: float) -> float:
    '''
    Computes ideal exit velocity from thermodynamics.
    '''
    R_specific = R_UNIVERSAL / (molar_mass / 1000)  # J/kg/K
    return np.sqrt((2 * gamma * R_specific * Tc) / (gamma - 1))


def characteristic_velocity(pc: float, At: float, mdot_total: float) -> float:
    '''
    Computes characteristic velocity C* = pc * At / mdot
    '''
    return pc * At / mdot_total if mdot_total > 0 else 0


def estimate_chamber_pressure(mdot_total: float, At: float, Tc: float, gamma: float, molar_mass: float) -> float:
    '''
    Estimates chamber pressure from flow and geometry.
    '''
    R_specific = R_UNIVERSAL / (molar_mass / 1000)
    term = (2 * gamma / (gamma + 1))**((gamma + 1)/(gamma - 1))
    return (mdot_total * R_specific * Tc) / (At * np.sqrt(term))
