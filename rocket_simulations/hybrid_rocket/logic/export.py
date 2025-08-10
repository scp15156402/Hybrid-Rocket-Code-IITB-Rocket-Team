# hybrid_rocket/export.py

"""
export.py

Enhanced result exports and comprehensive summaries.
EXACT implementation from integrated_code_HRM(4)_omn.ipynb notebook.
Includes structural analysis, propellant consumption, and all missing metrics.
"""

import pandas as pd
import numpy as np
from hybrid_rocket.constants import GRAVITY
from hybrid_rocket.structure import fuel_mass_from_geometry
from hybrid_rocket.combustion import n2o_liquid_density, n2o_pressure
from hybrid_rocket.material_db import get_material_properties


def export_simulation_data(results: dict, filename: str = "simulation_results.csv"):
    """
    Exports time-series data to CSV with all available metrics.
    Enhanced version including pressure and temperature data.
    """
    data_dict = {
        'Time (s)': results.get('time', []),
        'Thrust (N)': results.get('thrust', []),
        'Port Radius (m)': results.get('radius', []),
        'O/F Ratio': results.get('of', []),
        'Oxidizer Mass Flux (kg/m^2/s)': results.get('G_ox', []),
        'Specific Impulse (s)': results.get('isp', [])
    }

    # Only add if non-empty
    if len(results.get('Tc', [])) > 0:
        data_dict['Combustion Temperature (K)'] = results['Tc']

    if len(results.get('p_c', [])) > 0:
        data_dict['Chamber Pressure (Pa)'] = results['p_c']
        data_dict['Chamber Pressure (bar)'] = [pc / 1e5 for pc in results['p_c']]

    if len(results.get('r_dot', [])) > 0:
        data_dict['Regression Rate (m/s)'] = results['r_dot']

    df = pd.DataFrame(data_dict)
    df.to_csv(filename, index=False)
    print(f"[INFO] Exported enhanced simulation data to {filename}")


