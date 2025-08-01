"""
structure.py

Calculates mass and pressure capacity of structural components.
Extracted from integrated_code_HRM(4)_omn.ipynb (top-cell version only).
"""

import numpy as np
from .material_db import get_material_properties
from .geometry import grain_volume
from .constants import GRAVITY


def mass_cylinder(d_outer: float, length: float, thickness: float, material: str) -> float:
    """
    Computes mass of a cylindrical shell (hollow tube without caps).

    Parameters:
        d_outer : float
            Outer diameter (m)
        length : float
            Length of cylinder (m)
        thickness : float
            Wall thickness (m)
        material : str
            Material name

    Returns:
        float : Mass in kg
    """
    d_inner = d_outer - 2 * thickness
    volume = np.pi * (d_outer**2 - d_inner**2) / 4 * length
    rho = get_material_properties(material)['rho']
    return volume * rho


def mass_solid_cylinder(d: float, length: float, material: str) -> float:
    """
    Computes mass of a solid cylindrical component.

    Parameters:
        d : float
            Diameter (m)
        length : float
            Length (m)
        material : str
            Material name

    Returns:
        float : Mass in kg
    """
    volume = np.pi * (d / 2)**2 * length
    rho = get_material_properties(material)['rho']
    return volume * rho


def allowable_pressure(t: float, r_inner: float, material: str, safety_factor: float) -> float:
    """
    Computes max allowable internal pressure for a thin-walled pressure vessel.

    Parameters:
        t : float
            Wall thickness (m)
        r_inner : float
            Inner radius (m)
        material : str
            Material name
        safety_factor : float
            Safety factor (dimensionless)

    Returns:
        float : Allowable pressure (Pa)
    """
    sigma_y = get_material_properties(material)['sigma_y']
    return (sigma_y / (2 * safety_factor)) * t / (r_inner + 0.6 * t)


def fuel_mass_from_geometry(r1: float, r2: float, L_grain: float, rho_fuel: float) -> float:
    """
    Calculates fuel mass from port radius, outer radius, and length.

    Parameters:
        r1 : float
            Inner port radius (m)
        r2 : float
            Outer fuel radius (m)
        L_grain : float
            Grain length (m)
        rho_fuel : float
            Fuel density (kg/m³)

    Returns:
        float : Fuel mass (kg)
    """
    vol = grain_volume(r1, r2, L_grain)
    return vol * rho_fuel


def total_motor_structure_mass(components: dict) -> float:
    """
    Sums the masses of all structural components.

    Parameters:
        components : dict
            Dictionary of {component_name: mass}

    Returns:
        float : Total structural mass (kg)
    """
    return sum(components.values())


def bolt_tensile_capacity(d_bolt: float, n_bolts: int, material: str, safety_factor: float) -> float:
    """
    Calculates total axial tensile load capacity of multiple bolts.

    Parameters:
        d_bolt : float
            Nominal diameter of a bolt (m)
        n_bolts : int
            Number of bolts
        material : str
            Bolt material
        safety_factor : float
            Design safety factor

    Returns:
        float : Maximum load capacity (N)
    """
    A_t = np.pi * (d_bolt / 2)**2
    sigma_y = get_material_properties(material)['sigma_y']
    return (sigma_y / safety_factor) * A_t * n_bolts
