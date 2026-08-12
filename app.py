"""Streamlit web interface for NACA Airfoil Kit Pro.

Results in the web interface are preliminary engineering-screening results.
Validate with experimental data or a higher-fidelity viscous solver before any
safety-critical, certification, or manufacturing release decision.
"""

import csv
import io
import json
from datetime import datetime, timezone

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from airfoil_pro import AirfoilAnalysis, EngineeringStudy, GeometryOptimizer, NACAGeneratorPro, UIUCLoader


st.set_page_config(page_title="NACA Airfoil Kit Pro — Web Edition", layout="wide")


@st.cache_data(show_spinner=False)
def load_db():
    with open("uiuc_database.json", "r", encoding="utf-8") as handle:
        return json.load(handle)


def csv_download(rows, filename, extra_columns=None):
    """Build a UTF-8 CSV download from a list of dictionaries."""
    if not rows:
        return None, filename
    fieldnames = list(rows[0].keys())
    if extra_columns:
        fieldnames = list(extra_columns) + fieldnames
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return output.getvalue().encode("utf-8-sig"), filename


def coordinate_rows(xu, yu, xl, yl):
    rows = []
    for index, (x, y) in enumerate(zip(xu, yu), start=1):
        rows.append({"surface": "upper", "point": index, "x_over_c": float(x), "y_over_c": float(y)})
    for index, (x, y) in enumerate(zip(xl, yl), start=1):
        rows.append({"surface": "lower", "point": index, "x_over_c": float(x), "y_over_c": float(y)})
    return rows


def render_geometry(xu, yu, xl, yl, name):
    fig, axis = plt.subplots(figsize=(10, 4))
    axis.plot(xu, yu, color="#0ea5e9", linewidth=2.2, label="Upper surface")
    axis.plot(xl, yl, color="#f97316", linewidth=2.2, label="Lower surface")
    axis.fill(np.concatenate([xu, xl[::-1]]), np.concatenate([yu, yl[::-1]]), color="#94a3b8", alpha=0.25)
    axis.set_aspect("equal", adjustable="box")
    axis.set_xlabel("x/c")
    axis.set_ylabel("y/c")
    axis.set_title(f"{name} — normalized geometry")
    axis.grid(True, linestyle="--", alpha=0.35)
    axis.legend(loc="upper right")
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)


def render_pressure(xc, cp):
    fig, axis = plt.subplots(figsize=(10, 4))
    axis.plot(xc, cp, color="#22c55e", linewidth=2.0)
    axis.invert_yaxis()
    axis.set_xlabel("x/c")
    axis.set_ylabel("Cp")
    axis.set_title("Pressure coefficient distribution")
    axis.grid(True, alpha=0.35)
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)


def render_flow(xu, yu, xl, yl, alpha, gamma, panel_x, panel_y, panel_lengths):
    fig, axis = plt.subplots(figsize=(10, 4))
    x_mesh, y_mesh, u, v = AirfoilAnalysis.get_streamlines(xu, yu, xl, yl, alpha, gamma, panel_x, panel_y, panel_lengths)
    axis.streamplot(x_mesh, y_mesh, u, v, color="#38bdf8", density=1.15, linewidth=0.8)
    axis.fill(np.concatenate([xu, xl[::-1]]), np.concatenate([yu, yl[::-1]]), color="#0f172a", zorder=10)
    axis.set_aspect("equal", adjustable="box")
    axis.set_xlim(-0.5, 1.5)
    axis.set_ylim(-0.5, 0.5)
    axis.set_xlabel("x/c")
    axis.set_ylabel("y/c")
    axis.set_title("Potential-flow streamline visualization")
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)


def render_polar(polar_rows, name):
    alpha = np.asarray([row["alpha_deg"] for row in polar_rows])
    cl = np.asarray([row["cl"] for row in polar_rows])
    cd = np.asarray([row["cd"] for row in polar_rows])
    ld = np.asarray([row["ld"] for row in polar_rows])
    stalled = np.asarray([row["stalled_estimate"] for row in polar_rows], dtype=bool)
    best_index = int(np.nanargmax(ld)) if np.any(np.isfinite(ld)) else 0

    figure, axes = plt.subplots(1, 3, figsize=(15, 4))
    axes[0].plot(alpha, cl, color="#0ea5e9", linewidth=2.0)
    axes[0].set(title="Lift curve", xlabel="α [deg]", ylabel="Cl")
    axes[1].plot(cl, cd, color="#f97316", linewidth=2.0)
    axes[1].set(title="Drag polar", xlabel="Cl", ylabel="Cd")
    axes[2].plot(alpha, ld, color="#22c55e", linewidth=2.0)
    axes[2].scatter(alpha[best_index], ld[best_index], color="#eab308", s=56, zorder=5, label="Best L/D")
    axes[2].set(title="Efficiency envelope", xlabel="α [deg]", ylabel="L/D")
    if np.any(stalled):
        for axis in (axes[0], axes[2]):
            axis.scatter(alpha[stalled], (cl if axis is axes[0] else ld)[stalled], color="#ef4444", s=30, zorder=5, label="Stall estimate")
    for axis in axes:
        axis.grid(True, alpha=0.3)
        axis.legend(loc="best") if axis.get_legend_handles_labels()[0] else None
    figure.suptitle(f"{name} — preliminary polar study", fontsize=14)
    figure.tight_layout()
    st.pyplot(figure, clear_figure=True)


