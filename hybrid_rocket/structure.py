'''
structure.py

Calculates mass and pressure capacity of structural components.
Extracted from integrated_code_HRM(4)_omn.ipynb.
'''

import numpy as np
from .material_db import get_material_properties
from .geometry import grain_volume
from .constants import GRAVITY


def mass_cylinder(d_outer: float, length: float, thickness: float, material: str) -> float:
    '''
    Mass of cylindrical shell (without caps).
    '''
    d_inner = d_outer - 2 * thickness
    volume = np.pi * (d_outer**2 - d_inner**2) / 4 * length
    rho = get_material_properties(material)['rho']
    return volume * rho


def mass_solid_cylinder(d: float, length: float, material: str) -> float:
    '''
    Mass of a solid cylinder (for end caps, retainer, etc.).
    '''
    volume = np.pi * (d / 2)**2 * length
    rho = get_material_properties(material)['rho']
    return volume * rho


def allowable_pressure(t: float, r_inner: float, material: str, safety_factor: float) -> float:
    '''
    Calculates maximum internal pressure a cylinder can tolerate.
    Based on thin-walled pressure vessel theory.
    '''
    sigma_y = get_material_properties(material)['sigma_y']
    return (sigma_y / (2 * safety_factor)) * t / (r_inner + 0.6 * t)


def fuel_mass_from_geometry(r1: float, r2: float, L_grain: float, rho_fuel: float) -> float:
    '''
    Fuel mass given geometric dimensions and density.
    '''
    vol = grain_volume(r1, r2, L_grain)
    return vol * rho_fuel


def total_motor_structure_mass(components: dict) -> float:
    '''
    Sum all component masses.
    '''
    return sum(components.values())


def bolt_tensile_capacity(d_bolt: float, n_bolts: int, material: str, safety_factor: float) -> float:
    """
    Calculates total axial load capacity of all bolts.
    Assumes circular cross section with tensile stress area.

    Parameters
    ----------
    d_bolt : float
        Nominal diameter of bolt (m).
    n_bolts : int
        Number of bolts.
    material : str
        Bolt material.
    safety_factor : float
        Design safety factor.

    Returns
    -------
    float
        Maximum total load bolts can withstand (N).
    """
    A_t = np.pi * (d_bolt / 2)**2
    sigma_y = get_material_properties(material)['sigma_y']
    return (sigma_y / safety_factor) * A_t * n_bolts
