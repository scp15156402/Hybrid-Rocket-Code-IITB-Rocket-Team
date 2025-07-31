'''
material_db.py

Material properties database for Hybrid Rocket Simulation
Extracted directly from integrated_code_HRM(4)_omn.ipynb
'''

# Material properties: density (kg/m^3) and yield strength (Pa)
material_properties = {
    'SS304': {
        'rho': 8000,       # kg/m³
        'sigma_y': 205e6   # Pa
    },
    'Aluminum': {
        'rho': 2700,       # kg/m³ (Typical for Aluminum alloys)
        'sigma_y': 276e6   # Pa (Typical for 6061-T6 Aluminum)
    },
    'Titanium Grade 5': {
        'rho': 4430,       # kg/m³
        'sigma_y': 828e6   # Pa
    },
    'Carbon Steel': {
        'rho': 7850,       # kg/m³
        'sigma_y': 250e6   # Pa
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
    return material_properties.get(material_name)
