'''
material_db.py

Material properties database for Hybrid Rocket Simulation
Extracted directly from integrated_code_HRM(4)_omn.ipynb
'''

# Material properties: density (kg/m^3) and yield strength (Pa)
material_properties = {
    'SS304': {
        'rho': 8000,        # kg/m³
        'sigma_y': 205e6    # Pa
    },
    'Aluminum': {
        'rho': 2700,        # kg/m³ (Typical for 6061-T6 Aluminum)
        'sigma_y': 276e6    # Pa
    },
    'Titanium Grade 5': {
        'rho': 4430,
        'sigma_y': 828e6
    },
    'Carbon Steel': {
        'rho': 7850,
        'sigma_y': 250e6
    }
}


def get_material_properties(material_name: str) -> dict:
    '''
    Retrieve material properties by name.

    Parameters
    ----------
    material_name : str
        Name of the material (e.g., 'SS304').

    Returns
    -------
    dict
        Dictionary containing 'rho' and 'sigma_y'.
    '''
    props = material_properties.get(material_name)
    if props is None:
        raise ValueError(f"[ERROR] Material '{material_name}' not found in database.")
    return props


def get_density(material_name: str) -> float:
    '''
    Retrieve only density for a given material.

    Returns
    -------
    float
        Density in kg/m³.
    '''
    return get_material_properties(material_name)['rho']


def get_yield_strength(material_name: str) -> float:
    '''
    Retrieve only yield strength for a given material.

    Returns
    -------
    float
        Yield strength in Pascals.
    '''
    return get_material_properties(material_name)['sigma_y']


def list_available_materials() -> list:
    '''
    Returns a list of all supported material names.
    '''
    return list(material_properties.keys())
