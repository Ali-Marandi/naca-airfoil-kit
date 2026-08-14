"""Product-facing guidance and evidence-readiness checks.

This module deliberately separates UI wording and lightweight quality gates from the
engineering solvers. It makes the product easier to localize and prevents a
preliminary study from being mislabeled as experimentally validated.
"""

from __future__ import annotations

from typing import Any, Mapping


PRELIMINARY_SCOPE_NOTICE = (
    "Preliminary engineering screening only. Validate with experimental data or a "
    "higher-fidelity viscous solver before a safety-critical, certification, or "
    "manufacturing-release decision."
)

STARTER_WORKFLOWS = (
    {
        "id": "screen_compare",
        "title": "1. Screen a small candidate set",
        "workspace": "Design Study",
        "description": (
            "Compare 3–5 NACA candidates over the same alpha, Reynolds, and surface "
            "condition range. Keep the candidate list and operating conditions with the export."
        ),
    },
    {
        "id": "robust_shortlist",
        "title": "2. Stress-test the shortlist",
        "workspace": "Pareto Explorer / Robustness",
        "description": (
            "Use multi-Re Pareto and the deterministic condition envelope to inspect "
            "trade-offs. A robust rank is still a preliminary model result."
        ),
    },
    {
        "id": "evidence_package",
        "title": "3. Export an evidence-ready study package",
        "workspace": "Validation / QA & Export",
        "description": (
            "Attach experimental metadata where available, review residuals separately "
            "for Cl and Cd, then export the audit manifest alongside the raw results."
        ),
    },
)

VALIDATION_METADATA_FIELDS = (
    ("geometry_reference", "Geometry name/version, chord, and flap state"),
    ("mach_number", "Mach number or an explicit incompressible-flow statement"),
    ("transition_surface", "Transition, roughness, and turbulence description"),
    ("facility_corrections", "Tunnel/facility and blockage or wall-correction note"),
    ("alpha_convention", "Angle convention, tare, and force-reduction note"),
    ("source_identifier", "Dataset source, page/identifier, and permitted-use note"),
)


def normalized_validation_metadata(metadata: Mapping[str, Any] | None) -> dict[str, str]:
    """Return only known validation metadata fields as normalized text strings."""
    raw = metadata or {}
    return {
        field: str(raw.get(field, "")).strip()
        for field, _label in VALIDATION_METADATA_FIELDS
    }


def evidence_readiness(
    metadata: Mapping[str, Any] | None,
    *,
    experimental_rows_loaded: bool,
) -> dict[str, Any]:
    """Classify study evidence without claiming engineering validation.

    ``evidence_ready`` means that the expected metadata and a CSV have been
    supplied for review. It never means a model has passed a universal accuracy
    threshold, nor does it override the preliminary engineering scope.
    """
    normalized = normalized_validation_metadata(metadata)
    missing = [label for field, label in VALIDATION_METADATA_FIELDS if not normalized[field]]

    if not experimental_rows_loaded:
        status = "screening_only"
        headline = "Screening-only study"
        guidance = (
            "No experimental polar is attached. Export is suitable for preliminary "
            "screening and must retain the stated model-scope notice."
        )
    elif missing:
        status = "informational_validation"
        headline = "Informational comparison only"
        guidance = (
            "Residuals can be inspected, but one or more required validation metadata "
            "items are missing. Do not describe this comparison as validated."
        )
    else:
        status = "metadata_complete_validation_review"
        headline = "Metadata-complete validation review"
        guidance = (
            "The comparison has a CSV and the required metadata. Review Cl and Cd "
            "metrics within the documented alpha/condition range; this is not a universal validation claim."
        )

    return {
        "status": status,
        "headline": headline,
        "guidance": guidance,
        "missing_metadata": missing,
        "experimental_rows_loaded": bool(experimental_rows_loaded),
        "scope_notice": PRELIMINARY_SCOPE_NOTICE,
        "validation_metadata": normalized,
    }


def desktop_study_checklist() -> str:
    """Return concise guidance suitable for a desktop QMessageBox."""
    return (
        "Evidence-ready preliminary study checklist\n\n"
        "1. Lock geometry: record the exact airfoil, point treatment, and flap state.\n"
        "2. Match conditions: record Reynolds, Mach, surface/transition, and alpha convention.\n"
        "3. If experimental data are used, retain the dataset source and facility corrections.\n"
        "4. Export the audit manifest with CSV/PDF outputs for review.\n\n"
        f"Scope: {PRELIMINARY_SCOPE_NOTICE}"
    )