def compute_structural_metrics(current_values: dict, results: dict) -> dict:
    """
    Computes comprehensive structural analysis metrics.
    EXACT implementation from notebook structural calculations.
    """
    # Geometry conversions
    r2_fuel = current_values["r2"] / 100.0
    insul_gr = current_values["insul_grain_thk"] / 1000.0
    insul_pp = current_values["insul_prepost_thk"] / 1000.0
    L_grain = current_values["L"] / 100.0
    t_wall = current_values["casing_wall_thk"] / 1000.0

    # Casing
    inner_r = max(r2_fuel + insul_gr, r2_fuel + insul_pp)
    ID_casing = 2 * inner_r
    OD_casing = ID_casing + 2 * t_wall

    mat = get_material_properties(current_values["casing_material"])
    allowable = mat['sigma_y'] / (2 * current_values["safety_factor"])
    max_p_casing = allowable * t_wall / (inner_r + 0.6 * t_wall)

    # Masses
    L_front = current_values["frontcap_length"] / 1000.0
    L_ret = current_values["retainer_length"] / 1000.0
    r_ret = current_values["retainer_inner_radius"] / 1000.0

    vol_body = np.pi * (((inner_r + t_wall)**2 - inner_r**2) *
                       (L_grain +
                        current_values["pre_comb_len"] / 100.0 +
                        current_values["post_comb_len"] / 100.0))
    mass_body = vol_body * mat['rho']
    mass_front = np.pi * inner_r**2 * L_front * get_material_properties(
        current_values["frontcap_material"])['rho']
    mass_ret = np.pi * (inner_r**2 - r_ret**2) * L_ret * get_material_properties(
        current_values["retainer_material"])['rho']

    rho_graphite = 1800
    vol_nozzle = 0.5 * np.pi * inner_r**2 * 0.05
    mass_nozzle = vol_nozzle * rho_graphite

    # Tank
    D_out = current_values["ox_tank_outer_diameter"] / 100.0
    t_tank = current_values["ox_tank_wall_thk"] / 1000.0
    L_tank = current_values["ox_tank_length"] / 100.0
    D_in = D_out - 2 * t_tank

    mat_tank = get_material_properties(current_values["ox_tank_material"])
    allow_tank = mat_tank['sigma_y'] / (2 * current_values["ox_tank_safety_factor"])
    max_p_tank = allow_tank * t_tank / (D_in/2 + 0.6 * t_tank)

    SA = np.pi * D_out * L_tank
    mass_tank_shell = SA * t_tank * mat_tank['rho']

    cap_thk_f = current_values["ox_tank_frontcap_thk"] / 1000.0
    cap_thk_b = current_values["ox_tank_backcap_thk"] / 1000.0
    mass_tank_caps = np.pi * (D_in/2)**2 * (cap_thk_f + cap_thk_b) * mat_tank['rho']

    total_tank_mass = mass_tank_shell + mass_tank_caps

    # Propellant
    rho_n2o = n2o_liquid_density(current_values.get("ox_tank_temp", 25.0))
    V_avail = 0.8 * np.pi * (D_in/2)**2 * L_tank
    m_ox = V_avail * rho_n2o

    r1 = current_values["r1"] / 100.0
    m_fuel = fuel_mass_from_geometry(r1, r2_fuel, L_grain, current_values["rho_fuel"])

    m_struct = mass_body + mass_front + mass_ret + mass_nozzle
    total_m = m_struct + total_tank_mass + m_ox + m_fuel
    twr = (np.max(results.get('thrust', [0])) / (total_m * GRAVITY)) if total_m > 0 else 0

    return {
        'casing_inner_diameter':       ID_casing,
        'casing_outer_diameter':       OD_casing,
        'max_pressure_design_casing':  max_p_casing,
        'mass_casing_body':            mass_body,
        'mass_frontcap':               mass_front,
        'mass_retainer':               mass_ret,
        'mass_nozzle':                 mass_nozzle,
        'total_motor_structure_mass':  m_struct,
        'total_ox_tank_mass':          total_tank_mass,
        'mox_available':               m_ox,
        'mfuel_geom':                  m_fuel,
        'total_mass':                  total_m,
        'total_weight':                total_m * GRAVITY,
        'thrust_to_weight_ratio':      twr,
        'max_pressure_design_ox_tank': max_p_tank,
        'n2o_vapor_pressure':          n2o_pressure(current_values.get("ox_tank_temp", 25.0)) * 1e5,
        'tank_temperature':            current_values.get("ox_tank_temp", 25.0),
    }


