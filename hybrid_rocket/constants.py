"""
constants.py

Global physical and propellant constants for Hybrid Rocket Simulation.
Extracted directly from integrated_code_HRM(4)_omn.ipynb.
"""

# -----------------------------
# Universal Physical Constants
# -----------------------------
GRAVITY = 9.80665               # m/s², standard gravity
R_UNIVERSAL = 8.3144621         # J/(mol·K), universal gas constant

# -----------------------------
# Propellant / Combustion Constants
# -----------------------------
REG_A = 0.0005                  # Regression rate coefficient a [m/s / (kg/m²/s)^n]
REG_N = 0.5                     # Regression rate exponent n

# -----------------------------
# Oxidizer (N₂O) Properties
# -----------------------------
N2O_MOLAR_MASS = 44.013         # g/mol
N2O_TANK_PRESSURE = 7e6         # Pa, nominal oxidizer tank pressure (70 bar)

# -----------------------------
# Default Nozzle Geometry (used as fallback)
# -----------------------------
THROAT_DIAMETER = 0.015         # m, nozzle throat diameter
EXIT_DIAMETER = 0.03            # m, nozzle exit diameter

# -----------------------------
# Default Combustion Chamber Geometry (used as fallback)
# -----------------------------
INITIAL_PORT_RADIUS = 0.02      # m, initial port radius of fuel grain
CHAMBER_LENGTH = 0.5            # m, grain length / combustion chamber length
