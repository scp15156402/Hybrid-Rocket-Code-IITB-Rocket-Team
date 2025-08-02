# hybrid_rocket/slider_config.py

"""
slider_config.py

Enhanced UI configuration with corrected parameter names matching the notebook.
EXACT implementation from integrated_code_HRM(4)_omn.ipynb slider definitions.
"""

from hybrid_rocket.material_db import material_properties

# Enhanced slider configuration matching EXACT notebook parameters
slider_config = {
    # I. Combustion Geometry & Fuel Parameters (EXACT notebook values)
    "r1": {
        "label": "r1 (cm)",
        "min": 0.1,
        "max": 4.0,
        "step": 0.1,
        "default": 0.7  # Notebook default: r1_slider = 0.7
    },
    "r2": {
        "label": "r2 Fuel (cm)",
        "min": 1.0,
        "max": 10.0,
        "step": 0.1,
        "default": 1.9  # Notebook default: r2_slider = 1.9
    },
    "L": {
        "label": "Grain Len (cm)",
        "min": 1.0,
        "max": 50.0,
        "step": 0.1,
        "default": 6.0  # Notebook default: grain_slider = 6.0
    },
    "mdot_ox": {
        "label": "mdot_ox (g/s)",
        "min": 0.0,
        "max": 3000.0,
        "step": 47.0,
        "default": 47.0  # Notebook default: mdot_slider = 47.0
    },
    "rho_fuel": {
        "label": "Fuel Density (kg/m³)",
        "min": 500.0,
        "max": 1500.0,
        "step": 10.0,
        "default": 930.0  # Notebook default (implied)
    },

    # II. Casing & Insulation (EXACT notebook parameters)
    "insul_grain_thk": {
        "label": "Insul Grain (mm)",
        "min": 0.0,
        "max": 10.0,
        "step": 0.1,
        "default": 2.5  # Notebook: insul_grain_thickness_slider = 2.5
    },
    "insul_prepost_thk": {  # Corrected name from notebook
        "label": "Insul Pre/Post (mm)",
        "min": 0.0,
        "max": 10.0,
        "step": 0.1,
        "default": 3.0  # Notebook: insul_pre_post_thickness_slider = 3.0
    },
    "casing_wall_thk": {
        "label": "Casing Wall (mm)",
        "min": 1.0,
        "max": 20.0,
        "step": 0.1,
        "default": 3.0  # Notebook: casing_wall_thickness_slider = 3.0
    },
    "safety_factor": {
        "label": "Casing SF",
        "min": 1.5,
        "max": 3.0,
        "step": 0.1,
        "default": 2.0  # Notebook: safety_slider = 2.0
    },
    "pre_comb_len": {
        "label": "Pre-comb (cm)",
        "min": 0.0,
        "max": 10.0,
        "step": 0.1,
        "default": 3.0  # Notebook: pre_slider = 3.0
    },
    "post_comb_len": {
        "label": "Post-comb (cm)",
        "min": 0.0,
        "max": 20.0,
        "step": 0.1,
        "default": 3.0  # Notebook: post_slider = 3.0
    },

    # III. Nozzle Geometry (EXACT notebook parameters)
    "converge_half_angle": {
        "label": "Converge (°)",
        "min": 10,
        "max": 60,
        "step": 1,
        "default": 45  # Notebook: conv_slider = 45
    },
    "throat_diameter": {
        "label": "Throat D (mm)",
        "min": 4.0,
        "max": 40.0,
        "step": 0.1,
        "default": 6.0  # Notebook: throat_d_slider = 6.0
    },
    "throat_length": {
        "label": "Throat Len (mm)",
        "min": 5.0,
        "max": 50.0,
        "step": 0.1,
        "default": 7.0  # Notebook: throat_l_slider = 7
    },
    "diverge_half_angle": {
        "label": "Diverge (°)",
        "min": 5,
        "max": 30,
        "step": 1,
        "default": 15  # Notebook: div_slider = 15
    },

    # IV. Retainer & Front Cap (EXACT notebook parameters)
    "retainer_length": {
        "label": "Retainer Len (mm)",
        "min": 5.0,
        "max": 30.0,
        "step": 0.1,
        "default": 10.0  # Notebook: retainer_len_slider = 10.0
    },
    "retainer_inner_radius": {
        "label": "Retainer Inner R (mm)",
        "min": 10.0,
        "max": 50.0,
        "step": 0.1,
        "default": 20.0  # Notebook: retainer_inner_r_slider = 20.0
    },
    "frontcap_length": {
        "label": "Front Cap Len (mm)",
        "min": 5.0,
        "max": 50.0,
        "step": 0.1,
        "default": 20.0  # Notebook: frontcap_len_slider = 20.0
    },

    # V. Front Cap Bolts (EXACT notebook parameters)
    "frontcap_bolt_diameter": {
        "label": "Front Cap Bolt D (mm)",
        "min": 2.0,
        "max": 20.0,
        "step": 0.1,
        "default": 6.0  # Notebook: frontcap_bolt_diameter_slider = 6.0
    },
    "frontcap_num_bolts": {
        "label": "Front Cap Num Bolts",
        "min": 2,
        "max": 20,
        "step": 1,
        "default": 12  # Notebook: frontcap_num_bolts_slider = 12
    },

    # VI. Nozzle Retainer Bolts (EXACT notebook parameters)
    "nozzle_bolt_diameter": {
        "label": "Nozzle Bolt D (mm)",
        "min": 2.0,
        "max": 20.0,
        "step": 0.1,
        "default": 6.0  # Notebook: nozzle_bolt_diameter_slider = 6.0
    },
    "nozzle_num_bolts": {
        "label": "Nozzle Num Bolts",
        "min": 2,
        "max": 20,
        "step": 1,
        "default": 12  # Notebook: nozzle_num_bolts_slider = 12
    },

    # VII. Oxidizer Tank (EXACT notebook parameters)
    "ox_tank_safety_factor": {
        "label": "Ox Tank SF",
        "min": 1.0,
        "max": 4.0,
        "step": 0.1,
        "default": 1.5  # Notebook: ox_tank_safety_slider = 1.5
    },
    "ox_tank_outer_diameter": {
        "label": "Ox Tank Diam (cm)",
        "min": 1.0,
        "max": 20.0,
        "step": 0.5,
        "default": 10.0  # Notebook: ox_tank_diameter_slider = 10.0 (but disabled, auto-calculated)
    },
    "ox_tank_wall_thk": {
        "label": "Ox Tank Wall (mm)",
        "min": 1.0,
        "max": 10.0,
        "step": 0.1,
        "default": 3.5  # Notebook: ox_tank_thickness_slider = 3.5
    },
    "ox_tank_length": {
        "label": "Ox Tank Len (cm)",
        "min": 5.0,
        "max": 100.0,
        "step": 0.5,
        "default": 30.0  # Notebook: ox_tank_length_slider = 30.0
    },
    "ox_tank_temp": {
        "label": "Ox Tank Temp (°C)",
        "min": -50.0,
        "max": 100.0,
        "step": 1.0,
        "default": 25.0  # Notebook: ox_tank_temperature_slider = 25.0
    },
    "ox_tank_frontcap_thk": {
        "label": "Ox Tank Front Cap (mm)",
        "min": 1.0,
        "max": 20.0,
        "step": 0.5,
        "default": 10.0  # Notebook: ox_tank_frontcap_len_slider = 10.0
    },
    "ox_tank_backcap_thk": {
        "label": "Ox Tank Back Cap (mm)",
        "min": 1.0,
        "max": 20.0,
        "step": 0.5,
        "default": 10.0  # Notebook: ox_tank_backcap_len_slider = 10.0
    },

    # VIII. Oxidizer Tank Bolts (EXACT notebook parameters)
    "ox_tank_bolt_diameter": {
        "label": "Ox Tank Bolt D (mm)",
        "min": 2.0,
        "max": 20.0,
        "step": 0.1,
        "default": 6.0  # Notebook: ox_tank_bolt_diameter_slider = 6.0
    },
    "ox_tank_num_bolts": {
        "label": "Ox Tank Num Bolts",
        "min": 2,
        "max": 20,
        "step": 1,
        "default": 12  # Notebook: ox_tank_num_bolts_slider = 12
    },

    # IX. Assembly Parameters (EXACT notebook parameters)
    "motor_ox_gap": {
        "label": "Motor-Ox Tank Gap (mm)",
        "min": 0.0,
        "max": 100.0,
        "step": 1.0,
        "default": 0.0  # Notebook: motor_ox_gap_slider = 0.0 (initially)
    }
}

