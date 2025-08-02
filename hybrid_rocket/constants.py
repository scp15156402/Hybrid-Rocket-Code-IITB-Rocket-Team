# hybrid_rocket/constants.py

"""
constants.py

Global physical and propellant constants for Hybrid Rocket Simulation.
EXACT implementation from integrated_code_HRM(4)_omn.ipynb notebook.
"""

import numpy as np
from scipy.interpolate import CubicSpline

# -----------------------------
# Universal Physical Constants
# -----------------------------
GRAVITY = 9.81                  # m/s², gravitational acceleration (notebook: g = 9.81)
R_UNIVERSAL = 8.314             # J/(mol·K), universal gas constant (notebook: R_univ = 8.314)

# -----------------------------
# Combustion Gas Properties  
# -----------------------------
GAMMA = 1.33                    # Specific heat ratio (notebook: k = 1.33)
M_EXHAUST = 0.02897            # Default molar mass of exhaust (kg/mol) (notebook: M = 0.02897)
R_SPECIFIC = R_UNIVERSAL / M_EXHAUST  # Specific gas constant for exhaust [J/(kg·K)]
P_AMBIENT = 1e5                # Pa, ambient pressure (notebook: p_ambient = 1e5)

# -----------------------------
# Propellant / Regression Constants
# -----------------------------
REG_A = 0.1561e-3              # Regression rate coefficient a [m/s / (kg/m²/s)^n] (notebook: a = 0.1561e-3)
REG_N = 0.5                    # Regression rate exponent n (notebook: n = 0.5)

# -----------------------------
# Material Densities
# -----------------------------
RHO_FUEL = 900                 # Paraffin fuel density (kg/m³) (notebook: rho_fuel = 900)
RHO_GRAPHITE = 1800           # Graphite density for nozzle (kg/m³) (notebook: rho_graphite = 1800)

# -----------------------------
# N₂O Thermophysical Data (EXACT from notebook)
# -----------------------------
# Temperature in Kelvin from notebook
N2O_TEMP_K = np.array([249,259,269,279,289,299,301,303,305,307,308,308.2,308.4,308.6,308.8,309,309.4])
# Pressure in bar from notebook
N2O_PRESSURES_BAR = np.array([15.847,21.308,28.025,36.168,45.936,57.591,60.181,62.870,65.663,68.573,70.078,70.384,70.691,71.000,71.311,71.623,72.255])
# Liquid density in kg/m³ from notebook
N2O_DENSITY_KG_M3 = np.array([1014.9,973.32,927.62,876.03,815.00,734.79,713.98,690.07,661.16,622.45,594.69,587.72,579.98,571.22,561.02,548.57,505.57])

# Convert temperature to Celsius for spline interpolation (EXACT notebook approach)
N2O_TEMP_C = N2O_TEMP_K - 273.15

# Create cubic spline interpolators (EXACT notebook implementation)
PRESSURE_SPLINE = CubicSpline(N2O_TEMP_C, N2O_PRESSURES_BAR)
DENSITY_SPLINE = CubicSpline(N2O_TEMP_C, N2O_DENSITY_KG_M3)

# -----------------------------
# Combustion Temperature vs O/F Data (EXACT from notebook)
# -----------------------------
OF_DATA = np.array([0.2, 1.0, 2.0, 3.0, 4.0, 6.0, 7.0, 8.0, 9.0, 10.0])
T_COMBUSTION_DATA = np.array([1000, 1210, 1500, 1800, 2400, 3100, 3200, 3260, 3250, 3200])

# -----------------------------
# Oxidizer (N₂O) Properties
# -----------------------------
N2O_MOLAR_MASS = 44.013        # g/mol
N2O_TANK_PRESSURE = 7e6        # Pa, nominal oxidizer tank pressure (70 bar)

# -----------------------------
# Default Nozzle Geometry (used as fallback)
# -----------------------------
THROAT_DIAMETER = 0.006        # m, default nozzle throat diameter (6mm from notebook)
EXIT_DIAMETER = 0.012          # m, estimated nozzle exit diameter

# -----------------------------
# Default Combustion Chamber Geometry (used as fallback)
# -----------------------------
INITIAL_PORT_RADIUS = 0.007    # m, initial port radius (0.7 cm from notebook)
FINAL_PORT_RADIUS = 0.019      # m, final port radius (1.9 cm from notebook)
CHAMBER_LENGTH = 0.06          # m, grain length (6 cm from notebook)

# -----------------------------
# Bolt Analysis Constants (EXACT from notebook)
# -----------------------------
BOLT_YIELD_STRENGTH = 660e6        # Pa, typical bolt yield strength (notebook: bolt_yield_strength_typical = 660e6)
BOLT_SHEAR_YIELD_RATIO = 0.6       # Shear to tensile yield ratio (notebook: bolt_shear_yield_ratio = 0.6)
BOLT_SAFETY_FACTOR = 3.0           # Safety factor for bolts (notebook: bolt_safety_factor = 3.0)
ALLOWABLE_BOLT_SHEAR_STRESS = (BOLT_YIELD_STRENGTH * BOLT_SHEAR_YIELD_RATIO) / BOLT_SAFETY_FACTOR