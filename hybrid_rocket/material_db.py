# hybrid_rocket/material_db.py

"""
material_db.py

Material properties database for Hybrid Rocket Simulation.
Extracted directly from integrated_code_HRM(4)_omn.ipynb (top cell only).
"""

# -----------------------------
# Material Properties Database
# -----------------------------
# Format: { 'Material Name': { 'rho': density [kg/m³], 'sigma_y': yield strength [Pa] } }

material_properties = {
    "SS304": {
        "rho": 8000,          # Density [kg/m³]
        "sigma_y": 205e6      # Yield strength [Pa]
    },
    "Aluminum": {
        "rho": 2700,          # Typical for 6061-T6
        "sigma_y": 276e6
    },
    "Titanium Grade 5": {
        "rho": 4430,
        "sigma_y": 828e6
    },
    "Carbon Steel": {
        "rho": 7850,
        "sigma_y": 250e6
    }
}


# -----------------------------
# Retrieval Functions
# -----------------------------

def get_material_properties(material_name: str) -> dict:
    """
    Retrieves material properties by name.

    Parameters:
        material_name : str
            Name of the material (e.g., 'SS304')

    Returns:
        dict : {'rho': density [kg/m³], 'sigma_y': yield strength [Pa]}
    """
    props = material_properties.get(material_name)
    if props is None:
        raise ValueError(f"[ERROR] Material '{material_name}' not found in database.")
    return props


def get_density(material_name: str) -> float:
    """
    Retrieves density of a given material.

    Parameters:
        material_name : str

    Returns:
        float : Density in kg/m³
    """
    return get_material_properties(material_name)['rho']


def get_yield_strength(material_name: str) -> float:
    """
    Retrieves yield strength of a given material.

    Parameters:
        material_name : str

    Returns:
        float : Yield strength in Pa
    """
    return get_material_properties(material_name)['sigma_y']


def list_available_materials() -> list:
    """
    Returns a list of available material names.

    Returns:
        list[str] : Material names available in the database
    """
    return list(material_properties.keys())
