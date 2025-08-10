# hybrid_rocket/combustion.py

"""
combustion.py

Combustion physics implementation for Hybrid Rocket Simulation.
EXACT implementation from integrated_code_HRM(4)_omn.ipynb notebook.
Includes regression rate, mass flows, thrust, Isp, chamber pressure calculations.
"""

import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import newton
from rocket_simulations.hybrid_rocket.data.constants import (
    GRAVITY, R_UNIVERSAL, GAMMA, M_EXHAUST, R_SPECIFIC, P_AMBIENT,
    REG_A, REG_N, OF_DATA, T_COMBUSTION_DATA, PRESSURE_SPLINE, DENSITY_SPLINE
)

# -----------------------------
# Combustion Temperature Interpolation (EXACT from notebook)
# -----------------------------
temp_interp = interp1d(OF_DATA, T_COMBUSTION_DATA, kind='cubic',
                       bounds_error=False,
                       fill_value=(T_COMBUSTION_DATA[0], T_COMBUSTION_DATA[-1]))

def get_Tc(OF: float) -> float:
    """
    Returns combustion temperature [K] for given O/F ratio.
    EXACT implementation from notebook get_Tc function.
    """
    return float(temp_interp(OF))


# -----------------------------
# N₂O Properties Functions (EXACT from notebook)
# -----------------------------
def n2o_pressure(temp_c: float) -> float:
    """
    Returns N₂O saturated vapor pressure [bar] at given temperature [°C].
    EXACT implementation from notebook pressure_spline.
    """
    return float(PRESSURE_SPLINE(temp_c))


def n2o_liquid_density(temp_c: float) -> float:
    """
    Returns N₂O liquid density [kg/m³] at given temperature [°C].
    EXACT implementation from notebook density_spline.
    """
    return float(DENSITY_SPLINE(temp_c))


# -----------------------------
# Choked Flow Solver (EXACT from notebook)
# -----------------------------
def solve_choked_pressure(mdot_total: float, A_t: float, R_spec: float, Tc: float) -> float:
    """
    Invert the choked-flow relation to compute chamber pressure (Pa).
    EXACT implementation from notebook solve_choked_pressure function.
    
    Parameters:
        mdot_total: Total mass flow rate [kg/s]
        A_t: Throat area [m²]
        R_spec: Specific gas constant [J/(kg·K)]
        Tc: Combustion temperature [K]
    
    Returns:
        Chamber pressure [Pa]
    """
    # EXACT notebook calculation
    factor = np.sqrt(GAMMA/(R_spec * Tc)) * ((2/(GAMMA + 1))**((GAMMA + 1)/(2*(GAMMA - 1))))
    
    # Avoid division by zero (notebook safety check)
    if factor == 0:
        return P_AMBIENT
    
    return mdot_total / (A_t * factor)


# -----------------------------
# Core Combustion Functions (EXACT from notebook)
# -----------------------------
def regression_rate(G_ox: float) -> float:
    """
    Computes fuel regression rate using power law: r_dot = a * G_ox^n
    EXACT implementation from notebook.
    
    Parameters:
        G_ox: Oxidizer mass flux [kg/(m²·s)]
    
    Returns:
        Regression rate [m/s]
    """
    return REG_A * (G_ox ** REG_N)


def oxidizer_flux(mdot_ox: float, A_port: float) -> float:
    """
    Computes oxidizer mass flux through port.
    EXACT implementation from notebook: G_ox = mdot_ox / (pi * r1**2)
    
    Parameters:
        mdot_ox: Oxidizer mass flow rate [kg/s]
        A_port: Port cross-sectional area [m²]
    
    Returns:
        Oxidizer mass flux [kg/(m²·s)]
    """
    return mdot_ox / A_port if A_port > 0 else 0.0


def fuel_mass_flow_rate(r_dot: float, rho_fuel: float, r: float, L_grain: float) -> float:
    """
    Computes fuel mass flow rate from regression.
    EXACT implementation from notebook: mdot_f = 2 * pi * r1 * L_grain * rho_fuel * r_dot
    
    Parameters:
        r_dot: Regression rate [m/s]
        rho_fuel: Fuel density [kg/m³]
        r: Current port radius [m]
        L_grain: Grain length [m]
    
    Returns:
        Fuel mass flow rate [kg/s]
    """
    return 2 * np.pi * r * L_grain * rho_fuel * r_dot


