# hybrid_rocket/slider_config.py

slider_config = {
    # I. Combustion Geometry & Fuel Parameters
    "r1":        {"label": "Initial Port Radius r1 (cm)",            "min": 0.1,  "max": 5.0,   "step": 0.1,  "default": 0.7},
    "r2":        {"label": "Final Port Radius r2 (cm)",              "min": 0.5,  "max": 5.0,   "step": 0.1,  "default": 1.9},
    "L":         {"label": "Grain Length (cm)",                      "min": 1.0,  "max": 30.0,  "step": 0.5,  "default": 6.0},
    "mdot_ox":   {"label": "Oxidizer Mass Flow Rate (g/s)",          "min": 10.0, "max": 100.0, "step": 1.0,  "default": 47.0},
    "rho_fuel":  {"label": "Fuel Density (kg/m³)",                   "min": 500.0,"max": 1500.0,"step": 10.0, "default": 930.0},

    # II. Casing & Insulation
    "safety_factor":      {"label": "Casing Safety Factor",              "min": 1.0,  "max": 4.0,   "step": 0.1,  "default": 2.0},
    "insul_grain_thk":    {"label": "Insulation Thickness (Grain, mm)",   "min": 0.0,  "max": 10.0,  "step": 0.1,  "default": 2.5},
    "insul_prepost_thk":  {"label": "Insulation Thickness (Pre/Post, mm)", "min": 0.0,  "max": 10.0,  "step": 0.1,  "default": 3.0},
    "casing_wall_thk":    {"label": "Casing Wall Thickness (mm)",          "min": 1.0,  "max": 10.0,  "step": 0.1,  "default": 3.0},
    "pre_comb_len":       {"label": "Pre-combustion Chamber Length (cm)",   "min": 0.5,  "max": 10.0,  "step": 0.1,  "default": 3.0},
    "post_comb_len":      {"label": "Post-combustion Chamber Length (cm)",  "min": 0.5,  "max": 10.0,  "step": 0.1,  "default": 3.0},

    # III. Nozzle Geometry
    "converge_half_angle":{"label": "Converge (°)",                       "min": 10.0, "max": 80.0,  "step": 1.0,  "default": 45.0},
    "throat_diameter":    {"label": "Throat D (mm)",                      "min": 1.0,  "max": 20.0,  "step": 0.1,  "default": 6.0},
    "throat_length":      {"label": "Throat Len (mm)",                    "min": 1.0,  "max": 20.0,  "step": 0.1,  "default": 7.0},
    "diverge_half_angle": {"label": "Diverge (°)",                        "min": 5.0,  "max": 45.0,  "step": 1.0,  "default": 15.0},

    # IV. Retainer & Front Cap
    "retainer_length":         {"label": "Retainer Len (mm)",          "min": 1.0,  "max": 50.0,  "step": 1.0,  "default": 10.0},
    "retainer_inner_radius":   {"label": "Retainer Inner R (mm)",      "min": 1.0,  "max": 50.0,  "step": 1.0,  "default": 20.0},
    "frontcap_length":         {"label": "Front Cap Len (mm)",         "min": 1.0,  "max": 50.0,  "step": 1.0,  "default": 20.0},

    # V. Front Cap Bolts
    "frontcap_bolt_diameter":  {"label": "Front Cap Bolt D (mm)",     "min": 1.0,  "max": 20.0,  "step": 1.0,  "default": 6.0},
    "frontcap_num_bolts":      {"label": "Front Cap Num Bolts",        "min": 2,    "max": 20,    "step": 1,    "default": 12},

    # VI. Nozzle Retainer Bolts
    "nozzle_bolt_diameter":    {"label": "Nozzle Bolt D (mm)",         "min": 1.0,  "max": 20.0,  "step": 1.0,  "default": 6.0},
    "nozzle_num_bolts":        {"label": "Nozzle Num Bolts",            "min": 2,    "max": 20,    "step": 1,    "default": 12},

    # VII. Oxidizer Tank
    "ox_tank_safety_factor":   {"label": "Ox Tank SF",                  "min": 1.0,  "max": 4.0,   "step": 0.1,  "default": 1.5},
    "ox_tank_outer_diameter":  {"label": "Ox Tank Outer D (cm)",        "min": 1.0,  "max": 20.0,  "step": 0.5,  "default": 5.0},
    "ox_tank_wall_thk":        {"label": "Ox Tank Wall (mm)",           "min": 1.0,  "max": 10.0,  "step": 0.1,  "default": 3.5},
    "ox_tank_length":          {"label": "Ox Tank Len (cm)",            "min": 5.0,  "max": 100.0, "step": 0.5,  "default": 30.0},
    "ox_tank_temp":            {"label": "Ox Tank Temp (°C)",           "min": -50.0,"max": 100.0, "step": 1.0,  "default": 25.0},
    "ox_tank_frontcap_thk":    {"label": "Ox Tank Front Cap (mm)",     "min": 1.0,  "max": 20.0,  "step": 0.5,  "default": 10.0},
    "ox_tank_backcap_thk":     {"label": "Ox Tank Back Cap (mm)",      "min": 1.0,  "max": 20.0,  "step": 0.5,  "default": 10.0},

    # VIII. Oxidizer Tank Bolts
    "ox_tank_bolt_diameter":   {"label": "Ox Tank Bolt D (mm)",        "min": 1.0,  "max": 20.0,  "step": 1.0,  "default": 6.0},
    "ox_tank_num_bolts":       {"label": "Ox Tank Num Bolts",           "min": 2,    "max": 20,    "step": 1,    "default": 12},

    # IX. Assembly Parameters
    "motor_ox_gap":            {"label": "Motor-Ox Tank Gap (mm)",      "min": 0.0,  "max": 100.0, "step": 1.0,  "default": 10.0}
}

dropdown_config = {
    "casing_material": {
        "label":   "Casing Material",
        "options": ["SS304", "Al6061", "Titanium"],
        "default": "SS304"
    },
    "frontcap_material": {
        "label":   "Front Cap Material",
        "options": ["SS304", "Al6061", "Titanium"],
        "default": "SS304"
    },
    "retainer_material": {
        "label":   "Retainer Material",
        "options": ["SS304", "Al6061", "Titanium"],
        "default": "SS304"
    },
    "ox_tank_material": {
        "label":   "Ox Tank Body Material",
        "options": ["SS304", "Al6061", "Titanium"],
        "default": "SS304"
    },
    "ox_tank_frontcap_material": {
        "label":   "Ox Tank Front Cap Material",
        "options": ["SS304", "Al6061", "Titanium"],
        "default": "SS304"
    },
    "ox_tank_backcap_material": {
        "label":   "Ox Tank Back Cap Material",
        "options": ["SS304", "Al6061", "Titanium"],
        "default": "SS304"
    }
}
