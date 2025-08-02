# hybrid_rocket/geometry.py

"""
geometry.py

Geometric calculations for port, chamber, casing, insulation, and nozzle profiles.
EXACT implementation from integrated_code_HRM(4)_omn.ipynb with all geometric functions.
"""

import numpy as np


def port_area(radius: float) -> float:
    """
    Computes cross-sectional area of the port.
    EXACT implementation from notebook.

    Parameters:
        radius : float
            Port radius (m)

    Returns:
        float : Port area (m²)
    """
    return np.pi * radius**2


def update_port_radius(radius: float, rate: float, dt: float) -> float:
    """
    Updates port radius over one timestep based on regression rate.
    EXACT implementation from notebook: r1 += dr where dr = r_dot * dt

    Parameters:
        radius : float
            Current port radius (m)
        rate : float
            Regression rate (m/s)
        dt : float
            Time step (s)

    Returns:
        float : Updated port radius (m)
    """
    return radius + rate * dt


def grain_volume(r1: float, r2: float, length: float) -> float:
    """
    Computes volume of fuel grain as a cylindrical shell.
    EXACT implementation from notebook fuel mass calculations.

    Parameters:
        r1 : float
            Inner port radius (m)
        r2 : float
            Outer fuel radius (m)
        length : float
            Grain length (m)

    Returns:
        float : Grain volume (m³)
    """
    return np.pi * (r2**2 - r1**2) * length


def burning_surface_area(port_radius: float, grain_length: float) -> float:
    """
    Computes lateral burning surface area of the grain.
    EXACT implementation from notebook regression calculations.

    Parameters:
        port_radius : float
            Current port radius (m)
        grain_length : float
            Grain length (m)

    Returns:
        float : Surface area (m²)
    """
    return 2 * np.pi * port_radius * grain_length


def insulation_outer_radius(inner_radius: float, thickness: float) -> float:
    """
    Computes outer radius of insulation.
    EXACT implementation from notebook insulation calculations.

    Parameters:
        inner_radius : float
            Inner radius before insulation (m)
        thickness : float
            Insulation thickness (m)

    Returns:
        float : Outer radius after insulation (m)
    """
    return inner_radius + thickness


def casing_outer_diameter(inner_diameter: float, wall_thickness: float) -> float:
    """
    Computes outer diameter of casing from inner diameter and wall thickness.
    EXACT implementation from notebook casing calculations.

    Parameters:
        inner_diameter : float
            Inner diameter of casing (m)
        wall_thickness : float
            Wall thickness (m)

    Returns:
        float : Outer diameter of casing (m)
    """
    return inner_diameter + 2 * wall_thickness


