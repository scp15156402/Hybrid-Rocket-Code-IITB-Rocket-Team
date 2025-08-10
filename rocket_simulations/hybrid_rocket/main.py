# hybrid_rocket/main.py
"""
Reader-friendly CLI for the Hybrid Rocket Simulation (terminal only).

- Builds current_values from slider_config & dropdown_config defaults
- Allows overriding via --<key> command-line args or --params-file (JSON)
- Runs simulate_burn, prints a clear, human-readable summary with sections
- Performs structural checks and prints safety warnings
- Saves plots (via save_all_plots) and can export CSV
- No GUI; output is optimized for console reading
"""

from __future__ import annotations
import argparse
import json
import sys
import traceback
from typing import Any, Dict

from hybrid_rocket.solver import simulate_burn
from hybrid_rocket.plots import save_all_plots
from hybrid_rocket.export import (
    export_simulation_data,
    print_summary,
    compute_structural_metrics,
    get_summary_dict,
)
from hybrid_rocket.slider_config import slider_config, dropdown_config


# ---------------------------
# Console formatting helpers
# ---------------------------
ANSI_ENABLED = True  # default; can be disabled via CLI


def color_wrap(text: str, code: str) -> str:
    if not ANSI_ENABLED:
        return text
    return f"\033[{code}m{text}\033[0m"


def header(title: str) -> str:
    return color_wrap(f"\n=== {title} ===", "1;34")  # bold blue


def subheader(title: str) -> str:
    return color_wrap(f"\n--- {title} ---", "1;33")  # bold yellow


def ok(text: str) -> str:
    return color_wrap(text, "32")  # green


def err(text: str) -> str:
    return color_wrap(text, "31")  # red


def note(text: str) -> str:
    return color_wrap(text, "36")  # cyan


def fmt_num(x: Any, precision: int = 3) -> str:
    try:
        if isinstance(x, int):
            return str(x)
        f = float(x)
        # Choose compact formatting
        if abs(f) >= 1e5 or (0 < abs(f) < 1e-3):
            return f"{f:.{precision}e}"
        else:
            return f"{f:.{precision}f}".rstrip("0").rstrip(".")
    except Exception:
        return str(x)


