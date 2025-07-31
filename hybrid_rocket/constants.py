'''
constants.py

Global physical and propellant constants for Hybrid Rocket Simulation
Extracted directly from integrated_code_HRM(4)_omn.ipynb
'''

# Physics constants
GRAVITY = 9.80665            # m/s^2
R_UNIVERSAL = 8.3144621      # J/(mol*K)

# Regression rate constants (r = a * G^n)
REG_A = 0.0005               # m/s/(kg/m^2/s)^n
REG_N = 0.5                  # dimensionless exponent

# N2O properties
N2O_MOLAR_MASS = 44.013      # g/mol
N2O_TANK_PRESSURE = 7e6      # Pa (nominal tank pressure)

# Nozzle geometry defaults
THROAT_DIAMETER = 0.015      # m
EXIT_DIAMETER = 0.03         # m

# Chamber geometry defaults
INITIAL_PORT_RADIUS = 0.02   # m
CHAMBER_LENGTH = 0.5         # m
