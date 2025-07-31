"""
All physical and propellant constants go here.
"""

# Physics constants
GRAVITY = 9.80665            # m/s²
R_UNIVERSAL = 8.3144621      # J/(mol·K)

# Propellant / regression rate constants
# Example: r = a * G**n
REG_A = 0.0005               # m/s/(kg/m²/s)^n
REG_N = 0.5                  # dimensionless exponent

# N₂O properties
N2O_MOLAR_MASS = 44.013      # g/mol
N2O_TANK_PRESSURE = 7e6      # Pa

# Nozzle geometry defaults
THROAT_DIAMETER = 0.015      # m
EXIT_DIAMETER = 0.03         # m

# Chamber geometry
INITIAL_PORT_RADIUS = 0.02   # m
CHAMBER_LENGTH = 0.5         # m
