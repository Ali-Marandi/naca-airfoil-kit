#!/usr/bin/env python3
"""Summarize Pareto-front percentage deltas from a Reynolds comparison CSV."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def as_float(row, key):
    return float(row[key])


def main():
    args = parse_args()
    with args.metrics.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    front_rows = [row for row in rows if row["airfoil"].startswith("Pareto front")]
    if not front_rows:
        raise SystemExit("No Pareto front records found.")
    front_by_re = {as_float(row, "reynolds"): row for row in front_rows}
    summary = {"per_reynolds": [], "aggregate": {}}
    for reynolds in sorted(front_by_re):
        front = front_by_re[reynolds]
        condition = {"reynolds": reynolds, "front_airfoil": front["airfoil"], "comparisons": []}
        for reference in [row for row in rows if as_float(row, "reynolds") == reynolds and not row["airfoil"].startswith("Pareto front")]:
            comparison = {"reference_airfoil": reference["airfoil"]}
            for metric in ("best_ld", "cl_max", "ld_at_design_alpha", "cl_at_design_alpha"):
                reference_value = as_float(reference, metric)
                front_value = as_float(front, metric)
                comparison[f"{metric}_front"] = front_value
                comparison[f"{metric}_reference"] = reference_value
                comparison[f"{metric}_delta_pct"] = ((front_value - reference_value) / reference_value * 100.0) if reference_value != 0 else None
            condition["comparisons"].append(comparison)
        summary["per_reynolds"].append(condition)
    for reference_name in sorted({row["airfoil"] for row in rows if not row["airfoil"].startswith("Pareto front")}):
        matching = [
            item for condition in summary["per_reynolds"] for item in condition["comparisons"] if item["reference_airfoil"] == reference_name
        ]
        summary["aggregate"][reference_name] = {
            "mean_best_ld_delta_pct": sum(item["best_ld_delta_pct"] for item in matching) / len(matching),
            "mean_cl_max_delta_pct": sum(item["cl_max_delta_pct"] for item in matching) / len(matching),
            "mean_ld_at_design_alpha_delta_pct": sum(item["ld_at_design_alpha_delta_pct"] for item in matching) / len(matching),
            "mean_cl_at_design_alpha_delta_pct": sum(item["cl_at_design_alpha_delta_pct"] for item in matching) / len(matching),
        }
    args.output.write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