st.title("NACA Airfoil Kit Pro — Enterprise Web")
st.caption("Preliminary panel/empirical screening only. Validate with experimental data or a high-fidelity viscous solver before production decisions.")
st.markdown("---")

database = load_db()
st.sidebar.header("Airfoil controls")
mode = st.sidebar.radio("Operation mode", ["NACA Generator", "UIUC Database"])

coords = None
name = ""
if mode == "NACA Generator":
    series = st.sidebar.selectbox("Series", ["NACA 4-Digit", "NACA 5-Digit"])
    code = st.sidebar.text_input("NACA code", "2412").strip()
    points = st.sidebar.slider("Points per surface", 20, 300, 100)
    coords = NACAGeneratorPro.naca4(code, points) if series == "NACA 4-Digit" else NACAGeneratorPro.naca5(code, points)
    name = f"NACA {code}"
else:
    search = st.sidebar.text_input("Search UIUC airfoil", "")
    filtered = [item for item in database if search.lower() in item["name"].lower()]
    if not filtered:
        st.warning("No UIUC airfoil matches the current search.")
        st.stop()
    selected_name = st.sidebar.selectbox("Select airfoil", [item["name"] for item in filtered])
    url = next(item["url"] for item in database if item["name"] == selected_name)
    with st.spinner("Loading UIUC geometry..."):
        coords = UIUCLoader.load_from_url(url)
    name = selected_name

st.sidebar.subheader("Operating condition")
alpha = st.sidebar.slider("Alpha [deg]", -10.0, 20.0, 0.0, 0.5)
reynolds = st.sidebar.number_input("Reynolds number", 1e5, 1e8, 1e6, format="%.0e")
roughness = st.sidebar.number_input("Surface roughness k/c", 0.0, 0.05, 0.0, format="%.5f")

if not coords:
    st.error("Invalid airfoil data. Try another NACA code or UIUC profile.")
    st.stop()

xu, yu, xl, yl = coords
cl, cd, cp, xc, gamma, panel_x, panel_y, panel_lengths = AirfoilAnalysis.compute_aerodynamics(xu, yu, xl, yl, alpha, reynolds, roughness)
metrics = AirfoilAnalysis.geometry_metrics(xu, yu, xl, yl)

metric_a, metric_b, metric_c, metric_d = st.columns(4)
metric_a.metric("Lift coefficient — Cl", f"{cl:.4f}")
metric_b.metric("Drag coefficient — Cd", f"{cd:.5f}")
metric_c.metric("L/D ratio", f"{cl / cd:.2f}" if cd > 0 else "N/A")
metric_d.metric("Maximum thickness", f"{metrics['max_thickness_pct']:.2f}%")

analysis_tab, pressure_tab, flow_tab, polar_tab, study_tab, qa_tab = st.tabs(
    ["Geometry", "Pressure", "Flow Field", "Polar & Envelope", "Design Study", "QA & Export"]
)

with analysis_tab:
    render_geometry(xu, yu, xl, yl, name)
    if mode == "NACA Generator":
        st.subheader("Single-condition optimization")
        if st.button("Maximize L/D at current condition"):
            optimized_code, best_ld = GeometryOptimizer.optimize_ld(code, alpha, reynolds, "4-digit" if series == "NACA 4-Digit" else "5-digit")
            st.success(f"Screening optimum: NACA {optimized_code} | estimated L/D {best_ld:.2f}")

with pressure_tab:
    render_pressure(xc, cp)

with flow_tab:
    render_flow(xu, yu, xl, yl, alpha, gamma, panel_x, panel_y, panel_lengths)