# Material dropdown configuration (EXACT notebook dropdowns)
dropdown_config = {
    "casing_material": {
        "label": "Casing Mat:",
        "options": list(material_properties.keys()),
        "default": "SS304"  # Notebook: casing_material_dropdown default
    },
    "frontcap_material": {
        "label": "Front Cap Mat:",
        "options": list(material_properties.keys()),
        "default": "SS304"  # Notebook: frontcap_material_dropdown default
    },
    "retainer_material": {
        "label": "Retainer Mat:",
        "options": list(material_properties.keys()),
        "default": "SS304"  # Notebook: retainer_material_dropdown default
    },
    "ox_tank_material": {
        "label": "Ox Tank Mat:",
        "options": list(material_properties.keys()),
        "default": "SS304"  # Notebook: ox_tank_material_dropdown default
    },
    "ox_tank_frontcap_material": {
        "label": "Ox Tank Front Cap Mat:",
        "options": list(material_properties.keys()),
        "default": "SS304"  # Notebook: ox_tank_frontcap_material_dropdown default
    },
    "ox_tank_backcap_material": {
        "label": "Ox Tank Back Cap Mat:",
        "options": list(material_properties.keys()),
        "default": "SS304"  # Notebook: ox_tank_backcap_material_dropdown default
    }
}