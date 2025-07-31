'''
plots.py

Visualization tools for hybrid rocket simulation results.
Updated for Streamlit integration.
'''

import matplotlib.pyplot as plt
import streamlit as st


def plot_thrust_vs_time(time, thrust):
    fig, ax = plt.subplots()
    ax.plot(time, thrust, label='Thrust')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Thrust (N)')
    ax.set_title('Thrust vs Time')
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)


def plot_radius_vs_time(time, radius):
    fig, ax = plt.subplots()
    ax.plot(time, radius, label='Port Radius')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Radius (m)')
    ax.set_title('Port Radius vs Time')
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)


def plot_of_vs_time(time, of):
    fig, ax = plt.subplots()
    ax.plot(time, of, label='O/F Ratio')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('O/F Ratio')
    ax.set_title('O/F Ratio vs Time')
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)


def plot_gox_vs_time(time, G_ox):
    fig, ax = plt.subplots()
    ax.plot(time, G_ox, label='G_ox')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Oxidizer Mass Flux (kg/m^2/s)')
    ax.set_title('Oxidizer Mass Flux vs Time')
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)


def plot_all(time, thrust, radius, of, G_ox):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    axes[0, 0].plot(time, thrust)
    axes[0, 0].set_title('Thrust vs Time')
    axes[0, 0].set_xlabel('Time (s)')
    axes[0, 0].set_ylabel('Thrust (N)')
    axes[0, 0].grid(True)

    axes[0, 1].plot(time, radius)
    axes[0, 1].set_title('Port Radius vs Time')
    axes[0, 1].set_xlabel('Time (s)')
    axes[0, 1].set_ylabel('Radius (m)')
    axes[0, 1].grid(True)

    axes[1, 0].plot(time, of)
    axes[1, 0].set_title('O/F Ratio vs Time')
    axes[1, 0].set_xlabel('Time (s)')
    axes[1, 0].set_ylabel('O/F')
    axes[1, 0].grid(True)

    axes[1, 1].plot(time, G_ox)
    axes[1, 1].set_title('Oxidizer Mass Flux vs Time')
    axes[1, 1].set_xlabel('Time (s)')
    axes[1, 1].set_ylabel('G_ox (kg/m^2/s)')
    axes[1, 1].grid(True)

    fig.tight_layout()
    st.pyplot(fig)
