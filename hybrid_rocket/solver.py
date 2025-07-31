"""
Time‐stepping or ODE‐based burn simulation.
"""

import numpy as np
from .regression import regression_rate
from .geometry import update_port_radius, port_area
from .constants import INITIAL_PORT_RADIUS

def simulate_burn(time_span: float, dt: float, mass_flux: float):
    """
    Simulate the burn over a given time span.

    Parameters
    ----------
    time_span : float
        Total simulation time (s).
    dt : float
        Time step (s).
    mass_flux : float
        Oxidizer mass flux (kg/m²/s).

    Returns
    -------
    times : np.ndarray
    radii : np.ndarray
    areas : np.ndarray
    """
    steps = int(time_span / dt) + 1
    times = np.linspace(0, time_span, steps)
    radii = np.zeros(steps)
    areas = np.zeros(steps)

    radius = INITIAL_PORT_RADIUS
    for i, t in enumerate(times):
        rate = regression_rate(mass_flux)
        areas[i] = port_area(radius)
        radii[i] = radius
        radius = update_port_radius(radius, rate, dt)

    return times, radii, areas