def nozzle_profile_coords(
    L_conv: float,
    throat_len: float,
    L_div: float,
    r_inlet: float,
    r_throat: float,
    r_exit: float
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generates 2D profile coordinates of the nozzle for plotting.
    EXACT implementation from notebook nozzle geometry calculations.

    Parameters:
        L_conv : float
            Converging section length (m)
        throat_len : float
            Throat section length (m)
        L_div : float
            Diverging section length (m)
        r_inlet : float
            Inlet radius (m)
        r_throat : float
            Throat radius (m)
        r_exit : float
            Exit radius (m)

    Returns:
        tuple of np.ndarray:
            (x_coords, y_coords) defining the nozzle contour
    """
    x = np.array([0, L_conv, L_conv + throat_len, L_conv + throat_len + L_div])
    y = np.array([r_inlet, r_throat, r_throat, r_exit])
    return x, y


def nozzle_geometry_from_angles(
    r_inlet: float,
    r_throat: float,
    throat_length: float,
    converge_angle_deg: float,
    diverge_angle_deg: float,
    expansion_ratio: float = 4.0
) -> dict:
    """
    Computes complete nozzle geometry from design angles.
    EXACT implementation from notebook nozzle calculations.
    
    Parameters:
        r_inlet : float
            Inlet radius (m)
        r_throat : float
            Throat radius (m)
        throat_length : float
            Throat length (m)
        converge_angle_deg : float
            Convergence half-angle (degrees)
        diverge_angle_deg : float
            Divergence half-angle (degrees)
        expansion_ratio : float
            Area expansion ratio (Ae/At)
    
    Returns:
        dict: Complete nozzle geometry parameters
    """
    # Convert angles to radians
    converge_angle = np.radians(converge_angle_deg)
    diverge_angle = np.radians(diverge_angle_deg)
    
    # Converging section length (EXACT notebook formula)
    L_conv = (r_inlet - r_throat) / np.tan(converge_angle) if converge_angle != 0 else 0.01
    
    # Exit radius from expansion ratio
    r_exit = r_throat * np.sqrt(expansion_ratio)
    
    # Diverging section length (EXACT notebook formula)
    L_div = (r_exit - r_throat) / np.tan(diverge_angle) if diverge_angle != 0 else 0.01
    
    # Total nozzle length
    L_total = L_conv + throat_length + L_div
    
    # Areas
    A_inlet = np.pi * r_inlet**2
    A_throat = np.pi * r_throat**2
    A_exit = np.pi * r_exit**2
    
    return {
        'L_conv': L_conv,
        'L_throat': throat_length,
        'L_div': L_div,
        'L_total': L_total,
        'r_inlet': r_inlet,
        'r_throat': r_throat,
        'r_exit': r_exit,
        'A_inlet': A_inlet,
        'A_throat': A_throat,
        'A_exit': A_exit,
        'expansion_ratio': A_exit / A_throat,
        'contraction_ratio': A_inlet / A_throat
    }


def total_motor_length(
    precomb: float,
    grain_len: float,
    postcomb: float,
    front_cap: float,
    retainer: float,
    nozzle_len: float,
    gap: float = 0.0
) -> float:
    """
    Computes total axial length of the motor assembly.
    EXACT implementation from notebook L_total calculations.

    Parameters:
        precomb : float
            Pre-combustion section length (m)
        grain_len : float
            Grain length (m)
        postcomb : float
            Post-combustion section length (m)
        front_cap : float
            Front cap length (m)
        retainer : float
            Nozzle retainer length (m)
        nozzle_len : float
            Nozzle length (m)
        gap : float, optional
            Additional axial gap (m) [default: 0.0]

    Returns:
        float : Total length (m)
    """
    return precomb + grain_len + postcomb + front_cap + retainer + nozzle_len + gap


def oxidizer_tank_geometry(
    outer_diameter: float,
    wall_thickness: float,
    length: float,
    frontcap_thickness: float,
    backcap_thickness: float
) -> dict:
    """
    Computes oxidizer tank geometric parameters.
    EXACT implementation from notebook tank calculations.
    
    Parameters:
        outer_diameter : float
            Tank outer diameter (m)
        wall_thickness : float
            Wall thickness (m)
        length : float
            Tank cylindrical length (m)
        frontcap_thickness : float
            Front cap thickness (m)
        backcap_thickness : float
            Back cap thickness (m)
    
    Returns:
        dict: Tank geometry parameters
    """
    inner_diameter = outer_diameter - 2 * wall_thickness
    inner_radius = inner_diameter / 2
    outer_radius = outer_diameter / 2
    
    # Volumes
    inner_volume = np.pi * (inner_radius**2) * length
    available_volume = 0.8 * inner_volume  # 80% ullage (EXACT notebook)
    
    # Total tank length including caps
    total_length = frontcap_thickness + length + backcap_thickness
    
    return {
        'outer_diameter': outer_diameter,
        'inner_diameter': inner_diameter,
        'outer_radius': outer_radius,
        'inner_radius': inner_radius,
        'wall_thickness': wall_thickness,
        'length': length,
        'total_length': total_length,
        'inner_volume': inner_volume,
        'available_volume': available_volume,
        'frontcap_thickness': frontcap_thickness,
        'backcap_thickness': backcap_thickness
    }


def casing_geometry(
    fuel_outer_radius: float,
    insulation_thickness: float,
    wall_thickness: float
) -> dict:
    """
    Computes casing geometric parameters.
    EXACT implementation from notebook casing calculations.
    
    Parameters:
        fuel_outer_radius : float
            Outer radius of fuel grain (m)
        insulation_thickness : float
            Insulation thickness (m)
        wall_thickness : float
            Casing wall thickness (m)
    
    Returns:
        dict: Casing geometry parameters
    """
    inner_radius = fuel_outer_radius + insulation_thickness
    outer_radius = inner_radius + wall_thickness
    
    inner_diameter = 2 * inner_radius
    outer_diameter = 2 * outer_radius
    
    return {
        'inner_radius': inner_radius,
        'outer_radius': outer_radius,
        'inner_diameter': inner_diameter, 
        'outer_diameter': outer_diameter,
        'wall_thickness': wall_thickness,
        'insulation_thickness': insulation_thickness
    }