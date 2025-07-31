# app.py

import streamlit as st
from hybrid_rocket.solver import simulate_burn
from hybrid_rocket.plots import plot_all
from hybrid_rocket.export import print_summary

st.set_page_config(layout="wide")
st.title("🚀 Hybrid Rocket Motor Simulator")

st.sidebar.header("Simulation Parameters")

# Sliders and inputs
mdot_ox = st.sidebar.slider("Oxidizer Mass Flow Rate (kg/s)", 0.01, 1.0, 0.05, 0.01)
rho_fuel = st.sidebar.slider("Fuel Density (kg/m³)", 500, 1500, 930)
r1 = st.sidebar.slider("Initial Port Radius (m)", 0.005, 0.05, 0.01)
L = st.sidebar.slider("Fuel Grain Length (m)", 0.05, 0.5, 0.1)
dt = st.sidebar.slider("Time Step (s)", 0.001, 0.1, 0.01)
t_final = st.sidebar.slider("Burn Time (s)", 1.0, 10.0, 3.0)

# Optional nozzle parameters
st.sidebar.subheader("Nozzle Parameters")
Ve = st.sidebar.number_input("Exit Velocity Ve (m/s)", value=1800.0)
pe = st.sidebar.number_input("Exit Pressure Pe (Pa)", value=1e5)
pa = st.sidebar.number_input("Ambient Pressure Pa (Pa)", value=1e5)
Ae = st.sidebar.number_input("Nozzle Exit Area Ae (m²)", value=1e-4)

# Run button
if st.sidebar.button("Run Simulation"):
    results = simulate_burn(
        mdot_ox=mdot_ox,
        rho_fuel=rho_fuel,
        r1_init=r1,
        L_grain=L,
        dt=dt,
        t_final=t_final,
        Ve=Ve,
        pe=pe,
        pa=pa,
        Ae=Ae
    )

    st.success("✅ Simulation complete!")

    # Display summary
    st.subheader("📊 Simulation Summary")
    st.text(print_summary(results))  # Could be redirected to return a string

    # Plots
    st.subheader("📈 Performance Plots")
    plot_all(results["time"], results["thrust"], results["radius"], results["OF"], results["G_ox"])
else:
    st.info("Adjust parameters and click 'Run Simulation'.")

