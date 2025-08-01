"""
geometry.py

Geometric calculations for port, chamber, casing, insulation, and nozzle profiles.
Directly migrated and cleaned up from integrated_code_HRM(4)_omn.ipynb.
"""

import numpy as np


def port_area(radius: float) -> float:
    """
    Computes cross-sectional area of the port.

    Parameters:
        radius : float
            Port radius (m)

    Returns:
        float : Port area (m²)
    """
    return np.pi * radius**2


def update_port_radius(radius: float, rate: float, dt: float) -> float:
    """
    Updates port radius over one timestep based on regression rate.

    Parameters:
        radius : float
            Current port radius (m)
        rate : float
            Regression rate (m/s)
        dt : float
            Time step (s)

    Returns:
        float : Updated port radius (m)
    """
    return radius + rate * dt


def grain_volume(r1: float, r2: float, length: float) -> float:
    """
    Computes volume of fuel grain as a cylindrical shell.

    Parameters:
        r1 : float
            Initial port radius (m)
        r2 : float
            Outer fuel radius (m)
        length : float
            Grain length (m)

    Returns:
        float : Grain volume (m³)
    """
    return np.pi * (r2**2 - r1**2) * length


def insulation_outer_radius(inner_radius: float, thickness: float) -> float:
    """
    Computes outer radius of insulation.

    Parameters:
        inner_radius : float
            Inner radius before insulation (m)
        thickness : float
            Insulation thickness (m)

    Returns:
        float : Outer radius after insulation (m)
    """
    return inner_radius + thickness


def casing_outer_diameter(inner_diameter: float, wall_thickness: float) -> float:
    """
    Computes outer diameter of casing from inner diameter and wall thickness.

    Parameters:
        inner_diameter : float
            Inner diameter of casing (m)
        wall_thickness : float
            Wall thickness (m)

    Returns:
        float : Outer diameter of casing (m)
    """
    return inner_diameter + 2 * wall_thickness


def nozzle_profile_coords(
    L_conv: float,
    throat_len: float,
    L_div: float,
    r_inlet: float,
    r_throat: float,
    r_exit: float
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generates 2D profile coordinates of the nozzle for plotting.

    Parameters:
        L_conv : float
            Converging section length (m)
        throat_len : float
            Throat section length (m)
        L_div : float
            Diverging section length (m)
        r_inlet : float
            Inlet radius (m)
        r_throat : float
            Throat radius (m)
        r_exit : float
            Exit radius (m)

    Returns:
        tuple of np.ndarray:
            (x_coords, y_coords) defining the nozzle contour
    """
    x = np.array([0, L_conv, L_conv + throat_len, L_conv + throat_len + L_div])
    y = np.array([r_inlet, r_throat, r_throat, r_exit])
    return x, y


def burning_surface_area(port_radius: float, grain_length: float) -> float:
    """
    Computes lateral burning surface area of the grain.

    Parameters:
        port_radius : float
            Current port radius (m)
        grain_length : float
            Grain length (m)

    Returns:
        float : Surface area (m²)
    """
    return 2 * np.pi * port_radius * grain_length


def total_motor_length(
    precomb: float,
    grain_len: float,
    postcomb: float,
    front_cap: float,
    retainer: float,
    tank_len: float,
    gap: float = 0.0
) -> float:
    """
    Computes total axial length of the motor-tank assembly.

    Parameters:
        precomb : float
            Pre-combustion section length (m)
        grain_len : float
            Grain length (m)
        postcomb : float
            Post-combustion section length (m)
        front_cap : float
            Front cap length (m)
        retainer : float
            Nozzle retainer length (m)
        tank_len : float
            Oxidizer tank length (m)
        gap : float, optional
            Motor-to-tank axial gap (m) [default: 0.0]

    Returns:
        float : Total length (m)
    """
    return precomb + grain_len + postcomb + front_cap + retainer + tank_len + gap
