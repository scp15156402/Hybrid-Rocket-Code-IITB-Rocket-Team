"""
Geometry and burn-surface evolution logic.
"""

import numpy as np

def port_area(radius: float) -> float:
    """
    Cross-sectional area of the fuel port.

    Parameters
    ----------
    radius : float
        Port radius in meters.

    Returns
    -------
    float
        Area in m².
    """
    return np.pi * radius**2

def update_port_radius(radius: float, rate: float, dt: float) -> float:
    """
    Step the port radius forward by regression rate.

    Parameters
    ----------
    radius : float
        Current port radius (m).
    rate : float
        Regression rate (m/s).
    dt : float
        Timestep (s).

    Returns
    -------
    float
        Updated port radius.
    """
    return radius + rate * dt