def get_summary_dict(results: dict, current_values: dict = None) -> dict:
    """
    Builds and returns a nested dict of all summary sections and their formatted values.
    Wraps each section in try/except so you can see exactly which block failed.
    """
    summary = {}
    fmt = lambda v, u: f"{v:.2f} {u}".strip()

    def safe_section(name, func):
        try:
            summary[name] = func()
        except Exception as e:
            summary[name] = {"ERROR": str(e)}

    # 1) pull arrays into numpy (all tests by .size)
    try:
        t      = np.array(results.get('time', []))
        thrust = np.array(results.get('thrust', []))
        radius = np.array(results.get('radius', []))
        of     = np.array(results.get('of', []))
        gox    = np.array(results.get('G_ox', []))
        isp    = np.array(results.get('isp', np.full_like(t, np.nan)))
        Tc     = np.array(results.get('Tc', []))
        p_c    = np.array(results.get('p_c', []))
    except Exception as e:
        return {
            "ERROR INITIALIZING ARRAYS": {
                "ERROR": str(e),
                "Advice": "Check that `results` contains valid lists"
            }
        }

    # 2) Time & Burn Geometry
    safe_section("Time & Burn Geometry", lambda: {
        "Burn Time":           fmt(t[-1], "s"),
        "Initial Port Radius": fmt(radius[0], "m"),
        "Final Port Radius":   fmt(radius[-1], "m"),
        "Δ Port Radius":       fmt(radius[-1] - radius[0], "m"),
    } if (t.size > 0 and radius.size > 0) else {})

    # 3) Thrust Characteristics
    safe_section("Thrust Characteristics", lambda: {
        **({
            "Total Impulse":  fmt(np.trapz(thrust, t), "Ns"),
            "Average Thrust": fmt(np.mean(thrust), "N"),
            "Peak Thrust":    fmt(np.max(thrust), "N"),
            "Minimum Thrust": fmt(np.min(thrust), "N"),
        } if thrust.size > 0 else {})
    })

    # 4) Specific Impulse (Isp)
    safe_section("Specific Impulse (Isp)", lambda: {
        **({
            "Average Isp": fmt(np.nanmean(isp), "s"),
            "Max Isp":     fmt(np.nanmax(isp), "s"),
            "Min Isp":     fmt(np.nanmin(isp), "s"),
        } if isp.size > 0 else {})
    })

    # 5) Oxidizer-to-Fuel Ratio (O/F)
    safe_section("Oxidizer-to-Fuel Ratio (O/F)", lambda: {
        **({
            "Average O/F Ratio": fmt(np.mean(of), ""),
            "Max O/F Ratio":     fmt(np.max(of), ""),
            "Min O/F Ratio":     fmt(np.min(of), ""),
        } if of.size > 0 else {})
    })

    # 6) Oxidizer Mass Flux (G_ox)
    safe_section("Oxidizer Mass Flux (G_ox)", lambda: {
        **({
            "Average G_ox": fmt(np.mean(gox), "kg/m²/s"),
            "Max G_ox":     fmt(np.max(gox), "kg/m²/s"),
            "Min G_ox":     fmt(np.min(gox), "kg/m²/s"),
        } if gox.size > 0 else {})
    })

    # 7) Combustion Chamber
    safe_section("Combustion Chamber", lambda: {
        **({
            "Peak Combustion Temp":    fmt(np.max(Tc), "K"),
            "Average Combustion Temp": fmt(np.mean(Tc), "K"),
        } if Tc.size > 0 else {})
    })

    # 8) Chamber Pressure
    safe_section("Chamber Pressure", lambda: {
        **({
            "Peak Chamber Pressure":  fmt(np.max(p_c)/1e5, "bar"),
            "Final Chamber Pressure": fmt(p_c[-1]/1e5, "bar"),
        } if p_c.size > 0 else {})
    })

    # 9) Propellant / Structure / Tank
    if current_values is not None:
        safe_section("Propellant Consumption", lambda: {
            "Total Oxidizer Available": fmt(
                compute_structural_metrics(current_values, results)['mox_available'], "kg"
            ),
            "Total Fuel Available": fmt(
                compute_structural_metrics(current_values, results)['mfuel_geom'], "kg"
            ),
            **({"Oxidizer Consumed": fmt(results['mox_used'], "kg")} if 'mox_used' in results else {}),
            **({"Fuel Consumed":     fmt(results['mfuel_used'], "kg")} if 'mfuel_used' in results else {}),
        })

        safe_section("Structural Analysis", lambda: {
            **{
                k.replace('_', ' ').title():
                    (fmt(v, 'kg') if isinstance(v, (int, float)) else v)
                for k, v in compute_structural_metrics(current_values, results).items()
            }
        })

        safe_section("Oxidizer Tank", lambda: {
            "Tank Temperature": fmt(
                compute_structural_metrics(current_values, results)['tank_temperature'], "°C"
            ),
            "Max Tank Pressure": fmt(
                compute_structural_metrics(current_values, results)['max_pressure_design_ox_tank']/1e5,
                "bar"
            ),
            "N₂O Vapor Pressure": fmt(
                compute_structural_metrics(current_values, results)['n2o_vapor_pressure']/1e5,
                "bar"
            ),
            "Tank Mass": fmt(
                compute_structural_metrics(current_values, results)['total_ox_tank_mass'],
                "kg"
            ),
        })

    return summary
