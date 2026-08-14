"""PDF reporting for preliminary NACA Airfoil Kit studies."""

from __future__ import annotations

import datetime

from fpdf import FPDF

from product_guidance import PRELIMINARY_SCOPE_NOTICE


class AirfoilReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "NACA Airfoil Kit Pro - Preliminary Study Report", 0, 1, "C")
        self.set_draw_color(220, 220, 220)
        self.line(10, 19, 200, 19)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()} | Preliminary engineering screening", 0, 0, "C")


def _write_section_title(pdf: AirfoilReport, title: str):
    pdf.set_x(pdf.l_margin)
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(31, 78, 121)
    pdf.cell(0, 8, title, 0, 1, "L")
    pdf.set_x(pdf.l_margin)
    pdf.set_text_color(0, 0, 0)


def _write_multiline(pdf: AirfoilReport, line_height: float, text: str, **kwargs):
    """Render at the left margin regardless of fpdf2 cursor semantics."""
    pdf.set_x(pdf.l_margin)
    printable_width = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.multi_cell(printable_width, line_height, text, **kwargs)
    pdf.set_x(pdf.l_margin)


def _write_scope_and_evidence(pdf: AirfoilReport, readiness: dict | None):
    """Make the report's preliminary scope and available evidence explicit."""
    _write_section_title(pdf, "Scope and Evidence")
    pdf.set_font("Arial", "", 10)
    pdf.set_fill_color(255, 247, 237)
    _write_multiline(pdf, 6, PRELIMINARY_SCOPE_NOTICE, border=1, fill=True)
    pdf.ln(2)

    if readiness:
        headline = str(readiness.get("headline", "Screening-only study"))
        guidance = str(readiness.get("guidance", "No evidence status was supplied."))
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 6, f"Evidence status: {headline}", 0, 1, "L")
        pdf.set_font("Arial", "", 10)
        _write_multiline(pdf, 6, guidance)
        missing = readiness.get("missing_metadata") or []
        if missing:
            pdf.set_font("Arial", "I", 9)
            _write_multiline(pdf, 5, "Metadata still required for review: " + "; ".join(map(str, missing)))
    else:
        pdf.set_font("Arial", "", 10)
        _write_multiline(pdf, 6, "Evidence status: screening-only study; no validation metadata was attached to this report.")
    pdf.ln(3)


def generate_pdf_report(filename, data):
    """Generate a report that preserves the preliminary engineering scope.

    ``data`` must contain ``name``, ``params``, ``cl`` and ``cd``. Optional
    ``evidence_readiness`` is produced by ``product_guidance.evidence_readiness``.
    It intentionally does not convert metadata completeness into a validation or
    certification conclusion.
    """
    pdf = AirfoilReport()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.set_font("Arial", "", 11)

    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, f"Created UTC: {datetime.datetime.now(datetime.timezone.utc).isoformat()}", 0, 1, "L", fill=True)
    pdf.cell(0, 8, f"Airfoil: {data['name']}", 0, 1, "L")
    pdf.ln(3)

    _write_scope_and_evidence(pdf, data.get("evidence_readiness"))

    _write_section_title(pdf, "Input Parameters")
    pdf.set_font("Arial", "", 10)
    for key, value in data["params"].items():
        pdf.cell(0, 6, f"- {key}: {value}", 0, 1, "L")
    pdf.ln(3)

    _write_section_title(pdf, "Preliminary Aerodynamic Results")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, f"Lift Coefficient (Cl): {data['cl']:.4f}", 0, 1, "L")
    pdf.cell(0, 6, f"Drag Coefficient (Cd): {data['cd']:.4f}", 0, 1, "L")
    pdf.cell(0, 6, f"L/D Ratio: {data['cl'] / data['cd']:.2f}" if data["cd"] != 0 else "L/D: N/A", 0, 1, "L")
    pdf.ln(3)

    if data.get("audit_manifest_note"):
        _write_section_title(pdf, "Traceability")
        pdf.set_font("Arial", "", 10)
        _write_multiline(pdf, 6, str(data["audit_manifest_note"]))
        pdf.ln(3)

    plot_path = data.get("plot_path")
    if plot_path:
        _write_section_title(pdf, "Geometry Visualization")
        pdf.image(plot_path, x=10, w=190)

    pdf.output(filename)
