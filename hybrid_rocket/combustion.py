# hybrid_rocket/combustion.py

"""
combustion.py

Combustion and regression calculations.
Includes regression rate, oxidizer flux, OF ratio, thrust, Isp, C*, and ideal exit velocity.
Derived from integrated_code_HRM(4)_omn.ipynb.
"""

import numpy as np
from .constants import REG_A, REG_N, GRAVITY, R_UNIVERSAL


def regression_rate(G_ox: float) -> float:
    """
    Computes fuel regression rate: r = a * G^n

    Parameters:
        G_ox : float
            Oxidizer mass flux (kg/m²/s)

    Returns:
        float : Fuel regression rate (m/s)
    """
    return REG_A * G_ox**REG_N


def oxidizer_flux(mdot_ox: float, port_area: float) -> float:
    """
    Computes oxidizer mass flux: G = mdot / A

    Parameters:
        mdot_ox : float
            Oxidizer mass flow rate (kg/s)
        port_area : float
            Port cross-sectional area (m²)

    Returns:
        float : Mass flux (kg/m²/s)
    """
    return mdot_ox / port_area if port_area > 0 else 0.0


def burning_area(port_radius: float, grain_length: float) -> float:
    """
    Computes burning surface area: lateral area of the grain cylinder.

    Parameters:
        port_radius : float
            Current port radius (m)
        grain_length : float
            Grain length (m)

    Returns:
        float : Burning surface area (m²)
    """
    return 2 * np.pi * port_radius * grain_length


def fuel_mass_flow_rate(r: float, rho_fuel: float, port_radius: float, grain_length: float) -> float:
    """
    Computes fuel mass flow rate: ṁ_fuel = ρ * A_burn * r

    Parameters:
        r : float
            Regression rate (m/s)
        rho_fuel : float
            Fuel density (kg/m³)
        port_radius : float
            Current port radius (m)
        grain_length : float
            Grain length (m)

    Returns:
        float : Fuel mass flow rate (kg/s)
    """
    A_burn = burning_area(port_radius, grain_length)
    return rho_fuel * A_burn * r


def of_ratio(mdot_ox: float, mdot_fuel: float) -> float:
    """
    Computes Oxidizer-to-Fuel ratio.

    Parameters:
        mdot_ox : float
            Oxidizer mass flow rate (kg/s)
        mdot_fuel : float
            Fuel mass flow rate (kg/s)

    Returns:
        float : OF ratio (dimensionless)
    """
    return mdot_ox / mdot_fuel if mdot_fuel > 0 else 0.0


def thrust(mdot_total: float, Ve: float, pe: float, pa: float, Ae: float) -> float:
    """
    Computes thrust using ideal rocket thrust equation:
    T = ṁ * Ve + (pe - pa) * Ae

    Parameters:
        mdot_total : float
            Total mass flow rate (kg/s)
        Ve : float
            Exit velocity (m/s)
        pe : float
            Exit pressure (Pa)
        pa : float
            Ambient pressure (Pa)
        Ae : float
            Nozzle exit area (m²)

    Returns:
        float : Thrust (N)
    """
    return mdot_total * Ve + (pe - pa) * Ae


def specific_impulse(thrust: float, mdot_total: float) -> float:
    """
    Computes specific impulse (Isp = Thrust / (ṁ * g))

    Parameters:
        thrust : float
            Thrust (N)
        mdot_total : float
            Total mass flow rate (kg/s)

    Returns:
        float : Specific impulse (s)
    """
    return thrust / (mdot_total * GRAVITY) if mdot_total > 0 else 0.0


def ideal_exit_velocity(Tc: float, gamma: float, molar_mass: float) -> float:
    """
    Computes ideal exit velocity from chamber temperature.

    Parameters:
        Tc : float
            Chamber temperature (K)
        gamma : float
            Specific heat ratio (Cp/Cv)
        molar_mass : float
            Molar mass of exhaust gas (g/mol)

    Returns:
        float : Ideal exhaust velocity (m/s)
    """
    R_specific = R_UNIVERSAL / (molar_mass / 1000)  # Convert g/mol → kg/mol
    return np.sqrt((2 * gamma * R_specific * Tc) / (gamma - 1))


def characteristic_velocity(pc: float, At: float, mdot_total: float) -> float:
    """
    Computes characteristic velocity C* = pc * At / ṁ

    Parameters:
        pc : float
            Chamber pressure (Pa)
        At : float
            Nozzle throat area (m²)
        mdot_total : float
            Total mass flow rate (kg/s)

    Returns:
        float : Characteristic velocity (m/s)
    """
    return pc * At / mdot_total if mdot_total > 0 else 0.0


def estimate_chamber_pressure(mdot_total: float, At: float, Tc: float, gamma: float, molar_mass: float) -> float:
    """
    Estimates chamber pressure (pc) from nozzle geometry and flow properties.

    Parameters:
        mdot_total : float
            Total mass flow rate (kg/s)
        At : float
            Throat area (m²)
        Tc : float
            Chamber temperature (K)
        gamma : float
            Specific heat ratio
        molar_mass : float
            Exhaust molar mass (g/mol)

    Returns:
        float : Estimated chamber pressure (Pa)
    """
    R_specific = R_UNIVERSAL / (molar_mass / 1000)
    term = (2 * gamma / (gamma + 1)) ** ((gamma + 1) / (gamma - 1))
    return (mdot_total * R_specific * Tc) / (At * np.sqrt(term))
