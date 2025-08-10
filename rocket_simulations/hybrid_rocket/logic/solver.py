"""
solver.py

Main simulation engine with full notebook implementation.
EXACT implementation from integrated_code_HRM(4)_omn.ipynb.
Includes dynamic chamber pressure, N₂O tank modeling, and all missing features.
"""

import numpy as np
import numpy as np

from rocket_simulations.hybrid_rocket.logic.geometry import port_area, update_port_radius
from rocket_simulations.hybrid_rocket.logic.combustion import (
    regression_rate, oxidizer_flux, fuel_mass_flow_rate, of_ratio,
    get_Tc, solve_choked_pressure, exhaust_velocity, thrust_from_momentum, specific_impulse,
    n2o_liquid_density, nozzle_exit_area
)
from rocket_simulations.hybrid_rocket.data.constants import (
    GRAVITY, R_SPECIFIC, GAMMA, P_AMBIENT, RHO_FUEL
)



def simulate_burn(
    r1: float,
    r2: float,
    L: float,
    mdot_ox: float,
    rho_fuel: float,
    current_values: dict = None
) -> dict:
    """
    Simulates hybrid rocket motor burn with EXACT notebook implementation.
    Includes dynamic chamber pressure, N₂O tank modeling, and oxidizer depletion checks.

    Parameters:
        r1 (float): Initial port radius (cm)
        r2 (float): Final port radius (cm)
        L (float): Grain length (cm)
        mdot_ox (float): Oxidizer mass flow rate (g/s)
        rho_fuel (float): Fuel density (kg/m³)
        current_values (dict): UI parameter values for advanced calculations

    Returns:
        dict: Time-series results including pressure and temperature histories
    """
    # --- Convert inputs to SI units (EXACT notebook conversion) ---
    r      = r1 / 100.0               # cm → m
    r_max  = r2 / 100.0               # cm → m
    L_m    = L  / 100.0               # cm → m
    mdot_ox_si = mdot_ox / 1000.0     # g/s → kg/s

    # --- Time stepping parameters (EXACT notebook: dt = 0.001) ---
    t  = 0.0
    dt = 0.001  # Notebook uses finer timestep than app default

    # --- N₂O Tank Modeling (EXACT notebook implementation) ---
    if current_values is not None:
        # Oxidizer tank calculations (EXACT notebook)
        ox_tank_D_outer = current_values["ox_tank_outer_diameter"] / 100.0  # cm -> m
        ox_tank_t = current_values["ox_tank_wall_thk"] / 1000.0  # mm -> m
        ox_tank_L = current_values["ox_tank_length"] / 100.0  # cm -> m
        ox_tank_D_inner = ox_tank_D_outer - 2 * ox_tank_t
        ox_tank_V_inner = np.pi * (ox_tank_D_inner / 2)**2 * ox_tank_L
        ox_tank_V_available = 0.8 * ox_tank_V_inner  # 80% ullage (notebook)
        
        # N₂O liquid density at tank temperature (EXACT notebook)
        # Clamp °C to the spline’s valid domain (~–24.15 °C to +36.25 °C)
        temp_c = current_values.get("ox_tank_temp", 25.0)
        temp_c = max(min(temp_c,  36.25), -24.15)
        rho_n2o = n2o_liquid_density(temp_c)
        mox_available = ox_tank_V_available * rho_n2o

        
        # Throat area for chamber pressure calculation
        throat_d_mm = current_values.get("throat_diameter", 6.0)
        A_t = np.pi * (throat_d_mm / 2000.0)**2  # mm -> m radius
        
        use_advanced_model = True
    else:
        # Fallback for basic simulation
        mox_available = 1000.0  # Large value to prevent early termination
        A_t = np.pi * (0.003)**2  # Default 6mm throat
        use_advanced_model = False

    # --- Histories (EXACT notebook variables) ---
    time_hist = []
    radius_hist = []
    thrust_hist = []
    of_hist = []
    G_ox_hist = []
    isp_hist = []
    Tc_hist = []      # Combustion temperature (NEW)
    p_c_hist = []     # Chamber pressure (NEW)
    r_dot_hist = []   # Regression rate history
    
    # --- Tracking variables (EXACT notebook) ---
    mox_used = 0.0
    mfuel_used = 0.0
    low_pressure_warning = False
    last_p_c = P_AMBIENT

    # --- Main burn loop (EXACT notebook conditions) ---
    while (r < r_max) and (mox_used < mox_available * 0.90):  # Notebook: 90% oxidizer limit
        
        # Port area & oxidizer flux (EXACT notebook)
        A_port = port_area(r)
        G = oxidizer_flux(mdot_ox_si, A_port)

        # Fuel regression & mass flow (EXACT notebook)
        r_dot = regression_rate(G)
        mdot_fuel = fuel_mass_flow_rate(r_dot, rho_fuel, r, L_m)

        # Total flow & mixture ratio (EXACT notebook)
        mdot_total = mdot_ox_si + mdot_fuel
        OF = of_ratio(mdot_ox_si, mdot_fuel)

        # Combustion temperature (EXACT notebook)
        Tc = get_Tc(OF)
        
        if use_advanced_model:
            # Chamber pressure via choked flow (EXACT notebook)
            p_c = solve_choked_pressure(mdot_total, A_t, R_SPECIFIC, Tc)
            
            # Low pressure warning (EXACT notebook)
            if p_c < 2e5:  # 2 bar threshold from notebook
                low_pressure_warning = True
            
            # Exhaust velocity from isentropic expansion (EXACT notebook)
            v_e = exhaust_velocity(p_c, Tc, P_AMBIENT)
            
            # Thrust calculation (EXACT notebook)
            T = thrust_from_momentum(mdot_total, v_e)
            
            # Specific impulse calculation
            Isp = specific_impulse(T, mdot_total)
            
        else:
            # Fallback to simple model for compatibility
            p_c = 10e5  # Assume 10 bar
            T = mdot_total * 1800.0  # Fixed exhaust velocity
            Isp = T / (mdot_total * GRAVITY) if mdot_total > 0 else 0.0

        # Record histories (EXACT notebook)
        time_hist.append(t)
        thrust_hist.append(T)
        of_hist.append(OF)
        radius_hist.append(r)  # only once
        Tc_hist.append(Tc)
        G_ox_hist.append(G)
        r_dot_hist.append(r_dot)
        p_c_hist.append(p_c)
        isp_hist.append(Isp)

        # Update state (EXACT notebook)
        dr = r_dot * dt
        t += dt
        mox_used += mdot_ox_si * dt
        mfuel_used += mdot_fuel * dt
        r += dr
        last_p_c = p_c

    # --- Determine stopping reason (EXACT notebook logic) ---
    if mox_used >= mox_available * 0.90:
        stop_reason = "Reached 90% oxidizer consumption"
    elif r >= r_max:
        stop_reason = "Reached end of fuel grain"
    else:
        stop_reason = "Simulation completed"

    # --- Return results with all histories (EXACT notebook) ---
    results = {
        "time": np.array(time_hist),
        "radius": np.array(radius_hist),
        "thrust": np.array(thrust_hist),
        "of": np.array(of_hist),
        "G_ox": np.array(G_ox_hist),
        "isp": np.array(isp_hist),
        "Tc": np.array(Tc_hist),
        "p_c": np.array(p_c_hist),
        "r_dot": np.array(r_dot_hist),
        "stop_reason": stop_reason,
        "mox_used": mox_used,
        "mfuel_used": mfuel_used,
        "low_pressure_warning": low_pressure_warning
    }

    return results


def simulate_burn_legacy(
    r1: float,
    r2: float,
    L: float,
    mdot_ox: float,
    rho_fuel: float
) -> dict:
    """
    Legacy simulation function for backward compatibility.
    Calls the enhanced simulate_burn with simplified parameters.
    """
    return simulate_burn(r1, r2, L, mdot_ox, rho_fuel, current_values=None)