def format_sequence(seq, max_items: int = 10) -> str:
    # Convert sequence (list/tuple/ndarray) to compact string
    try:
        length = len(seq)
        if length == 0:
            return "[]"
        if length <= max_items:
            return "[" + ", ".join(fmt_num(v) for v in seq) + "]"
        # show head ... tail
        head = ", ".join(fmt_num(v) for v in seq[: max_items // 2])
        tail = ", ".join(fmt_num(v) for v in seq[-(max_items // 2) :])
        return f"[{head}, ..., {tail}] (len={length})"
    except Exception:
        return str(seq)


def pretty_print_dict(d: dict, indent: int = 0) -> None:
    pad = " " * (indent * 2)
    if not isinstance(d, dict):
        print(pad + str(d))
        return
    for k, v in d.items():
        key_str = f"{pad}{k}:"
        if isinstance(v, dict):
            print(key_str)
            pretty_print_dict(v, indent + 1)
        elif isinstance(v, (list, tuple)):
            print(f"{key_str} {format_sequence(v)}")
        elif isinstance(v, (int, float)):
            print(f"{key_str} {fmt_num(v)}")
        else:
            print(f"{key_str} {v}")


# ---------------------------
# CLI building & helpers
# ---------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Hybrid Rocket Motor Simulation — Reader-friendly CLI"
    )

    # Generic flags
    parser.add_argument(
        "--params-file",
        type=str,
        default=None,
        help="Path to JSON file with parameter overrides (key: value).",
    )
    parser.add_argument(
        "--list-defaults",
        action="store_true",
        help="Print default parameters and exit.",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI color output.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print verbose/debug messages.",
    )

    # Output / behaviour flags
    parser.add_argument(
        "--export",
        action="store_true",
        help="Export results to CSV after simulation.",
    )
    parser.add_argument(
        "--out-csv",
        type=str,
        default=None,
        help="Filename for CSV export when --export is used.",
    )
    parser.add_argument(
        "--detailed",
        action="store_true",
        help="Show detailed structural analysis.",
    )
    parser.add_argument(
        "--warnings",
        action="store_true",
        help="Print detected safety warnings separately.",
    )
    parser.add_argument(
        "--plot-info",
        action="store_true",
        help="Print list of generated plot keys/filenames.",
    )

    # Add dynamic args for sliders (floats)
    for key, meta in slider_config.items():
        default = meta.get("default")
        help_text = meta.get("help", f"Slider parameter {key}")
        parser.add_argument(
            f"--{key}",
            type=float,
            default=None,
            help=f"{help_text} (default: {default})",
        )

    # Add dynamic args for dropdowns (strings)
    for key, meta in dropdown_config.items():
        default = meta.get("default")
        help_text = meta.get("help", f"Dropdown parameter {key}")
        parser.add_argument(
            f"--{key}",
            type=str,
            default=None,
            help=f"{help_text} (default: {default})",
        )

    return parser


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("params-file must contain a JSON object of key: value pairs.")
    return data


def build_current_values(ns: argparse.Namespace, params_file: dict | None) -> dict:
    # Start with defaults
    current_values = {k: v["default"] for k, v in slider_config.items()}
    current_values.update({k: v["default"] for k, v in dropdown_config.items()})

    # Overlay params file (if provided)
    if params_file:
        for k, v in params_file.items():
            if k in current_values:
                current_values[k] = v
            else:
                print(note(f"Warning: unknown key in params file '{k}' — ignored"))

    # Overlay CLI explicit args
    for k in slider_config.keys():
        val = getattr(ns, k, None)
        if val is not None:
            current_values[k] = float(val)

    for k in dropdown_config.keys():
        val = getattr(ns, k, None)
        if val is not None:
            current_values[k] = val

    return current_values


# ---------------------------
# Simulation & printing
# ---------------------------


def run_simulation(current_values: dict, verbose: bool = False) -> dict:
    # Extract commonly used args (defensive)
    results = simulate_burn(
        r1=current_values.get("r1"),
        r2=current_values.get("r2"),
        L=current_values.get("L"),
        mdot_ox=current_values.get("mdot_ox"),
        rho_fuel=current_values.get("rho_fuel"),
        current_values=current_values,
    )
    if verbose:
        print(note("Simulation finished; results keys: ") + ", ".join(sorted(results.keys())))
    return results


def collect_warnings_and_struct(current_values: dict, results: dict) -> (list, dict):
    warnings = []
    # chamber pressure array
    p_c = results.get("p_c", [])
    low_warn = results.get("low_pressure_warning", False)

    # Peak pressure check
    try:
        if isinstance(p_c, (list, tuple)) and len(p_c) > 0:
            max_pc = max(p_c)
            if max_pc > 40e5:
                warnings.append("Peak chamber pressure exceeds 40 bar")
    except Exception:
        # ignore array errors
        pass

    if low_warn:
        warnings.append("Chamber pressure dropped below 2 bar")

    struct = {}
    try:
        struct = compute_structural_metrics(current_values, results)
        if isinstance(p_c, (list, tuple)) and len(p_c) > 0:
            try:
                if max(p_c) > struct.get("max_pressure_design_casing", float("inf")):
                    warnings.append("Chamber pressure exceeds casing design pressure")
            except Exception:
                pass
        if struct.get("n2o_vapor_pressure", 0) > struct.get("max_pressure_design_ox_tank", float("inf")):
            warnings.append("N₂O vapor pressure exceeds tank design pressure")
    except Exception as e:
        warnings.append(f"Structural check failed: {e}")

    return warnings, struct


def pretty_cli_output(current_values: dict, results: dict, summary: dict, struct: dict, warnings: list, args: argparse.Namespace):
    # Header
    print(header("HYBRID ROCKET SIMULATION"))

    # Configuration block (aligned)
    print(subheader("Configuration (inputs)"))
    # Determine column width
    max_k_len = max((len(k) for k in current_values.keys()), default=10)
    for k in sorted(current_values.keys()):
        v = current_values[k]
        if isinstance(v, (list, tuple)):
            vstr = format_sequence(v)
        elif isinstance(v, (int, float)):
            vstr = fmt_num(v)
        else:
            vstr = str(v)
        print(f"  {k.ljust(max_k_len)} : {vstr}")

    # Summary block
    print(subheader("Simulation Summary"))
    if isinstance(summary, dict):
        pretty_print_dict(summary, indent=1)
    else:
        # fallback to whatever string print_summary returns
        print("  " + str(summary))

    # Structural block (if available or requested)
    if args.detailed:
        print(subheader("Detailed Structural Analysis"))
        if struct:
            pretty_print_dict(struct, indent=1)
        else:
            print("  No structural metrics available.")

    # Warnings
    if warnings:
        print(subheader("Safety Warnings"))
        for i, w in enumerate(warnings, 1):
            print(err(f"  [{i}] {w}"))
    else:
        if args.warnings:
            print(subheader("Safety Warnings"))
            print(ok("  No safety warnings detected."))

    # Other useful numbers (compact)
    try:
        if "time" in results and len(results["time"]) > 0:
            t_last = results["time"][-1]
            print(subheader("Run Metrics"))
            print(f"  Burn time           : {fmt_num(t_last)} s")
            print(f"  Total impulse       : {results.get('total_impulse', 'N/A')}")
            print(f"  Data points         : {len(results['time'])}")
            # Print peak chamber pressure and temperature if present
            if "p_c" in results and len(results["p_c"]) > 0:
                print(f"  Peak chamber press. : {fmt_num(max(results['p_c']))} Pa ({fmt_num(max(results['p_c'])/1e5)} bar)")
            if "Tc" in results and len(results["Tc"]) > 0:
                print(f"  Peak combustion temp: {fmt_num(max(results['Tc']))} K")
    except Exception:
        # defensive fail-safe
        pass


def main():
    global ANSI_ENABLED

    parser = build_parser()
    args = parser.parse_args()
    if args.no_color:
        ANSI_ENABLED = False

    # Print defaults and exit
    if args.list_defaults:
        defaults = {**{k: v["default"] for k, v in slider_config.items()},
                    **{k: v["default"] for k, v in dropdown_config.items()}}
        print(json.dumps(defaults, indent=2, sort_keys=True))
        return

    params_file_dict = None
    if args.params_file:
        try:
            params_file_dict = load_json(args.params_file)
        except Exception as e:
            print(err(f"Error reading params file: {e}"), file=sys.stderr)
            sys.exit(2)

    try:
        current_values = build_current_values(args, params_file=params_file_dict)

        # Announce run
        print(note("Starting simulation..."))
        if args.verbose:
            print(note("Current values (preview):"))
            for k in sorted(current_values.keys())[:20]:
                print(f"  {k} = {current_values[k]}")

        # Run simulation
        results = run_simulation(current_values, verbose=args.verbose)

        # Build summary dict (try structured, fallback to print_summary string)
        try:
            summary = get_summary_dict(results, current_values)
        except Exception:
            try:
                summary_text = print_summary(results, current_values)
                summary = {"Summary": summary_text}
            except Exception:
                summary = {"Summary": "Could not build summary."}

        # Structural checks and warnings
        warnings, struct = collect_warnings_and_struct(current_values, results)

        # Print nicely formatted output
        pretty_cli_output(current_values, results, summary, struct, warnings, args)

        # Generate plots (saved by implementation)
        try:
            plot_keys = save_all_plots(results, current_values)
            if args.plot_info:
                print(subheader("Plots"))
                print(f"  Generated {len(plot_keys)} plot keys/files:")
                for pk in plot_keys:
                    print(f"    - {pk}")
        except Exception as e:
            print(err(f"Error generating plots: {e}"))

        # Export CSV if requested
        if args.export:
            filename = args.out_csv or f"hybrid_rocket_simulation_{current_values.get('r1')}_to_{current_values.get('r2')}.csv"
            try:
                export_simulation_data(results, filename)
                print(ok(f"Exported CSV to: {filename}"))
            except Exception as e:
                print(err(f"CSV export failed: {e}"))

        print(ok("\nSimulation complete."))

    except Exception as e:
        print(err("Simulation failed with an error:"))
        traceback.print_exc()
        print("\n" + note("Advice: please check your input parameters and try again."))
        sys.exit(1)


if __name__ == "__main__":
    main()
