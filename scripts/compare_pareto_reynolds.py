#!/usr/bin/env python3
"""Compare the UIUC Pareto-front profile with standard NACA references across Reynolds.

All aerodynamic quantities are from the repository's preliminary panel/empirical
model. The script records real UIUC coordinate URLs but does not use experimental
polars, so its output is an engineering-screening comparison—not validation.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from airfoil_pro import AirfoilAnalysis, UIUCLoader  # noqa: E402


PROFILES = {
    "Pareto front — UIUC NACA6412": "https://m-selig.ae.illinois.edu/ads/coord/naca6412.dat",
    "Reference — UIUC NACA0012": "https://m-selig.ae.illinois.edu/ads/coord/n0012.dat",
    "Reference — UIUC NACA2412": "https://m-selig.ae.illinois.edu/ads/coord/naca2412.dat",
    "Reference — UIUC NACA4412": "https://m-selig.ae.illinois.edu/ads/coord/naca4412.dat",
}
DEFAULT_REYNOLDS = [50_000.0, 100_000.0, 250_000.0, 500_000.0, 1_000_000.0, 2_000_000.0]


def parse_args():
    parser = argparse.ArgumentParser(description="Compare a UIUC Pareto-front NACA profile with standard NACA references across Reynolds.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "analysis_outputs" / "pareto_reynolds_comparison")
    parser.add_argument("--roughness", type=float, default=0.0)
    parser.add_argument("--design-alpha", type=float, default=4.0)
    parser.add_argument("--alpha-start", type=float, default=-4.0)
    parser.add_argument("--alpha-end", type=float, default=12.0)
    parser.add_argument("--alpha-step", type=float, default=1.0)
    parser.add_argument("--reynolds", type=float, nargs="+", default=DEFAULT_REYNOLDS)
    return parser.parse_args()


def interpolate_metric(rows, alpha, key):
    row_alpha = np.asarray([row["alpha_deg"] for row in rows], dtype=float)
    row_values = np.asarray([row[key] for row in rows], dtype=float)
    return float(np.interp(alpha, row_alpha, row_values))


def build_rows(profile_coords, reynolds_values, alpha_values, design_alpha, roughness):
    records = []
    for profile_name, coords in profile_coords.items():
        for reynolds in reynolds_values:
            polar = AirfoilAnalysis.compute_polar(*coords, alpha_values, re=float(reynolds), rough=float(roughness))
            summary = AirfoilAnalysis.summarize_polar(polar["rows"])
            records.append(
                {
                    "airfoil": profile_name,
                    "reynolds": float(reynolds),
                    "best_ld": float(summary["best_ld"]),
                    "best_ld_alpha_deg": float(summary["best_alpha_deg"]),
                    "cl_max": float(summary["cl_max"]),
                    "cd_min": float(summary["cd_min"]),
                    "design_alpha_deg": float(design_alpha),
                    "cl_at_design_alpha": interpolate_metric(polar["rows"], design_alpha, "cl"),
                    "cd_at_design_alpha": interpolate_metric(polar["rows"], design_alpha, "cd"),
                    "ld_at_design_alpha": interpolate_metric(polar["rows"], design_alpha, "ld"),
                }
            )
    return records


def plot_comparison(rows, output_path):
    metrics = [
        ("best_ld", "Maximum L/D over envelope"),
        ("cl_max", "Maximum Cl over envelope"),
        ("cd_at_design_alpha", "Cd at design alpha"),
        ("ld_at_design_alpha", "L/D at design alpha"),
    ]
    profile_names = list(dict.fromkeys(row["airfoil"] for row in rows))
    figure, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
    color_map = plt.get_cmap("tab10")
    for axis, (metric, label) in zip(axes.ravel(), metrics):
        for index, profile_name in enumerate(profile_names):
            subset = [row for row in rows if row["airfoil"] == profile_name]
            re_values = [row["reynolds"] for row in subset]
            metric_values = [row[metric] for row in subset]
            linestyle = "-" if profile_name.startswith("Pareto") else "--"
            axis.plot(re_values, metric_values, marker="o", linewidth=2.1, linestyle=linestyle, color=color_map(index), label=profile_name.replace("UIUC ", ""))
        axis.set_xscale("log")
        axis.set_xlabel("Reynolds number")
        axis.set_ylabel(label)
        axis.grid(True, which="both", alpha=0.28)
    axes[0, 0].legend(fontsize=8, loc="best")
    figure.suptitle("Preliminary Reynolds comparison: Pareto-front profile vs standard NACA references", fontsize=14)
    figure.savefig(output_path, dpi=180)
    plt.close(figure)


def write_outputs(output_dir, rows, settings):
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "pareto_reynolds_metrics.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    chart_path = output_dir / "pareto_reynolds_comparison.png"
    plot_comparison(rows, chart_path)
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "study_scope": "Preliminary panel/empirical screening only; not a viscous CFD or wind-tunnel validation result.",
        "pareto_front_source": "analysis_outputs/pareto_uiuc_catalog/pareto_uiuc_manifest.json",
        "profile_sources": PROFILES,
        "settings": settings,
        "metrics_csv": csv_path.name,
        "chart": chart_path.name,
    }
    (output_dir / "pareto_reynolds_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main():
    args = parse_args()
    if args.alpha_end <= args.alpha_start or args.alpha_step <= 0:
        raise SystemExit("alpha-end must exceed alpha-start and alpha-step must be positive.")
    alpha_values = np.arange(args.alpha_start, args.alpha_end + 0.5 * args.alpha_step, args.alpha_step)
    if not alpha_values.min() <= args.design_alpha <= alpha_values.max():
        raise SystemExit("design-alpha must fall inside the alpha envelope.")
    profile_coords = {}
    failed = []
    for name, url in PROFILES.items():
        coords = UIUCLoader.load_from_url(url)
        if coords is None:
            failed.append(name)
        else:
            profile_coords[name] = coords
    if failed:
        raise SystemExit(f"Unable to load required UIUC profiles: {', '.join(failed)}")
    rows = build_rows(profile_coords, args.reynolds, alpha_values, args.design_alpha, args.roughness)
    settings = {
        "reynolds": [float(value) for value in args.reynolds],
        "roughness_k_over_c": float(args.roughness),
        "alpha_values_deg": [float(value) for value in alpha_values],
        "design_alpha_deg": float(args.design_alpha),
    }
    write_outputs(args.output_dir, rows, settings)
    print(json.dumps({"profiles": len(profile_coords), "conditions": len(rows), "output_dir": str(args.output_dir)}, indent=2))


if __name__ == "__main__":
    main()