def of_ratio(mdot_ox: float, mdot_fuel: float) -> float:
    """
    Computes oxidizer-to-fuel ratio.
    EXACT implementation from notebook: OF = mdot_ox / mdot_f
    
    Parameters:
        mdot_ox: Oxidizer mass flow rate [kg/s]
        mdot_fuel: Fuel mass flow rate [kg/s]
    
    Returns:
        O/F ratio [dimensionless]
    """
    if mdot_fuel <= 1e-9:  # Notebook safety check
        return 10.0  # Notebook default cap
    return mdot_ox / mdot_fuel


# -----------------------------
# Thrust and Performance (EXACT from notebook)
# -----------------------------
def exhaust_velocity(p_c: float, Tc: float, p_e: float = P_AMBIENT) -> float:
    """
    Computes exhaust velocity from isentropic expansion.
    EXACT implementation from notebook: v_e = sqrt((2*k/(k-1)) * R_spec * Tc * (1 - (p_ambient/p_c)**((k-1)/k)))
    
    Parameters:
        p_c: Chamber pressure [Pa]
        Tc: Combustion temperature [K]
        p_e: Exit pressure [Pa] (defaults to ambient)
    
    Returns:
        Exhaust velocity [m/s]
    """
    if p_c <= p_e or (GAMMA - 1) == 0:  # Notebook safety checks
        return 0.0
    
    exponent = (GAMMA - 1) / GAMMA
    term = 1 - (p_e / p_c) ** exponent
    
    return np.sqrt((2 * GAMMA / (GAMMA - 1)) * R_SPECIFIC * Tc * term)


def thrust_from_momentum(mdot_total: float, v_e: float, p_e: float = P_AMBIENT, A_e: float = 0.0) -> float:
    """
    Computes thrust from momentum and pressure terms.
    EXACT implementation from notebook: thrust = mdot_total * v_e (simplified, no pressure term in notebook)
    
    Parameters:
        mdot_total: Total mass flow rate [kg/s]
        v_e: Exhaust velocity [m/s]
        p_e: Exit pressure [Pa]
        A_e: Exit area [m²]
    
    Returns:
        Thrust [N]
    """
    momentum_thrust = mdot_total * v_e
    pressure_thrust = (p_e - P_AMBIENT) * A_e
    return momentum_thrust + pressure_thrust


def specific_impulse(thrust: float, mdot_total: float) -> float:
    """
    Computes specific impulse.
    Standard definition: Isp = thrust / (mdot_total * g)
    
    Parameters:
        thrust: Thrust [N]
        mdot_total: Total mass flow rate [kg/s]
    
    Returns:
        Specific impulse [s]
    """
    if mdot_total <= 0:
        return 0.0
    return thrust / (mdot_total * GRAVITY)


# -----------------------------
# Nozzle Area Calculations
# -----------------------------
def nozzle_exit_area(p_c: float, p_e: float, A_t: float) -> float:
    """
    Computes nozzle exit area from isentropic area ratio.
    Based on notebook nozzle geometry calculations.
    
    Parameters:
        p_c: Chamber pressure [Pa]
        p_e: Exit pressure [Pa]
        A_t: Throat area [m²]
    
    Returns:
        Exit area [m²]
    """
    if p_c <= p_e or (GAMMA - 1) == 0:
        return A_t
    
    # Isentropic area ratio formula
    pressure_ratio = p_e / p_c
    term1 = (2 / (GAMMA + 1)) ** ((GAMMA + 1) / (2 * (GAMMA - 1)))
    term2 = (pressure_ratio) ** (1 / GAMMA)
    term3 = np.sqrt((2 / (GAMMA - 1)) * (1 - pressure_ratio ** ((GAMMA - 1) / GAMMA)))
    
    denominator = term1 * term2 * term3
    
    if denominator <= 0:
        return A_t
    
    return A_t / denominator


# -----------------------------
# Legacy Functions (for compatibility with existing solver)
# -----------------------------
def thrust(mdot_total: float, Ve: float = 1800.0, pe: float = P_AMBIENT, pa: float = P_AMBIENT, Ae: float = 1e-4) -> float:
    """
    Legacy thrust function with fixed parameters (notebook compatibility).
    EXACT implementation from notebook fixed nozzle parameters.
    """
    return mdot_total * Ve + (pe - pa) * Ae