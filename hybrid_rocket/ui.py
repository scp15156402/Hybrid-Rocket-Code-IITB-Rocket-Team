"""
Interactive UI components (for Jupyter/Colab).
"""

import ipywidgets as widgets
from IPython.display import display

def create_slider(name: str, min_val, max_val, step, initial):
    """
    Utility to generate a labeled FloatSlider.
    """
    return widgets.FloatSlider(
        description=name,
        min=min_val,
        max=max_val,
        step=step,
        value=initial,
    )

def display_sliders(**kwargs):
    """
    Display multiple sliders given as name: widget.
    """
    for widget in kwargs.values():
        display(widget)