with polar_tab:
    st.subheader("Operating envelope")
    polar_controls = st.columns(3)
    polar_start = polar_controls[0].number_input("Alpha start [deg]", -20.0, 10.0, -6.0, 0.5, key="polar_start")
    polar_end = polar_controls[1].number_input("Alpha end [deg]", -5.0, 30.0, 14.0, 0.5, key="polar_end")
    polar_step = polar_controls[2].selectbox("Alpha increment [deg]", [0.5, 1.0, 2.0], index=1, key="polar_step")
    if polar_end <= polar_start:
        st.warning("Alpha end must be greater than alpha start.")
    else:
        alpha_values = np.arange(polar_start, polar_end + 0.5 * polar_step, polar_step)
        with st.spinner("Computing preliminary polar..."):
            polar = AirfoilAnalysis.compute_polar(xu, yu, xl, yl, alpha_values, reynolds, roughness)
        polar_rows = polar["rows"]
        polar_summary = AirfoilAnalysis.summarize_polar(polar_rows)
        envelope_a, envelope_b, envelope_c = st.columns(3)
        envelope_a.metric("Best L/D", f"{polar_summary['best_ld']:.2f}")
        envelope_b.metric("Best-alpha", f"{polar_summary['best_alpha_deg']:.1f}°")
        envelope_c.metric("Maximum Cl", f"{polar_summary['cl_max']:.3f}")
        render_polar(polar_rows, name)

        polar_export_rows = [
            {
                "airfoil": name,
                "reynolds": f"{reynolds:.0f}",
                "roughness_k_over_c": f"{roughness:.6f}",
                **row,
            }
            for row in polar_rows
        ]
        polar_file, polar_filename = csv_download(polar_export_rows, f"{name.replace(' ', '_')}_polar.csv")
        st.download_button("Download polar CSV", polar_file, polar_filename, "text/csv", use_container_width=True)

with study_tab:
    st.subheader("Multi-airfoil screening study")
    st.write("Compare a set of NACA 4-digit candidates over the same alpha envelope. Results are ranked by estimated best L/D.")
    default_codes = "0012, 2412, 4412, 6409"
    candidates = st.text_area("NACA 4-digit candidates (comma-separated)", default_codes, key="candidate_codes")
    study_columns = st.columns(3)
    study_start = study_columns[0].number_input("Study alpha start", -15.0, 5.0, -4.0, 0.5, key="study_start")
    study_end = study_columns[1].number_input("Study alpha end", 0.0, 20.0, 12.0, 0.5, key="study_end")
    study_step = study_columns[2].selectbox("Study alpha increment", [1.0, 2.0], key="study_step")
    if st.button("Run multi-airfoil screening", use_container_width=True):
        candidate_codes = EngineeringStudy.parse_naca4_codes(candidates)
        if not candidate_codes:
            st.error("Enter at least one valid four-digit NACA code.")
        elif study_end <= study_start:
            st.error("Study alpha end must be greater than the alpha start.")
        else:
            with st.spinner("Screening candidate airfoils..."):
                study_alphas = np.arange(study_start, study_end + 0.5 * study_step, study_step)
                st.session_state["design_study"] = EngineeringStudy.screen_naca4(candidate_codes, study_alphas, reynolds, roughness, 100)
                st.session_state["design_study_metadata"] = {"reynolds": reynolds, "roughness": roughness, "alpha_start": study_start, "alpha_end": study_end, "alpha_step": study_step}

    result = st.session_state.get("design_study")
    if result and result["rankings"]:
        st.dataframe(result["rankings"], use_container_width=True, hide_index=True)
        ranking_file, ranking_filename = csv_download(result["rankings"], "naca_design_study_ranking.csv")
        st.download_button("Download ranking CSV", ranking_file, ranking_filename, "text/csv", use_container_width=True)

        figure, axis = plt.subplots(figsize=(10, 4))
        for airfoil_name, rows in result["polars"].items():
            axis.plot([row["alpha_deg"] for row in rows], [row["ld"] for row in rows], linewidth=1.8, label=airfoil_name)
        axis.set(title="Candidate efficiency comparison", xlabel="α [deg]", ylabel="L/D")
        axis.grid(True, alpha=0.3)
        axis.legend(ncol=2)
        figure.tight_layout()
        st.pyplot(figure, clear_figure=True)

with qa_tab:
    st.subheader("Geometry quality assurance")
    qa_a, qa_b, qa_c = st.columns(3)
    qa_a.metric("Max thickness location", f"{metrics['max_thickness_xc']:.3f} c")
    qa_b.metric("Max camber", f"{metrics['max_camber_pct']:.2f}% @ {metrics['max_camber_xc']:.3f} c")
    qa_c.metric("Trailing-edge gap", f"{metrics['trailing_edge_gap_pct']:.3f}% c")
    st.caption(f"Normalized section area ratio: {metrics['section_area_ratio']:.5f}. Use QA values for preliminary geometry checks, not tooling tolerances.")

    qa_rows = [{"airfoil": name, **metrics, "analysis_timestamp_utc": datetime.now(timezone.utc).isoformat()}]
    qa_file, qa_filename = csv_download(qa_rows, f"{name.replace(' ', '_')}_geometry_qa.csv")
    st.download_button("Download geometry QA CSV", qa_file, qa_filename, "text/csv", use_container_width=True)

    coordinates_file, coordinates_filename = csv_download(coordinate_rows(xu, yu, xl, yl), f"{name.replace(' ', '_')}_coordinates.csv")
    st.download_button("Download normalized coordinate CSV", coordinates_file, coordinates_filename, "text/csv", use_container_width=True)

st.markdown("---")
st.caption("NACA Airfoil Kit Pro — preliminary aerodynamic screening; validate externally before safety-critical use.")
