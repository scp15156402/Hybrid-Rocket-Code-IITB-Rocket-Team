# features/dropdowns/generate_cad/logic.py

import os
import cadquery as cq
from datetime import datetime

def generate_cad_parts(current_values: dict, results: dict, cad_dir: str) -> dict:
    """
    Generate STEP and STL for each component based on parameters.
    Returns a dict: { component_name: { 'step': filename, 'stl': filename } }
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    files = {}

    D_outer = current_values.get("ox_tank_outer_diameter", 10) / 100.0  # cm → m
    t_wall  = current_values.get("ox_tank_wall_thk", 2) / 1000.0      # mm → m
    L       = current_values.get("ox_tank_length", 50) / 100.0        # cm → m
    r_out = D_outer / 2.0
    r_in  = r_out - t_wall

    tank_shell = (
        cq.Workplane("XY")
        .circle(r_out)
        .extrude(L)
        .faces(">Z")
        .workplane()
        .circle(r_in)
        .extrude(-L)
    )

    step_name = f"ox_tank_shell_{ts}.step"
    stl_name  = f"ox_tank_shell_{ts}.stl"
    tank_shell.exportStep(os.path.join(cad_dir, step_name))
    tank_shell.exportStl(os.path.join(cad_dir, stl_name))

    files["ox_tank_shell"] = {"step": step_name, "stl": stl_name}

    # TODO: Add generation for other components

    return files
