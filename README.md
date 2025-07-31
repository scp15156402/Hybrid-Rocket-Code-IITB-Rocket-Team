# Hybrid Rocket Motor Simulator

This Python-based simulator models the internal ballistics and performance of a hybrid rocket motor, offering a modular, object-oriented structure for ease of use and extensibility.

## Project Overview

Hybrid rocket motors utilize a **liquid oxidizer** that flows through and combusts a **solid fuel grain**. This simulator models the interplay between oxidizer flow, fuel regression (burn rate), and consequent thrust generation. It enables users to analyze:

- **Regression rate** (how quickly fuel is consumed)
- **Oxidizer-to-Fuel (O/F) ratio**
- **Thrust and specific impulse (Isp) over time**
- **Port geometry evolution (radius/area)**
- **Total impulse and burn duration**

Intended applications include early-stage engineering validation, instructional use, and design parameter sweeps for small-scale hybrid motors.

## Directory Structure

```
hybrid_rocket/
├── __init__.py
├── constants.py         # Physical constants and default simulation parameters
├── combustion.py        # Implements combustion physics: regression, thrust, Isp, OF ratio
├── geometry.py          # Handles port area, volume, and geometry updates
├── material_db.py       # Lookups for solid fuel and oxidizer properties
├── structure.py         # Casing mass, mechanical integrity, and pressure checks
├── solver.py            # Main simulation engine (time-stepping logic)
├── export.py            # CSV data and summary exports
├── plots.py             # Generates relevant plots/visualizations
app.py                   # GUI launcher (Streamlit)
main.py                  # Command-line execution
README.md                # Complete documentation
```

## Key Features

- **Full time-domain simulation** for hybrid rocket ballistics
- Modular Python code, facilitating maintainability and testing
- Plots for thrust, port radius, O/F ratio, oxidizer mass flux over time
- Command-line and GUI (Streamlit) support
- CSV export capabilities for detailed post-processing
- Extensible material and geometry modules

## Getting Started

### 1. Install Dependencies

```
pip install -r requirements.txt
```

*Optional*: Set up a virtual environment for isolation

```
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
```

### 2. How to Run

- **Command Line**:  
  ```
  python main.py
  ```
- **GUI (Streamlit)**:  
  ```
  streamlit run app.py
  ```

## Output Example

**Simulation summary (console):**

```
=== SIMULATION SUMMARY ===
Total Burn Time:     3.80 s
Total Impulse:       896.65 Ns
Average Thrust:      235.96 N
Peak Thrust:         235.96 N
Average O/F Ratio:   0.62
```

**CSV Export Columns:**

- Time (s)
- Thrust (N)
- Port Radius (m)
- O/F Ratio
- Oxidizer Mass Flux (kg/m²/s)

**Generated Plots:**

- Thrust vs Time
- Port Radius vs Time
- O/F Ratio vs Time
- Oxidizer Mass Flux vs Time

## Physics and Equations

| Quantity              | Formula                                                |
|-----------------------|--------------------------------------------------------|
| Regression rate       | \( r = a \cdot G_{ox}^n \)                             |
| Oxidizer mass flux    | \( G_{ox} = \frac{\dot{m}_{ox}}{A_{port}} \)           |
| Fuel flow rate        | \( \dot{m}_{fuel} = \rho_{fuel} \cdot A_{burn} \cdot r \) |
| O/F Ratio             | \( \frac{\dot{m}_{ox}}{\dot{m}_{fuel}} \)              |
| Thrust                | \( F = \dot{m}_{total} V_e + (p_e - p_a) A_e \)        |
| Specific Impulse      | \( I_{sp} = \frac{F}{\dot{m}_{total} \cdot g} \)       |

This structure and simulation enable robust, tailored modeling of hybrid rocket performance for experimentation, learning, and optimization.
```

