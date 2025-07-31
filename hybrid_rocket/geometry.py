'''
geometry.py

Geometric calculations for port, chamber, casing, insulation, and nozzle.
Directly migrated from integrated_code_HRM(4)_omn.ipynb
'''

import numpy as np


def port_area(radius: float) -> float:
    """
    Cross-sectional area of the port.
    """
    return np.pi * radius**2


def update_port_radius(radius: float, rate: float, dt: float) -> float:
    """
    Increment port radius based on regression rate and timestep.
    """
    return radius + rate * dt


def grain_volume(r1: float, r2: float, length: float) -> float:
    """
    Volume of cylindrical grain segment.
    r1 and r2 in meters.
    """
    return np.pi * (r2**2 - r1**2) * length


def insulation_outer_radius(inner_radius: float, thickness: float) -> float:
    """
    Computes outer radius of insulation.
    """
    return inner_radius + thickness


def casing_outer_diameter(inner_diameter: float, wall_thickness: float) -> float:
    """
    Computes casing OD from ID and wall thickness.
    """
    return inner_diameter + 2 * wall_thickness


def nozzle_profile_coords(L_conv, throat_len, L_div, r_inlet, r_throat, r_exit):
    """
    Returns X and Y coordinates for the nozzle inner wall contour.
    All lengths in meters.
    """
    x = np.array([0, L_conv, L_conv + throat_len, L_conv + throat_len + L_div])
    y = np.array([r_inlet, r_throat, r_throat, r_exit])
    return x, y
