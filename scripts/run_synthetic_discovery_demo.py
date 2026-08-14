"""Generate a clearly labeled synthetic discovery-analysis demonstration.

This script uses hand-authored hypothetical records. It must never be used as
customer evidence, traction, pricing validation, or investment evidence.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


OUTPUT_DIR = Path("analysis_outputs/synthetic_discovery_demo")
DATA_STATUS = "SYNTHETIC_DEMO_NOT_CUSTOMER_EVIDENCE"


RECORDS = [
    {
        "interview_id": "INT-01", "segment": "Small UAS design team", "role": "Technical founder",
        "team_size_band": "2-10", "timeline": 30, "frequency": "monthly", "pain": 5,
        "consequence": "Client review is delayed when analyses cannot be reproduced.", "data_ready": "yes",
        "buyer": "yes", "price": 3500, "reaction": "accept", "objection": "trust_accuracy",
        "package": "strong", "eligibility": 5, "status": "pilot_candidate",
        "scores": [2, 2, 2, 2, 2, 2], "offer": "Standard Evidence Pilot",
    },
    {
        "interview_id": "INT-02", "segment": "Rotor startup", "role": "Lead engineer",
        "team_size_band": "11-25", "timeline": 45, "frequency": "weekly", "pain": 5,
        "consequence": "Shortlist decisions are reworked before management reviews.", "data_ready": "yes",
        "buyer": "yes", "price": 5000, "reaction": "conditional_accept", "objection": "scope_mismatch",
        "package": "strong", "eligibility": 5, "status": "pilot_candidate",
        "scores": [2, 2, 2, 2, 2, 1], "offer": "Extended Workflow Pilot",
    },
    {
        "interview_id": "INT-03", "segment": "Aero design consultancy", "role": "Principal consultant",
        "team_size_band": "2-10", "timeline": 21, "frequency": "weekly", "pain": 4,
        "consequence": "Manual report assembly consumes billable review time.", "data_ready": "yes",
        "buyer": "yes", "price": 3500, "reaction": "accept", "objection": "none",
        "package": "strong", "eligibility": 5, "status": "pilot_candidate",
        "scores": [2, 2, 2, 2, 2, 1], "offer": "Standard Evidence Pilot",
    },
    {
        "interview_id": "INT-04", "segment": "Applied research laboratory", "role": "Research lead",
        "team_size_band": "11-25", "timeline": 60, "frequency": "monthly", "pain": 3,
        "consequence": "Metadata is inconsistent across student studies.", "data_ready": "partial",
        "buyer": "unknown", "price": 1500, "reaction": "consider", "objection": "budget",
        "package": "moderate", "eligibility": 4, "status": "follow_up",
        "scores": [1, 1, 1, 1, 2, 2], "offer": "Founding Design Partner",
    },
    {
        "interview_id": "INT-05", "segment": "Small UAS design team", "role": "Aero engineer",
        "team_size_band": "2-10", "timeline": 90, "frequency": "quarterly", "pain": 3,
        "consequence": "Analyses are delayed while geometry inputs are cleaned.", "data_ready": "partial",
        "buyer": "no", "price": 1500, "reaction": "not_discussed", "objection": "timing",
        "package": "moderate", "eligibility": 3, "status": "nurture",
        "scores": [1, 0, 1, 1, 2, 1], "offer": "None",
    },
    {
        "interview_id": "INT-06", "segment": "Aero design consultancy", "role": "Project manager",
        "team_size_band": "2-10", "timeline": 35, "frequency": "monthly", "pain": 4,
        "consequence": "Client-facing handoff lacks condition and solver provenance.", "data_ready": "yes",
        "buyer": "yes", "price": 3500, "reaction": "conditional_accept", "objection": "security_privacy",
        "package": "strong", "eligibility": 5, "status": "pilot_candidate",
        "scores": [2, 2, 2, 2, 2, 1], "offer": "Standard Evidence Pilot",
    },
    {
        "interview_id": "INT-07", "segment": "UAS manufacturer", "role": "Systems engineer",
        "team_size_band": "26-50", "timeline": 50, "frequency": "monthly", "pain": 4,
        "consequence": "Aero assumptions are difficult to explain to adjacent teams.", "data_ready": "yes",
        "buyer": "unknown", "price": 3500, "reaction": "too_high", "objection": "budget",
        "package": "moderate", "eligibility": 4, "status": "follow_up",
        "scores": [2, 1, 2, 2, 2, 1], "offer": "Founding Design Partner",
    },
    {
        "interview_id": "INT-08", "segment": "Applied research laboratory", "role": "Graduate researcher",
        "team_size_band": "2-10", "timeline": 120, "frequency": "semesterly", "pain": 2,
        "consequence": "No immediate decision consequence beyond documentation quality.", "data_ready": "partial",
        "buyer": "no", "price": 1500, "reaction": "not_discussed", "objection": "no_current_project",
        "package": "weak", "eligibility": 2, "status": "disqualified",
        "scores": [0, 0, 1, 0, 1, 1], "offer": "None",
    },
    {
        "interview_id": "INT-09", "segment": "Early-stage drone venture", "role": "Founder",
        "team_size_band": "2-10", "timeline": 75, "frequency": "monthly", "pain": 3,
        "consequence": "Concept comparisons are not retained for later review.", "data_ready": "partial",
        "buyer": "yes", "price": 1500, "reaction": "no_budget", "objection": "budget",
        "package": "moderate", "eligibility": 3, "status": "nurture",
        "scores": [1, 2, 1, 1, 2, 1], "offer": "None",
    },
    {
        "interview_id": "INT-10", "segment": "Rotor technology team", "role": "Engineering director",
        "team_size_band": "11-25", "timeline": 28, "frequency": "weekly", "pain": 5,
        "consequence": "Repeated review cycles delay a near-term design selection.", "data_ready": "yes",
        "buyer": "yes", "price": 5000, "reaction": "accept", "objection": "none",
        "package": "strong", "eligibility": 5, "status": "pilot_candidate",
        "scores": [2, 2, 2, 2, 2, 2], "offer": "Extended Workflow Pilot",
    },
]


INTERVIEW_FIELDS = [
    "data_status", "interview_id", "segment", "role", "team_size_band", "decision_timeline_days",
    "workflow_frequency", "pain_severity_1_5", "consequence_of_delay", "geometry_data_ready",
    "economic_buyer_identified", "price_offer_shown_usd", "price_reaction", "primary_objection",
    "study_package_reaction", "pilot_eligibility_1_5", "follow_up_status", "synthetic_note",
]

SCORE_FIELDS = [
    "data_status", "candidate_id", "segment", "scope_safety_gate", "data_handling_gate",
    "operating_commitment_gate", "problem_repetition_score_0_2", "ownership_score_0_2",
    "data_readiness_score_0_2", "pain_urgency_score_0_2", "product_fit_score_0_2",
    "collaboration_score_0_2", "total_score", "qualification_status", "recommended_offer",
    "selection_note",
]


def qualification_status(total: int, gates_pass: bool = True) -> str:
    if not gates_pass:
        return "Disqualified"
    if total >= 10:
        return "Priority design partner"
    if total >= 8:
        return "Eligible pilot candidate"
    if total >= 6:
        return "Nurture / diagnostic"
    return "Do not pursue now"


def write_csvs() -> tuple[list[dict], list[dict]]:
    interviews: list[dict] = []
    scores: list[dict] = []
    for record in RECORDS:
        total = sum(record["scores"])
        interviews.append({
            "data_status": DATA_STATUS,
            "interview_id": record["interview_id"],
            "segment": record["segment"],
            "role": record["role"],
            "team_size_band": record["team_size_band"],
            "decision_timeline_days": record["timeline"],
            "workflow_frequency": record["frequency"],
            "pain_severity_1_5": record["pain"],
            "consequence_of_delay": record["consequence"],
            "geometry_data_ready": record["data_ready"],
            "economic_buyer_identified": record["buyer"],
            "price_offer_shown_usd": record["price"],
            "price_reaction": record["reaction"],
            "primary_objection": record["objection"],
            "study_package_reaction": record["package"],
            "pilot_eligibility_1_5": record["eligibility"],
            "follow_up_status": record["status"],
            "synthetic_note": "Hand-authored illustrative record; not a customer interview.",
        })
        scores.append({
            "data_status": DATA_STATUS,
            "candidate_id": record["interview_id"].replace("INT", "PILOT"),
            "segment": record["segment"],
            "scope_safety_gate": "PASS",
            "data_handling_gate": "PASS" if record["data_ready"] == "yes" else "HOLD",
            "operating_commitment_gate": "PASS" if record["status"] == "pilot_candidate" else "HOLD",
            "problem_repetition_score_0_2": record["scores"][0],
            "ownership_score_0_2": record["scores"][1],
            "data_readiness_score_0_2": record["scores"][2],
            "pain_urgency_score_0_2": record["scores"][3],
            "product_fit_score_0_2": record["scores"][4],
            "collaboration_score_0_2": record["scores"][5],
            "total_score": total,
            "qualification_status": qualification_status(total, record["data_ready"] == "yes"),
            "recommended_offer": record["offer"],
            "selection_note": "Synthetic demonstration only.",
        })

    with (OUTPUT_DIR / "synthetic_interviews.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=INTERVIEW_FIELDS)
        writer.writeheader()
        writer.writerows(interviews)
    with (OUTPUT_DIR / "synthetic_pilot_qualification.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SCORE_FIELDS)
        writer.writeheader()
        writer.writerows(scores)
    return interviews, scores


def write_charts(interviews: list[dict], scores: list[dict]) -> None:
    plt.style.use("dark_background")
    reaction_counts = Counter(row["price_reaction"].replace("_", " ").title() for row in interviews)
    labels, values = zip(*sorted(reaction_counts.items()))
    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    fig.patch.set_facecolor("#08111f")
    ax.set_facecolor("#08111f")
    bars = ax.bar(labels, values, color="#38bdf8")
    ax.set_title("SYNTHETIC DEMO — Illustrative price reactions, not customer evidence", fontsize=13, pad=14)
    ax.set_ylabel("Synthetic interview count")
    ax.set_ylim(0, max(values) + 1)
    ax.tick_params(axis="x", rotation=22)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.08, str(value), ha="center", color="white")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "synthetic_price_reactions.png", dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)

    ranked = sorted(scores, key=lambda row: row["total_score"], reverse=True)
    labels = [row["candidate_id"] for row in ranked]
    values = [row["total_score"] for row in ranked]
    colors = ["#22c55e" if score >= 10 else "#f59e0b" if score >= 8 else "#64748b" for score in values]
    fig, ax = plt.subplots(figsize=(10, 5.4))
    fig.patch.set_facecolor("#08111f")
    ax.set_facecolor("#08111f")
    bars = ax.bar(labels, values, color=colors)
    ax.axhline(8, color="#f59e0b", linestyle="--", linewidth=1.5, label="Eligibility threshold (8)")
    ax.axhline(10, color="#22c55e", linestyle="--", linewidth=1.5, label="Priority threshold (10)")
    ax.set_title("SYNTHETIC DEMO — Illustrative pilot qualification ranking", fontsize=13, pad=14)
    ax.set_ylabel("Score / 12")
    ax.set_ylim(0, 13)
    ax.legend(loc="lower left")
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.2, str(value), ha="center", color="white")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "synthetic_qualification_ranking.png", dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)


def write_summary(interviews: list[dict], scores: list[dict]) -> None:
    reaction_counts = Counter(row["price_reaction"] for row in interviews)
    objection_counts = Counter(row["primary_objection"] for row in interviews)
    segment_counts = Counter(row["segment"] for row in interviews)
    high_pain = sum(int(row["pain_severity_1_5"]) >= 4 for row in interviews)
    priority = [row for row in scores if row["qualification_status"] == "Priority design partner"]
    eligible = [row for row in scores if row["qualification_status"] == "Eligible pilot candidate"]
    summary = {
        "data_status": DATA_STATUS,
        "record_count": len(interviews),
        "high_pain_4_or_5_count": high_pain,
        "price_reaction_counts": dict(sorted(reaction_counts.items())),
        "objection_counts": dict(sorted(objection_counts.items())),
        "segment_counts": dict(sorted(segment_counts.items())),
        "priority_design_partner_count": len(priority),
        "eligible_candidate_count": len(eligible),
        "selected_synthetic_cohort": [row["candidate_id"] for row in priority[:5]],
        "disclosure": "All values are hand-authored synthetic examples. They are not customer, market, traction, pricing, or investment evidence.",
    }
    (OUTPUT_DIR / "synthetic_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    markdown = f"""# Synthetic Discovery Analysis Demonstration

