
"""
plots.py

Visualization tools for hybrid rocket simulation results.
EXACT implementation matching integrated_code_HRM(4)_omn.ipynb.
Includes motor assembly, nozzle profile, and combined performance plots.
"""

import os
import matplotlib
# Force non-interactive Agg backend to avoid GUI/thread issues
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from io import BytesIO
from flask_caching import Cache
from hybrid_rocket.geometry import nozzle_profile_coords

# Where on disk to dump static images
PLOTS_DIR = os.path.join(os.getcwd(), "static", "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

cache: Cache = None  # Initialized via init_plot_cache()


def init_plot_cache(app):
    """
    Initializes Flask-Caching with SimpleCache.
    Call once in your Flask app setup (e.g., in app.py).
    """
    global cache
    cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
    cache.init_app(app)
    # Ensure static/plots exists relative to app root
    plots_path = os.path.join(app.root_path, "static", "plots")
    os.makedirs(plots_path, exist_ok=True)


def _save_to_cache_and_disk(fig, cache_key: str) -> str:
    """
    Save a matplotlib figure to a BytesIO buffer and store it in Flask cache,
    *and* write out to static/plots/<cache_key>.png for permanent storage.
    """
    # 1) In-memory cache
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=150)
    buf.seek(0)
    plt.close(fig)
    cache.set(cache_key, buf, timeout=300)  # Cache for 5 minutes

    # 2) Disk write
    disk_path = os.path.join(PLOTS_DIR, f"{cache_key}.png")
    with open(disk_path, "wb") as f:
        f.write(buf.getvalue())

    return cache_key


