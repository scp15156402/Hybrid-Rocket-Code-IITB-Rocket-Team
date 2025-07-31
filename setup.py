from setuptools import setup, find_packages

setup(
    name="hybrid_rocket",
    version="0.1.0",
    description="Hybrid Rocket Motor simulation package",
    author="Om Nunase & IITBRT",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "scipy",
        "pandas",
        "ipywidgets",
    ],
    entry_points={
        "console_scripts": [
            "hrm=hybrid_rocket.main:run",
        ],
    },
)
