"""Create a transparent capacity-scenario chart for the investor pilot deck."""

from pathlib import Path

import matplotlib.pyplot as plt


SCENARIOS = {
    "Minimum\n3 × Founding": 4_500,
    "Core\n2 Founding + 2 Standard": 10_000,
    "Full cohort\n2 Founding + 2 Standard + 1 Extended": 15_000,
}


def main():
    output = Path("analysis_outputs/pilot_program/pilot_cohort_capacity_scenarios.png")
    output.parent.mkdir(parents=True, exist_ok=True)

    labels = list(SCENARIOS)
    values = list(SCENARIOS.values())
    figure, axis = plt.subplots(figsize=(10.5, 5.7))
    figure.patch.set_facecolor("#08111f")
    axis.set_facecolor("#08111f")
    bars = axis.bar(labels, values, color=["#38bdf8", "#f59e0b", "#22c55e"], width=0.62)
    axis.set_ylim(0, 17_000)
    axis.set_ylabel("Illustrative gross pilot fees (USD)", color="#e2e8f0")
    axis.set_title("Pilot capacity scenarios — experimental offer design, not revenue forecast", color="#f8fafc", fontsize=14, pad=14)
    axis.tick_params(axis="x", colors="#cbd5e1", labelsize=9)
    axis.tick_params(axis="y", colors="#cbd5e1")
    axis.grid(axis="y", color="#334155", alpha=0.6, linewidth=0.8)
    for spine in axis.spines.values():
        spine.set_visible(False)
    for bar, value in zip(bars, values):
        axis.text(bar.get_x() + bar.get_width() / 2, value + 450, f"${value:,.0f}", ha="center", va="bottom", color="#f8fafc", fontsize=11, fontweight="bold")
    axis.text(0.01, -0.20, "Source: LIMITED_PILOT_EXECUTION_AND_PRICING_PLAN_FA.md. Fees and package mix are unvalidated assumptions.", transform=axis.transAxes, color="#94a3b8", fontsize=8)
    figure.tight_layout()
    figure.savefig(output, dpi=190, facecolor=figure.get_facecolor(), bbox_inches="tight")
    print(output)


if __name__ == "__main__":
    main()