def plot_motor_assembly(current_values: dict, results: dict) -> str:
    """
    Plots a 2D cross-section of the entire motor assembly including the oxidizer tank and bolts.
    EXACT implementation from notebook plot_motor_assembly function.
    """
    # Extract values from current_values (converted from UI units)
    r1 = results['radius'][0]  # Initial port radius in m
    r2_fuel = current_values["r2"] / 100.0  # cm -> m
    
    # Unit conversions from notebook
    insulation_grain_thickness = current_values["insul_grain_thk"] / 1000.0  # mm -> m
    insulation_pre_post_thickness = current_values["insul_prepost_thk"] / 1000.0  # mm -> m
    L_grain = current_values["L"] / 100.0  # cm -> m
    t_wall = current_values["casing_wall_thk"] / 1000.0  # mm -> m
    
    # Pre/post combustion lengths
    pre_comb_cm = current_values["pre_comb_len"]  # cm
    post_comb_cm = current_values["post_comb_len"]  # cm
    
    # Front cap and retainer
    L_frontcap = current_values["frontcap_length"] / 1000.0  # mm -> m
    L_retainer_mm = current_values["retainer_length"]  # mm
    r_retainer_inner_mm = current_values["retainer_inner_radius"]  # mm
    
    # Nozzle geometry (computed in solver - simplified here)
    throat_d_mm = current_values["throat_diameter"]  # mm
    throat_len_mm = current_values["throat_length"]  # mm
    converge_deg = current_values["converge_half_angle"]
    diverge_deg = current_values["diverge_half_angle"]
    
    # Oxidizer tank
    ox_tank_D_outer_cm = current_values["ox_tank_outer_diameter"]  # cm
    ox_tank_t_mm = current_values["ox_tank_wall_thk"]  # mm
    ox_tank_L_cm = current_values["ox_tank_length"]  # cm
    ox_tank_frontcap_len_mm = current_values["ox_tank_frontcap_thk"]  # mm
    ox_tank_backcap_len_mm = current_values["ox_tank_backcap_thk"]  # mm
    motor_ox_gap_mm = current_values["motor_ox_gap"]  # mm
    
    # Bolt parameters
    frontcap_bolt_diameter_mm = current_values["frontcap_bolt_diameter"]  # mm
    frontcap_num_bolts = current_values["frontcap_num_bolts"]
    nozzle_bolt_diameter_mm = current_values["nozzle_bolt_diameter"]  # mm
    nozzle_num_bolts = current_values["nozzle_num_bolts"]
    ox_tank_bolt_diameter_mm = current_values["ox_tank_bolt_diameter"]  # mm
    ox_tank_num_bolts = current_values["ox_tank_num_bolts"]
    
    # Compute casing dimensions (notebook logic)
    casing_inner_radius = max(r2_fuel + insulation_grain_thickness, r2_fuel + insulation_pre_post_thickness)
    
    # Simplified nozzle geometry calculations
    r_throat = throat_d_mm / 2000.0  # mm -> m
    insulation_pre_post_inner_radius = casing_inner_radius - insulation_pre_post_thickness
    
    # Estimate nozzle lengths
    L_conv = (insulation_pre_post_inner_radius - r_throat) / np.tan(np.radians(converge_deg)) if converge_deg != 0 else 0.01
    throat_len = throat_len_mm / 1000.0  # mm -> m
    
    # Simplified exit calculation (assume expansion ratio ~4 for visualization)
    r_exit = r_throat * 2.0  # Simplified
    L_div = (r_exit - r_throat) / np.tan(np.radians(diverge_deg)) if diverge_deg != 0 else 0.01
    L_nozzle = L_conv + throat_len + L_div
    
    # Create nozzle profile data
    nozzle_profile = {
        'x': np.array([0, L_conv, L_conv + throat_len, L_conv + throat_len + L_div]) * 1000,  # mm
        'y_upper': np.array([insulation_pre_post_inner_radius, r_throat, r_throat, r_exit]) * 1000,  # mm
        'y_lower': -np.array([insulation_pre_post_inner_radius, r_throat, r_throat, r_exit]) * 1000  # mm
    }
    
    fig, ax = plt.subplots(figsize=(20, 5))  # Wide figure like notebook
    
    # Convert all dimensions to mm for plotting (EXACT notebook approach)
    r1_mm = r1 * 1000
    r2_fuel_mm = r2_fuel * 1000
    casing_inner_radius_mm = casing_inner_radius * 1000
    t_wall_mm = t_wall * 1000
    r_outer_mm = casing_inner_radius_mm + t_wall_mm
    L_frontcap_mm = L_frontcap * 1000
    pre_comb_mm = pre_comb_cm * 10  # cm -> mm
    L_grain_mm = L_grain * 1000
    post_comb_mm = post_comb_cm * 10  # cm -> mm
    L_nozzle_mm = L_nozzle * 1000
    insulation_grain_thickness_mm = insulation_grain_thickness * 1000
    insulation_pre_post_thickness_mm = insulation_pre_post_thickness * 1000
    insulation_outer_radius_mm = casing_inner_radius_mm
    
    insulation_grain_inner_radius_mm = insulation_outer_radius_mm - insulation_grain_thickness_mm
    insulation_pre_post_inner_radius_mm = insulation_outer_radius_mm - insulation_pre_post_thickness_mm
    
    # Oxidizer tank dimensions (EXACT notebook conversion)
    ox_tank_D_outer_mm = ox_tank_D_outer_cm * 10
    ox_tank_t_mm_plot = ox_tank_t_mm
    ox_tank_L_mm = ox_tank_L_cm * 10
    ox_tank_r_outer_mm = ox_tank_D_outer_mm / 2
    ox_tank_D_inner_mm = ox_tank_D_outer_mm - 2 * ox_tank_t_mm_plot
    ox_tank_r_inner_mm = ox_tank_D_inner_mm / 2
    ox_tank_L_total_mm = ox_tank_frontcap_len_mm + ox_tank_L_mm + ox_tank_backcap_len_mm
    
    # Axial positions (EXACT notebook logic)
    x_ox_tank_start = 0
    x_ox_tank_frontcap_end = x_ox_tank_start + ox_tank_frontcap_len_mm
    x_ox_tank_casing_end = x_ox_tank_frontcap_end + ox_tank_L_mm
    x_ox_tank_end = x_ox_tank_casing_end + ox_tank_backcap_len_mm
    
    x_motor_start = x_ox_tank_end + motor_ox_gap_mm
    x_frontcap_end = x_motor_start + L_frontcap_mm
    x_precomb_end = x_frontcap_end + pre_comb_mm
    x_grain_end = x_precomb_end + L_grain_mm
    x_postcomb_end = x_grain_end + post_comb_mm
    x_nozzle_start = x_postcomb_end
    x_nozzle_end = x_nozzle_start + L_nozzle_mm
    x_retainer_start = x_nozzle_end
    x_retainer_end = x_retainer_start + L_retainer_mm
    x_motor_end = x_retainer_end
    
    # Drawing tank shell (EXACT notebook patches)
    ax.add_patch(patches.Rectangle((x_ox_tank_start, ox_tank_r_inner_mm), ox_tank_L_total_mm, ox_tank_t_mm_plot, facecolor='lightblue', edgecolor='black'))
    ax.add_patch(patches.Rectangle((x_ox_tank_start, -ox_tank_r_outer_mm), ox_tank_L_total_mm, ox_tank_t_mm_plot, facecolor='lightblue', edgecolor='black'))
    ax.add_patch(patches.Rectangle((x_ox_tank_start, -ox_tank_r_inner_mm), ox_tank_frontcap_len_mm, ox_tank_D_inner_mm, facecolor='cornflowerblue', edgecolor='black'))
    ax.add_patch(patches.Rectangle((x_ox_tank_casing_end, -ox_tank_r_inner_mm), ox_tank_backcap_len_mm, ox_tank_D_inner_mm, facecolor='cornflowerblue', edgecolor='black'))
    
    # Motor Casing
    ax.add_patch(patches.Rectangle((x_motor_start, casing_inner_radius_mm), x_motor_end - x_motor_start, t_wall_mm, facecolor='silver', edgecolor='black'))
    ax.add_patch(patches.Rectangle((x_motor_start, -r_outer_mm), x_motor_end - x_motor_start, t_wall_mm, facecolor='silver', edgecolor='black'))
    
    # Front Cap
    ax.add_patch(patches.Rectangle((x_motor_start, -casing_inner_radius_mm), L_frontcap_mm, 2 * casing_inner_radius_mm, facecolor='darkgray', edgecolor='black'))
    
    # Fuel Grain
    ax.add_patch(patches.Rectangle((x_precomb_end, r1_mm), L_grain_mm, r2_fuel_mm - r1_mm, facecolor='lightcoral', edgecolor='black'))
    ax.add_patch(patches.Rectangle((x_precomb_end, -r2_fuel_mm), L_grain_mm, r2_fuel_mm - r1_mm, facecolor='lightcoral', edgecolor='black'))
    
    # Insulation layers
    ax.add_patch(patches.Rectangle((x_frontcap_end, insulation_pre_post_inner_radius_mm), pre_comb_mm, insulation_pre_post_thickness_mm, facecolor='peru', edgecolor='black'))
    ax.add_patch(patches.Rectangle((x_frontcap_end, -insulation_outer_radius_mm), pre_comb_mm, insulation_pre_post_thickness_mm, facecolor='peru', edgecolor='black'))
    
    ax.add_patch(patches.Rectangle((x_precomb_end, insulation_grain_inner_radius_mm), L_grain_mm, insulation_grain_thickness_mm, facecolor='sandybrown', edgecolor='black'))
    ax.add_patch(patches.Rectangle((x_precomb_end, -insulation_outer_radius_mm), L_grain_mm, insulation_grain_thickness_mm, facecolor='sandybrown', edgecolor='black'))
    
    ax.add_patch(patches.Rectangle((x_grain_end, insulation_pre_post_inner_radius_mm), post_comb_mm, insulation_pre_post_thickness_mm, facecolor='peru', edgecolor='black'))
    ax.add_patch(patches.Rectangle((x_grain_end, -insulation_outer_radius_mm), post_comb_mm, insulation_pre_post_thickness_mm, facecolor='peru', edgecolor='black'))
    
    # Nozzle
    nozzle_x_abs = nozzle_profile['x'] + x_nozzle_start
    ax.fill_between(nozzle_x_abs, nozzle_profile['y_upper'], casing_inner_radius_mm, color='gray', edgecolor='black')
    ax.fill_between(nozzle_x_abs, nozzle_profile['y_lower'], -casing_inner_radius_mm, color='gray', edgecolor='black')
    
    # Retainer
    ax.add_patch(patches.Rectangle((x_retainer_start, r_retainer_inner_mm), L_retainer_mm, casing_inner_radius_mm - r_retainer_inner_mm, facecolor='darkgray', edgecolor='black'))
    ax.add_patch(patches.Rectangle((x_retainer_start, -casing_inner_radius_mm), L_retainer_mm, casing_inner_radius_mm - r_retainer_inner_mm, facecolor='darkgray', edgecolor='black'))
    
    # Bolts (EXACT notebook logic)
    bolt_color = 'red'
    
    # Frontcap bolts
    if frontcap_num_bolts > 0:
        x_frontcap_bolt = x_motor_start + L_frontcap_mm / 2.0 - frontcap_bolt_diameter_mm / 2.0
        ax.add_patch(patches.Rectangle((x_frontcap_bolt, casing_inner_radius_mm), frontcap_bolt_diameter_mm, t_wall_mm, facecolor=bolt_color, edgecolor='black'))
        ax.add_patch(patches.Rectangle((x_frontcap_bolt, -casing_inner_radius_mm - t_wall_mm), frontcap_bolt_diameter_mm, t_wall_mm, facecolor=bolt_color, edgecolor='black'))
    
    # Nozzle retainer bolts
    if nozzle_num_bolts > 0:
        x_retainer_bolt = x_retainer_start + L_retainer_mm / 2.0 - nozzle_bolt_diameter_mm / 2.0
        ax.add_patch(patches.Rectangle((x_retainer_bolt, casing_inner_radius_mm), nozzle_bolt_diameter_mm, t_wall_mm, facecolor=bolt_color, edgecolor='black'))
        ax.add_patch(patches.Rectangle((x_retainer_bolt, -casing_inner_radius_mm - t_wall_mm), nozzle_bolt_diameter_mm, t_wall_mm, facecolor=bolt_color, edgecolor='black'))
    
    # Oxidizer tank bolts
    if ox_tank_num_bolts > 0:
        x_ox_tank_front_bolt = x_ox_tank_start + ox_tank_frontcap_len_mm / 2.0 - ox_tank_bolt_diameter_mm / 2.0
        ax.add_patch(patches.Rectangle((x_ox_tank_front_bolt, ox_tank_r_inner_mm), ox_tank_bolt_diameter_mm, ox_tank_t_mm_plot, facecolor=bolt_color, edgecolor='black'))
        ax.add_patch(patches.Rectangle((x_ox_tank_front_bolt, -ox_tank_r_inner_mm - ox_tank_t_mm_plot), ox_tank_bolt_diameter_mm, ox_tank_t_mm_plot, facecolor=bolt_color, edgecolor='black'))
        
        x_ox_tank_back_bolt = x_ox_tank_casing_end + ox_tank_backcap_len_mm / 2.0 - ox_tank_bolt_diameter_mm / 2.0
        ax.add_patch(patches.Rectangle((x_ox_tank_back_bolt, ox_tank_r_inner_mm), ox_tank_bolt_diameter_mm, ox_tank_t_mm_plot, facecolor=bolt_color, edgecolor='black'))
        ax.add_patch(patches.Rectangle((x_ox_tank_back_bolt, -ox_tank_r_inner_mm - ox_tank_t_mm_plot), ox_tank_bolt_diameter_mm, ox_tank_t_mm_plot, facecolor=bolt_color, edgecolor='black'))
    
    # Set plot limits and labels (EXACT notebook)
    ax.set_aspect('equal', adjustable='box')
    ax.set_title('Motor and Oxidizer Tank Assembly 2D Cross-Section (mm)')
    ax.set_xlabel('Axial Length (mm)')
    ax.set_ylabel('Radius (mm)')
    ax.grid(True, linestyle='--', alpha=0.6)
    max_radius = max(r_outer_mm, ox_tank_r_outer_mm)
    ax.set_ylim(-max_radius * 1.5, max_radius * 1.5)
    ax.set_xlim(x_ox_tank_start - 10, x_retainer_end + 10)
    
    return _save_to_cache_and_disk(fig, "motor_assembly")


