import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from airfoil_pro import NACAGeneratorPro, AirfoilAnalysis, GeometryOptimizer, UIUCLoader
import json
import os

st.set_page_config(page_title="NACA Airfoil Kit Pro - Web Edition", layout="wide")

st.title("🛩 NACA Airfoil Kit Pro - Enterprise Web")
st.markdown("---")

# Load UIUC DB
@st.cache_data
def load_db():
    with open("uiuc_database.json", "r") as f:
        return json.load(f)

db = load_db()

# Sidebar
st.sidebar.header("Controls")
mode = st.sidebar.radio("Operation Mode", ["NACA Generator", "UIUC Database"])

if mode == "NACA Generator":
    series = st.sidebar.selectbox("Series", ["NACA 4-Digit", "NACA 5-Digit"])
    code = st.sidebar.text_input("NACA Code", "2412")
    pts = st.sidebar.slider("Points", 20, 500, 100)
    coords = NACAGeneratorPro.naca4(code, pts) if series == "NACA 4-Digit" else NACAGeneratorPro.naca5(code, pts)
    name = f"NACA {code}"
else:
    search = st.sidebar.text_input("Search Airfoil", "")
    filtered = [i for i in db if search.lower() in i['name'].lower()]
    selected = st.sidebar.selectbox("Select Airfoil", [i['name'] for i in filtered])
    url = next(i['url'] for i in db if i['name'] == selected)
    coords = UIUCLoader.load_from_url(url)
    name = selected

# Analysis Params
st.sidebar.subheader("Analysis Parameters")
alpha = st.sidebar.slider("Alpha (deg)", -10, 20, 0)
re = st.sidebar.number_input("Reynolds Number", 1e5, 1e8, 1e6, format="%.0e")
rough = st.sidebar.number_input("Roughness (k/c)", 0.0, 0.1, 0.0, format="%.5f")

if coords:
    xu, yu, xl, yl = coords
    res = AirfoilAnalysis.compute_aerodynamics(xu, yu, xl, yl, alpha, re, rough)
    cl, cd, cp, xc, gamma, pxc, pyc, pl = res
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Lift Coefficient (Cl)", f"{cl:.4f}")
    col2.metric("Drag Coefficient (Cd)", f"{cd:.4f}")
    col3.metric("L/D Ratio", f"{cl/cd:.2f}" if cd > 0 else "N/A")
    
    tab1, tab2, tab3 = st.tabs(["Geometry", "Pressure Distribution", "Flow Field"])
    
    with tab1:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(xu, yu, 'b', label='Upper')
        ax.plot(xl, yl, 'r', label='Lower')
        ax.fill(np.concatenate([xu, xl[::-1]]), np.concatenate([yu, yl[::-1]]), 'gray', alpha=0.3)
        ax.set_aspect('equal')
        ax.grid(True, linestyle='--')
        ax.set_title(f"{name} Geometry")
        st.pyplot(fig)
        
    with tab2:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(xc, cp, 'g')
        ax.invert_yaxis()
        ax.set_xlabel("x/c")
        ax.set_ylabel("Cp")
        ax.grid(True)
        ax.set_title("Pressure Coefficient Distribution")
        st.pyplot(fig)
        
    with tab3:
        fig, ax = plt.subplots(figsize=(10, 4))
        X, Y, u, v = AirfoilAnalysis.get_streamlines(xu, yu, xl, yl, alpha, gamma, pxc, pyc, pl)
        ax.streamplot(X, Y, u, v, color='blue', density=1.2)
        ax.fill(np.concatenate([xu, xl[::-1]]), np.concatenate([yu, yl[::-1]]), 'black', zorder=10)
        ax.set_aspect('equal')
        ax.set_xlim(-0.5, 1.5)
        ax.set_ylim(-0.5, 0.5)
        ax.set_title("Flow Field Visualization")
        st.pyplot(fig)

    # Optimization
    st.sidebar.subheader("Optimization")
    if mode == "NACA Generator":
        if st.sidebar.button("Maximize L/D"):
            new_code, best_ld = GeometryOptimizer.optimize_ld(code, alpha, re, "4-digit" if series == "NACA 4-Digit" else "5-digit")
            st.sidebar.success(f"Optimized to {new_code} (L/D: {best_ld:.2f})")
else:
    st.error("Invalid Airfoil Data")

st.markdown("---")
st.caption("Developed by Manus AI for Aerospace Engineers")
