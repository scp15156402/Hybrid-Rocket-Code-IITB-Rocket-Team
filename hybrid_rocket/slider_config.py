# hybrid_rocket/slider_config.py

slider_config = {
    "mdot_ox":   {"label": "Oxidizer Mass Flow Rate (kg/s)", "min": 0.01, "max": 1.0, "step": 0.01, "default": 0.05},
    "rho_fuel":  {"label": "Fuel Density (kg/m³)", "min": 500, "max": 1500, "step": 10, "default": 930},
    "r1":        {"label": "Initial Port Radius (m)", "min": 0.005, "max": 0.05, "step": 0.001, "default": 0.01},
    "L":         {"label": "Grain Length (m)", "min": 0.05, "max": 0.5, "step": 0.01, "default": 0.1},
    "dt":        {"label": "Time Step (s)", "min": 0.001, "max": 0.1, "step": 0.001, "default": 0.01},
    "t_final":   {"label": "Burn Time (s)", "min": 1.0, "max": 10.0, "step": 0.1, "default": 3.0},
    "Ve":        {"label": "Exit Velocity (m/s)", "min": 1000, "max": 3000, "step": 10, "default": 1800},
    "pe":        {"label": "Exit Pressure (Pa)", "min": 90000, "max": 110000, "step": 500, "default": 100000},
    "pa":        {"label": "Ambient Pressure (Pa)", "min": 90000, "max": 110000, "step": 500, "default": 100000},
    "Ae":        {"label": "Nozzle Exit Area (m²)", "min": 1e-5, "max": 1e-3, "step": 1e-5, "default": 1e-4}
}
