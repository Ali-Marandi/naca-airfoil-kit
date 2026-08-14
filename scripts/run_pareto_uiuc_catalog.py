#!/usr/bin/env python3
"""Run a reproducible Pareto study over a curated real UIUC NACA profile catalog.

The script deliberately uses a bounded, named catalog instead of downloading the
full UIUC index. This makes the integration check repeatable, avoids bulk load on
the public source, and records every profile URL used in the output manifest.
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

from airfoil_pro import ParetoExplorer, UIUCLoader  # noqa: E402


DEFAULT_PROFILE_NAMES = [
    "naca0006.dat", "naca0008.dat", "naca0010.dat", "naca0015.dat", "naca0018.dat", "naca0021.dat", "naca0024.dat",
    "naca1408.dat", "naca1410.dat", "naca1412.dat",
    "naca2408.dat", "naca2410.dat", "naca2411.dat", "naca2412.dat", "naca2415.dat", "naca2418.dat", "naca2421.dat", "naca2424.dat",
    "naca4412.dat", "naca4415.dat", "naca4418.dat", "naca4421.dat", "naca4424.dat", "naca6412.dat",
]


def parse_args():
    parser = argparse.ArgumentParser(description="Run preliminary L/D–Cl Pareto screening against a curated UIUC NACA catalog.")
    parser.add_argument("--catalog", type=Path, default=ROOT / "uiuc_database.json")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "analysis_outputs" / "pareto_uiuc_catalog")
    parser.add_argument("--reynolds", type=float, default=1_000_000.0)
    parser.add_argument("--roughness", type=float, default=0.0)
    parser.add_argument("--alpha-start", type=float, default=-4.0)
    parser.add_argument("--alpha-end", type=float, default=12.0)
    parser.add_argument("--alpha-step", type=float, default=1.0)
    parser.add_argument("--design-alpha", type=float, default=None, help="If supplied, optimize Cl at this alpha instead of maximum Cl.")
    return parser.parse_args()


def load_catalog(catalog_path: Path):
    entries = json.loads(catalog_path.read_text(encoding="utf-8"))
    lookup = {entry["name"].lower(): entry["url"] for entry in entries if "name" in entry and "url" in entry}
    selected, missing = {}, []
    for name in DEFAULT_PROFILE_NAMES:
        url = lookup.get(name)
        if url is None:
            missing.append(name)
            continue
        coords = UIUCLoader.load_from_url(url)
        if coords is not None:
            selected[f"UIUC {name[:-4].upper()}"] = {"coords": coords, "url": url}
    return selected, missing


def write_outputs(output_dir: Path, study: dict, sources: dict, failures: list[str]):
    output_dir.mkdir(parents=True, exist_ok=True)
    ranks_path = output_dir / "pareto_uiuc_rankings.csv"
    rows = study["rankings"]
    with ranks_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    front = [row for row in rows if row["pareto_front"]]
    figure, axis = plt.subplots(figsize=(9, 5.4))
    dominated = [row for row in rows if not row["pareto_front"]]
    if dominated:
        axis.scatter([row["cl_objective"] for row in dominated], [row["best_ld"] for row in dominated], color="#94a3b8", s=44, label="Dominated candidate")
    axis.scatter([row["cl_objective"] for row in front], [row["best_ld"] for row in front], color="#f97316", edgecolor="#7c2d12", s=76, label="Pareto front", zorder=3)
    for row in front:
        axis.annotate(row["airfoil"].replace("UIUC ", ""), (row["cl_objective"], row["best_ld"]), xytext=(4, 4), textcoords="offset points", fontsize=8)
    axis.set(title="Preliminary UIUC NACA catalog: L/D–Cl Pareto screening", xlabel=study["objective"]["cl"], ylabel=study["objective"]["ld"])
    axis.grid(alpha=0.25)
    axis.legend(loc="best")
    figure.tight_layout()
    figure.savefig(output_dir / "pareto_uiuc_catalog.png", dpi=180)
    plt.close(figure)

    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "study_scope": "Preliminary panel/empirical screen only; not a validated viscous or wind-tunnel result.",
        "objective": study["objective"],
        "requested_profile_count": len(DEFAULT_PROFILE_NAMES),
        "loaded_profile_count": len(sources),
        "failed_or_missing_profiles": failures,
        "sources": sources,
        "pareto_front": [row["airfoil"] for row in front],
        "ranking_csv": ranks_path.name,
        "chart": "pareto_uiuc_catalog.png",
    }
    (output_dir / "pareto_uiuc_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main():
    args = parse_args()
    if args.alpha_end <= args.alpha_start or args.alpha_step <= 0:
        raise SystemExit("alpha-end must exceed alpha-start and alpha-step must be positive.")
    profiles, missing = load_catalog(args.catalog)
    if len(profiles) < 3:
        raise SystemExit("Fewer than three UIUC profiles loaded; check connectivity and catalog availability.")
    alpha_values = np.arange(args.alpha_start, args.alpha_end + 0.5 * args.alpha_step, args.alpha_step)
    geometries = {name: value["coords"] for name, value in profiles.items()}
    objective = "cl_at_design_alpha" if args.design_alpha is not None else "cl_max"
    study = ParetoExplorer.screen_geometries(
        geometries,
        alpha_values,
        re=args.reynolds,
        rough=args.roughness,
        cl_objective=objective,
        design_alpha_deg=args.design_alpha,
    )
    source_metadata = {name: {"url": value["url"]} for name, value in profiles.items()}
    failed = missing + [name for name in DEFAULT_PROFILE_NAMES if f"UIUC {name[:-4].upper()}" not in profiles and name not in missing]
    write_outputs(args.output_dir, study, source_metadata, failed)
    front_names = [row["airfoil"] for row in study["rankings"] if row["pareto_front"]]
    print(json.dumps({"loaded_profiles": len(profiles), "pareto_front": front_names, "output_dir": str(args.output_dir)}, indent=2))


if __name__ == "__main__":
    main()
