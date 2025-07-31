'''
plots.py

Visualization tools for hybrid rocket simulation results.
Directly adapted from integrated_code_HRM(4)_omn.ipynb.
'''

import matplotlib.pyplot as plt


def plot_thrust_vs_time(time, thrust):
    plt.figure()
    plt.plot(time, thrust, label='Thrust')
    plt.xlabel('Time (s)')
    plt.ylabel('Thrust (N)')
    plt.title('Thrust vs Time')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_radius_vs_time(time, radius):
    plt.figure()
    plt.plot(time, radius, label='Port Radius')
    plt.xlabel('Time (s)')
    plt.ylabel('Radius (m)')
    plt.title('Port Radius vs Time')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_of_vs_time(time, of):
    plt.figure()
    plt.plot(time, of, label='O/F Ratio')
    plt.xlabel('Time (s)')
    plt.ylabel('O/F Ratio')
    plt.title('O/F Ratio vs Time')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_gox_vs_time(time, G_ox):
    plt.figure()
    plt.plot(time, G_ox, label='G_ox')
    plt.xlabel('Time (s)')
    plt.ylabel('Oxidizer Mass Flux (kg/m^2/s)')
    plt.title('Oxidizer Mass Flux vs Time')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_isp_vs_time(time, isp):
    plt.figure()
    plt.plot(time, isp, label='Specific Impulse')
    plt.xlabel('Time (s)')
    plt.ylabel('Isp (s)')
    plt.title('Specific Impulse vs Time')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


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
    plt.show()