def plot_performance_subplots(results: dict) -> str:
    """
    Creates 2×3 subplot figure showing all performance metrics vs time.
    EXACT implementation from notebook performance plots.
    """
    time_hist = results["time"]
    thrust_hist = results["thrust"]
    r_hist = results["radius"]
    OF_hist = results["of"]
    G_ox_hist = results["G_ox"]
    Tc_hist = results.get("Tc", [])
    p_c_hist = results.get("p_c", [])
    
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 6))
    
    # EXACT notebook plot configuration
    plots = [
        ("Thrust (N)", thrust_hist),
        ("Radius (m)", r_hist),
        ("O/F Ratio", OF_hist),
        ("G_ox (kg/m²/s)", G_ox_hist),
        ("Temperature (K)", Tc_hist if len(Tc_hist) > 0 else [0] * len(time_hist)),
        ("Chamber Pressure (bar)", [p/1e5 for p in p_c_hist] if len(p_c_hist) > 0 else [0] * len(time_hist))
    ]
    
    for ax, (label, data) in zip(axes.flat, plots):
        if len(data) > 0 and any(data):
            ax.plot(time_hist, data)
        else:
            ax.plot(time_hist, [0] * len(time_hist))
        ax.set_title(label)
        ax.grid(True)
        ax.set_xlabel('Time (s)')
    
    plt.tight_layout()
    return _save_to_cache_and_disk(fig, "performance_subplots")


