"""
Regression rate calculations for hybrid rocket port.
"""

import numpy as np
from .constants import REG_A, REG_N

def regression_rate(oxidizer_mass_flux: float) -> float:
    """
    Compute the fuel port regression rate r = a * G^n.

    Parameters
    ----------
    oxidizer_mass_flux : float
        Oxidizer mass flux (kg/m²/s).

    Returns
    -------
    float
        Regression rate in m/s.
    """
    return REG_A * oxidizer_mass_flux**REG_N
