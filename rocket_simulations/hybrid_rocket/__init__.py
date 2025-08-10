# hybrid_rocket/__init__.py

__version__ = "0.1.0"

# Public entrypoints
from .main   import app
from .plots  import plot_motor_assembly, plot_nozzle_profile
from .export import (
    export_simulation_data,
    compute_structural_metrics,
    get_summary_dict
)

# Define the public API
__all__ = [
    "app",
    "plot_motor_assembly",
    "plot_nozzle_profile",
    "export_simulation_data",
    "compute_structural_metrics",
    "get_summary_dict",
    "__version__",
]