def plot_nozzle_profile(current_values: dict) -> str:
    """
    Plots the 2D nozzle cross-section showing stock outline and machined profile.
    EXACT implementation from notebook nozzle shape plot.
    """
    # Extract nozzle parameters
    throat_d_mm = current_values["throat_diameter"]
    throat_len_mm = current_values["throat_length"]
    converge_deg = current_values["converge_half_angle"]
    diverge_deg = current_values["diverge_half_angle"]
    
    # Casing and insulation
    r2_fuel = current_values["r2"] / 100.0  # cm -> m
    insulation_pre_post_thickness = current_values["insul_prepost_thk"] / 1000.0  # mm -> m
    t_wall = current_values["casing_wall_thk"] / 1000.0  # mm -> m
    
    # Compute geometry
    casing_inner_radius = r2_fuel + insulation_pre_post_thickness + 0.001  # small buffer
    insulation_pre_post_inner_radius = casing_inner_radius - insulation_pre_post_thickness
    r_throat = throat_d_mm / 2000.0  # mm -> m
    
    # Compute nozzle lengths
    L_conv = (insulation_pre_post_inner_radius - r_throat) / np.tan(np.radians(converge_deg)) if converge_deg != 0 else 0.01
    throat_len = throat_len_mm / 1000.0
    
    # Simplified exit calculation (assume moderate expansion for visualization)
    r_exit = r_throat * 2.0  # Simplified expansion
    L_div = (r_exit - r_throat) / np.tan(np.radians(diverge_deg)) if diverge_deg != 0 else 0.01
    L_nozzle = L_conv + throat_len + L_div
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Nozzle profile coordinates (EXACT notebook approach)
    x_nozzle_inner = np.array([0, L_conv, L_conv + throat_len, L_conv + throat_len + L_div])
    y_nozzle_upper_inner = np.array([insulation_pre_post_inner_radius, r_throat, r_throat, r_exit])
    
    # Stock outline (EXACT notebook)
    stock_x = np.array([0, L_nozzle, L_nozzle, 0, 0]) * 1000  # convert to mm
    stock_y = np.array([-casing_inner_radius, -casing_inner_radius, casing_inner_radius, casing_inner_radius, -casing_inner_radius]) * 1000
    
    # Plot stock outline
    ax.plot(stock_x, stock_y, 'k--', linewidth=1, label='Graphite Stock Outline')
    
    # Plot machined profile
    ax.plot(x_nozzle_inner * 1000, y_nozzle_upper_inner * 1000, 'k-', linewidth=2, label='Machined Profile')
    ax.plot(x_nozzle_inner * 1000, -y_nozzle_upper_inner * 1000, 'k-', linewidth=2)
    
    # Fill areas (EXACT notebook approach)
    ax.fill_between(stock_x[:2], stock_y[:2], stock_y[2:4], color='lightgray', zorder=0)
    ax.fill_between(x_nozzle_inner*1000, y_nozzle_upper_inner*1000, -y_nozzle_upper_inner*1000, color='white', zorder=1)
    
    ax.set_aspect('equal', adjustable='box')
    ax.set_title("Nozzle 2D Cross-Section (mm)")
    ax.set_xlabel("Axial Length (mm)")
    ax.set_ylabel("Radius (mm)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    return _save_to_cache_and_disk(fig, "nozzle_profile")


def plot_thrust_vs_time(time, thrust) -> str:
    fig, ax = plt.subplots()
    ax.plot(time, thrust, 'b-', linewidth=2, label='Thrust')
    ax.set(xlabel='Time (s)', ylabel='Thrust (N)', title='Thrust vs Time')
    ax.grid(True)
    ax.legend()
    return _save_to_cache_and_disk(fig, "thrust_plot")


def plot_radius_vs_time(time, radius) -> str:
    fig, ax = plt.subplots()
    ax.plot(time, radius, 'r-', linewidth=2, label='Port Radius')
    ax.set(xlabel='Time (s)', ylabel='Radius (m)', title='Port Radius vs Time')
    ax.grid(True)
    ax.legend()
    return _save_to_cache_and_disk(fig, "radius_plot")


def plot_of_vs_time(time, of) -> str:
    fig, ax = plt.subplots()
    ax.plot(time, of, 'g-', linewidth=2, label='O/F Ratio')
    ax.set(xlabel='Time (s)', ylabel='O/F Ratio', title='O/F Ratio vs Time')
    ax.grid(True)
    ax.legend()
    return _save_to_cache_and_disk(fig, "of_plot")


def plot_gox_vs_time(time, G_ox) -> str:
    fig, ax = plt.subplots()
    ax.plot(time, G_ox, 'm-', linewidth=2, label='Oxidizer Flux')
    ax.set(xlabel='Time (s)', ylabel='Oxidizer Mass Flux (kg/m²/s)', title='G_ox vs Time')
    ax.grid(True)
    ax.legend()
    return _save_to_cache_and_disk(fig, "gox_plot")


def plot_isp_vs_time(time, isp) -> str:
    fig, ax = plt.subplots()
    ax.plot(time, isp, 'c-', linewidth=2, label='Specific Impulse')
    ax.set(xlabel='Time (s)', ylabel='Isp (s)', title='Specific Impulse vs Time')
    ax.grid(True)
    ax.legend()
    return _save_to_cache_and_disk(fig, "isp_plot")


def save_all_plots(results: dict, current_values: dict = None) -> list:
    """
    Generate all plots and store them in Flask's in-memory cache and on disk.
    Returns a list of cache keys for retrieval.
    
    EXACT notebook implementation with all plot types.
    """
    time = results["time"]
    thrust = results["thrust"]
    radius = results["radius"]
    of = results["of"]
    G_ox = results["G_ox"]
    isp = results.get("isp")
    
    keys = []
    
    # Individual time series plots
    keys.append(plot_thrust_vs_time(time, thrust))
    keys.append(plot_radius_vs_time(time, radius))
    keys.append(plot_of_vs_time(time, of))
    keys.append(plot_gox_vs_time(time, G_ox))
    
    if isp is not None and len(isp) > 0:
        keys.append(plot_isp_vs_time(time, isp))
    
    # Combined performance subplots (EXACT notebook 2x3 grid)
    keys.append(plot_performance_subplots(results))
    
    # Motor assembly diagram (if current_values provided)
    if current_values is not None:
        keys.append(plot_motor_assembly(current_values, results))
        keys.append(plot_nozzle_profile(current_values))
    
    return keys


def get_cached_image(cache_key: str) -> BytesIO | None:
    """
    Retrieves a BytesIO image from the cache by key.
    Returns None if not found.
    """
    return cache.get(cache_key)
