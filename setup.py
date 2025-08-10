from setuptools import setup, find_packages

setup(
    name="hybrid_rocket",
    version="0.1.0",
    description="Hybrid Rocket Motor simulation and CAD export web application",
    author="Om Nunase & Siddhant Patil",
    packages=find_packages(),
    include_package_data=True,  # include static/templates
    install_requires=[
        "flask>=2.1.0",
        "flask-caching>=1.10.1",
        "numpy>=1.23.0",
        "matplotlib>=3.6.0",
        "scipy>=1.9.0",
        "pandas>=1.5.0",
        "cadquery>=2.4.0",        # for STEP/STL export
        "ipywidgets>=8.0.0"
    ],
    entry_points={
        "console_scripts": [
            # Starts your Flask app via `hrm` command
            "hrm=app:app.run",
        ],
    },
)