> **SYNTHETIC DEMO — NOT CUSTOMER EVIDENCE.** All ten records are hand-authored illustrative examples approved by the user for pipeline demonstration only. They do not represent interviews, prospects, customer feedback, market demand, willingness to pay, or revenue.

## Illustrative Cohort Summary

| Metric | Synthetic result | Interpretation rule |
|---|---:|---|
| Records | {len(interviews)} | Demonstrates the ten-interview input shape only. |
| Pain score 4–5 | {high_pain}/{len(interviews)} | Synthetic distribution; do not infer pain prevalence. |
| `accept` price reactions | {reaction_counts.get('accept', 0)} | Illustrative response coding; not a conversion rate. |
| `conditional_accept` reactions | {reaction_counts.get('conditional_accept', 0)} | Demonstrates the need to record conditions and objections. |
| Priority design partners | {len(priority)} | Illustrative scorecard output, subject to mandatory gates. |
| Eligible candidates | {len(eligible)} | Illustrative next-best candidates, not confirmed pilots. |

## Illustrative Price-Reaction Coding

| Reaction | Count |
|---|---:|
""" + "\n".join(f"| `{key}` | {value} |" for key, value in sorted(reaction_counts.items())) + f"""

## Illustrative Objection Coding

| Objection | Count |
|---|---:|
""" + "\n".join(f"| `{key}` | {value} |" for key, value in sorted(objection_counts.items())) + """

## Qualification Demonstration

| Candidate | Score / 12 | Status | Experimental offer |
|---|---:|---|---|
""" + "\n".join(
        f"| {row['candidate_id']} | {row['total_score']} | {row['qualification_status']} | {row['recommended_offer']} |"
        for row in sorted(scores, key=lambda item: item["total_score"], reverse=True)
    ) + """

## Demonstration-Only Interpretation

The synthetic cohort is designed to illustrate how a structured dataset can surface a provisional priority list, price-reaction distribution, and objection taxonomy. The output must not be quoted as traction or investor evidence. When real interview notes are supplied, the analysis must be rerun in a separate directory and every metric in this document must be replaced.
"""
    (OUTPUT_DIR / "SYNTHETIC_DISCOVERY_ANALYSIS.md").write_text(markdown, encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    interviews, scores = write_csvs()
    write_charts(interviews, scores)
    write_summary(interviews, scores)
    print(f"Synthetic demo written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
