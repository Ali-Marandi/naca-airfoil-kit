#!/usr/bin/env python3
"""Run a Reynolds-aware robust Pareto screen for the curated UIUC NACA catalog.

The solver is the project's panel/empirical preliminary-screening model. UIUC
coordinates provide real geometry provenance, but this runner does not claim
validated viscous or wind-tunnel performance.
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

from airfoil_pro import ParetoExplorer  # noqa: E402
from run_pareto_uiuc_catalog import DEFAULT_PROFILE_NAMES, load_catalog  # noqa: E402


DEFAULT_REYNOLDS = [100_000.0, 250_000.0, 500_000.0, 1_000_000.0, 2_000_000.0]


def parse_reynolds(raw: str) -> list[float]:
    try:
        values = sorted({float(value.strip()) for value in raw.split(",") if value.strip()})
    except ValueError as error:
        raise argparse.ArgumentTypeError("Reynolds values must be comma-separated numbers.") from error
    if len(values) < 2 or any(value <= 0.0 for value in values):
        raise argparse.ArgumentTypeError("Provide at least two distinct positive Reynolds values.")
    return values


def parse_args():
    parser = argparse.ArgumentParser(description="Run robust multi-Re Pareto screening against the curated UIUC NACA catalog.")
    parser.add_argument("--catalog", type=Path, default=ROOT / "uiuc_database.json")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "analysis_outputs" / "pareto_multi_re")
    parser.add_argument("--reynolds", type=parse_reynolds, default=DEFAULT_REYNOLDS, help="Comma-separated Reynolds values.")
    parser.add_argument("--roughness", type=float, default=0.0)
    parser.add_argument("--alpha-start", type=float, default=-4.0)
    parser.add_argument("--alpha-end", type=float, default=12.0)
    parser.add_argument("--alpha-step", type=float, default=1.0)
    parser.add_argument("--design-alpha", type=float, default=4.0, help="Lift objective is Cl evaluated at this alpha in degrees.")
    return parser.parse_args()


def flatten_rankings(rankings: list[dict]) -> list[dict]:
    flattened = []
    for ranking in rankings:
        row = {key: value for key, value in ranking.items() if key != "per_re_metrics"}
        flattened.append(row)
    return flattened


def condition_rows(rankings: list[dict]) -> list[dict]:
    rows = []
    for ranking in rankings:
        for metric in ranking["per_re_metrics"]:
            rows.append(
                {
                    "airfoil": ranking["airfoil"],
                    "pareto_rank": ranking["pareto_rank"],
                    "pareto_front": ranking["pareto_front"],
                    "reynolds": metric["reynolds"],
                    "best_ld": metric["best_ld"],
                    "best_ld_alpha_deg": metric["best_ld_alpha_deg"],
                    "cl_objective": metric["cl_objective"],
                    "cl_max": metric["cl_max"],
                    "cd_min": metric["cd_min"],
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict]):
    if not rows:
        raise ValueError(f"No rows available for {path.name}.")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_chart(output_dir: Path, rankings: list[dict], study: dict):
    front = [row for row in rankings if row["pareto_front"]]
    dominated = [row for row in rankings if not row["pareto_front"]]
    figure, axes = plt.subplots(1, 2, figsize=(13.0, 5.3), layout="constrained")

    for rows, color, label, zorder in (
        (dominated, "#94a3b8", "Dominated in robust multi-Re comparison", 2),
        (front, "#f97316", "Robust Pareto front", 3),
    ):
        if rows:
            axes[0].scatter(
                [row["mean_cl_objective"] for row in rows],
                [row["mean_best_ld"] for row in rows],
                color=color,
                edgecolor="#7c2d12" if label == "Robust Pareto front" else "none",
                s=78 if label == "Robust Pareto front" else 42,
                label=label,
                zorder=zorder,
            )
            axes[1].scatter(
                [row["worst_case_best_ld"] for row in rows],
                [row["best_ld_std"] for row in rows],
                color=color,
                edgecolor="#7c2d12" if label == "Robust Pareto front" else "none",
                s=78 if label == "Robust Pareto front" else 42,
                label=label,
                zorder=zorder,
            )

    for row in front:
        label = row["airfoil"].replace("UIUC ", "")
        axes[0].annotate(label, (row["mean_cl_objective"], row["mean_best_ld"]), xytext=(4, 4), textcoords="offset points", fontsize=8)
        axes[1].annotate(label, (row["worst_case_best_ld"], row["best_ld_std"]), xytext=(4, 4), textcoords="offset points", fontsize=8)

    axes[0].set(
        title="Mean screening performance across Reynolds conditions",
        xlabel=f"Mean {study['objective']['cl']}",
        ylabel="Mean maximum L/D",
    )
    axes[1].set(
        title="Robustness diagnostics (not the rank definition)",
        xlabel="Worst-case maximum L/D",
        ylabel="Standard deviation of maximum L/D (lower is steadier)",
    )
    for axis in axes:
        axis.grid(alpha=0.25)
        axis.legend(loc="best", fontsize=8)
    figure.suptitle("Preliminary UIUC NACA catalog — robust Pareto screen across Reynolds conditions", fontsize=12, fontweight="bold")
    figure.savefig(output_dir / "pareto_multi_re.png", dpi=180, bbox_inches="tight")
    plt.close(figure)


def write_outputs(output_dir: Path, study: dict, sources: dict, failures: list[str], args):
    output_dir.mkdir(parents=True, exist_ok=True)
    rankings = study["rankings"]
    flat_rows = flatten_rankings(rankings)
    by_condition = condition_rows(rankings)
    rankings_path = output_dir / "pareto_multi_re_rankings.csv"
    conditions_path = output_dir / "pareto_multi_re_condition_metrics.csv"
    write_csv(rankings_path, flat_rows)
    write_csv(conditions_path, by_condition)
    write_chart(output_dir, rankings, study)

    front = [row for row in rankings if row["pareto_front"]]
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "study_scope": "Preliminary panel/empirical screen only; not a validated viscous or wind-tunnel result.",
        "method": {
            "robust_pareto_definition": study["objective"]["pareto_definition"],
            "aggregate_metrics": "mean and worst-case L/D plus L/D standard deviation are descriptive metrics; the rank uses all per-Re L/D and lift objectives.",
            "lift_objective": study["objective"]["cl"],
            "roughness_k_over_c": args.roughness,
            "alpha_values_deg": study["objective"]["alpha_values_deg"],
            "design_alpha_deg": args.design_alpha,
        },
        "reynolds_values": study["objective"]["reynolds_values"],
        "requested_profile_count": len(DEFAULT_PROFILE_NAMES),
        "loaded_profile_count": len(sources),
        "failed_or_missing_profiles": failures,
        "sources": sources,
        "robust_pareto_front": [row["airfoil"] for row in front],
        "ranking_csv": rankings_path.name,
        "condition_metrics_csv": conditions_path.name,
        "chart": "pareto_multi_re.png",
        "limitations": [
            "Geometry coordinates originate from UIUC sources; aerodynamic metrics use this repository's lightweight panel/empirical screening model.",
            "The model does not provide a validated viscous boundary-layer, transition, separation, or post-stall prediction.",
            "Results rank this exact candidate set and operating envelope only; they are not a design release, safety margin, or certification input.",
        ],
    }
    summary = {
        "robust_pareto_front": [row["airfoil"] for row in front],
        "front_metrics": [
            {
                "airfoil": row["airfoil"],
                "mean_best_ld": row["mean_best_ld"],
                "worst_case_best_ld": row["worst_case_best_ld"],
                "best_ld_std": row["best_ld_std"],
                "mean_cl_objective": row["mean_cl_objective"],
                "worst_case_cl_objective": row["worst_case_cl_objective"],
            }
            for row in front
        ],
    }
    (output_dir / "pareto_multi_re_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (output_dir / "pareto_multi_re_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main():
    args = parse_args()
    if args.alpha_end <= args.alpha_start or args.alpha_step <= 0.0:
        raise SystemExit("alpha-end must exceed alpha-start and alpha-step must be positive.")
    if not args.alpha_start <= args.design_alpha <= args.alpha_end:
        raise SystemExit("design-alpha must lie inside the supplied alpha envelope.")
    profiles, missing = load_catalog(args.catalog)
    if len(profiles) < 3:
        raise SystemExit("Fewer than three UIUC profiles loaded; check connectivity and catalog availability.")
    alpha_values = np.arange(args.alpha_start, args.alpha_end + 0.5 * args.alpha_step, args.alpha_step)
    study = ParetoExplorer.screen_geometries_multi_re(
        {name: value["coords"] for name, value in profiles.items()},
        alpha_values,
        args.reynolds,
        rough=args.roughness,
        cl_objective="cl_at_design_alpha",
        design_alpha_deg=args.design_alpha,
    )
    source_metadata = {name: {"url": value["url"]} for name, value in profiles.items()}
    failed = missing + [name for name in DEFAULT_PROFILE_NAMES if f"UIUC {name[:-4].upper()}" not in profiles and name not in missing]
    write_outputs(args.output_dir, study, source_metadata, failed, args)
    print(
        json.dumps(
            {
                "loaded_profiles": len(profiles),
                "robust_pareto_front": [row["airfoil"] for row in study["rankings"] if row["pareto_front"]],
                "output_dir": str(args.output_dir),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
