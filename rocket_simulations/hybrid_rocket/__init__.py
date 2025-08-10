__version__ = "0.1.0"

# Create a Flask app instance from the factory
from .hybrid_app import create_app
app = create_app()

from .plots import plot_motor_assembly, plot_nozzle_profile
from .export import (
    export_simulation_data,
    compute_structural_metrics,
    get_summary_dict,
)

__all__ = [
    "app",
    "plot_motor_assembly",
    "plot_nozzle_profile",
    "export_simulation_data",
    "compute_structural_metrics",
    "get_summary_dict",
    "__version__",
]
