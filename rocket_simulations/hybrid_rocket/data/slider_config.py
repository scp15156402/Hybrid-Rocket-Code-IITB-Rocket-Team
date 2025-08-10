# hybrid_rocket/slider_config.py

"""
slider_config.py

Enhanced UI configuration with clear, professional labels aligned with notebook parameters.
"""

from rocket_simulations.hybrid_rocket.data.material_db import material_properties

slider_config = {
    # I. Combustion Geometry & Fuel Parameters
    "r1": {
        "label": "Inner Port Radius (r1, cm)",
        "min": 0.1,
        "max": 4.0,
        "step": 0.1,
        "default": 0.7
    },
    "r2": {
        "label": "Outer Fuel Radius (r2, cm)",
        "min": 1.0,
        "max": 10.0,
        "step": 0.1,
        "default": 1.9
    },
    "L": {
        "label": "Grain Length (cm)",
        "min": 1.0,
        "max": 50.0,
        "step": 0.1,
        "default": 6.0
    },
    "mdot_ox": {
        "label": "Oxidizer Mass Flow (g/s)",
        "min": 0.0,
        "max": 3000.0,
        "step": 47.0,
        "default": 47.0
    },
    "rho_fuel": {
        "label": "Fuel Density (kg/m³)",
        "min": 500.0,
        "max": 1500.0,
        "step": 10.0,
        "default": 930.0
    },

    # II. Casing & Insulation
    "insul_grain_thk": {
        "label": "Grain Insulation Thickness (mm)",
        "min": 0.0,
        "max": 10.0,
        "step": 0.1,
        "default": 2.5
    },
    "insul_prepost_thk": {
        "label": "Pre/Post Insulation Thickness (mm)",
        "min": 0.0,
        "max": 10.0,
        "step": 0.1,
        "default": 3.0
    },
    "casing_wall_thk": {
        "label": "Casing Wall Thickness (mm)",
        "min": 1.0,
        "max": 20.0,
        "step": 0.1,
        "default": 3.0
    },
    "safety_factor": {
        "label": "Casing Safety Factor",
        "min": 1.5,
        "max": 3.0,
        "step": 0.1,
        "default": 2.0
    },
    "pre_comb_len": {
        "label": "Pre-Combustion Chamber Length (cm)",
        "min": 0.0,
        "max": 10.0,
        "step": 0.1,
        "default": 3.0
    },
    "post_comb_len": {
        "label": "Post-Combustion Chamber Length (cm)",
        "min": 0.0,
        "max": 20.0,
        "step": 0.1,
        "default": 3.0
    },

    # III. Nozzle Geometry
    "converge_half_angle": {
        "label": "Converging Angle (°)",
        "min": 10,
        "max": 60,
        "step": 1,
        "default": 45
    },
    "throat_diameter": {
        "label": "Throat Diameter (mm)",
        "min": 4.0,
        "max": 40.0,
        "step": 0.1,
        "default": 6.0
    },
    "throat_length": {
        "label": "Throat Length (mm)",
        "min": 5.0,
        "max": 50.0,
        "step": 0.1,
        "default": 7.0
    },
    "diverge_half_angle": {
        "label": "Diverging Angle (°)",
        "min": 5,
        "max": 30,
        "step": 1,
        "default": 15
    },

    # IV. Retainer & Front Cap
    "retainer_length": {
        "label": "Retainer Length (mm)",
        "min": 5.0,
        "max": 30.0,
        "step": 0.1,
        "default": 10.0
    },
    "retainer_inner_radius": {
        "label": "Retainer Inner Radius (mm)",
        "min": 10.0,
        "max": 50.0,
        "step": 0.1,
        "default": 20.0
    },
    "frontcap_length": {
        "label": "Front Cap Length (mm)",
        "min": 5.0,
        "max": 50.0,
        "step": 0.1,
        "default": 20.0
    },

    # V. Front Cap Bolts
    "frontcap_bolt_diameter": {
        "label": "Front Cap Bolt Diameter (mm)",
        "min": 2.0,
        "max": 20.0,
        "step": 0.1,
        "default": 6.0
    },
    "frontcap_num_bolts": {
        "label": "Number of Front Cap Bolts",
        "min": 2,
        "max": 20,
        "step": 1,
        "default": 12
    },

    # VI. Nozzle Retainer Bolts
    "nozzle_bolt_diameter": {
        "label": "Nozzle Bolt Diameter (mm)",
        "min": 2.0,
        "max": 20.0,
        "step": 0.1,
        "default": 6.0
    },
    "nozzle_num_bolts": {
        "label": "Number of Nozzle Bolts",
        "min": 2,
        "max": 20,
        "step": 1,
        "default": 12
    },

    # VII. Oxidizer Tank
    "ox_tank_safety_factor": {
        "label": "Oxidizer Tank Safety Factor",
        "min": 1.0,
        "max": 4.0,
        "step": 0.1,
        "default": 1.5
    },
    "ox_tank_outer_diameter": {
        "label": "Oxidizer Tank Diameter (cm)",
        "min": 1.0,
        "max": 20.0,
        "step": 0.5,
        "default": 10.0
    },
    "ox_tank_wall_thk": {
        "label": "Oxidizer Tank Wall Thickness (mm)",
        "min": 1.0,
        "max": 10.0,
        "step": 0.1,
        "default": 3.5
    },
    "ox_tank_length": {
        "label": "Oxidizer Tank Length (cm)",
        "min": 5.0,
        "max": 100.0,
        "step": 0.5,
        "default": 30.0
    },
    "ox_tank_temp": {
        "label": "Oxidizer Tank Temperature (°C)",
        "min": -50.0,
        "max": 100.0,
        "step": 1.0,
        "default": 25.0
    },
    "ox_tank_frontcap_thk": {
        "label": "Tank Front Cap Thickness (mm)",
        "min": 1.0,
        "max": 20.0,
        "step": 0.5,
        "default": 10.0
    },
    "ox_tank_backcap_thk": {
        "label": "Tank Back Cap Thickness (mm)",
        "min": 1.0,
        "max": 20.0,
        "step": 0.5,
        "default": 10.0
    },

    # VIII. Oxidizer Tank Bolts
    "ox_tank_bolt_diameter": {
        "label": "Tank Bolt Diameter (mm)",
        "min": 2.0,
        "max": 20.0,
        "step": 0.1,
        "default": 6.0
    },
    "ox_tank_num_bolts": {
        "label": "Number of Tank Bolts",
        "min": 2,
        "max": 20,
        "step": 1,
        "default": 12
    },

    # IX. Assembly Parameters
    "motor_ox_gap": {
        "label": "Motor–Tank Gap (mm)",
        "min": 0.0,
        "max": 100.0,
        "step": 1.0,
        "default": 0.0
    }
}

# Dropdown configuration for materials
dropdown_config = {
    "casing_material": {
        "label": "Casing Material:",
        "options": list(material_properties.keys()),
        "default": "SS304"
    },
    "frontcap_material": {
        "label": "Front Cap Material:",
        "options": list(material_properties.keys()),
        "default": "SS304"
    },
    "retainer_material": {
        "label": "Retainer Material:",
        "options": list(material_properties.keys()),
        "default": "SS304"
    },
    "ox_tank_material": {
        "label": "Oxidizer Tank Material:",
        "options": list(material_properties.keys()),
        "default": "SS304"
    },
    "ox_tank_frontcap_material": {
        "label": "Tank Front Cap Material:",
        "options": list(material_properties.keys()),
        "default": "SS304"
    },
    "ox_tank_backcap_material": {
        "label": "Tank Back Cap Material:",
        "options": list(material_properties.keys()),
        "default": "SS304"
    }
}
