# NACA Airfoil Kit Pro (Ultimate Enterprise Edition)

The most comprehensive, commercial-grade toolkit for airfoil design, analysis, and optimization. This edition features advanced aerodynamic modeling, flow visualization, and a massive integrated airfoil database.

## 🚀 Key Features

### 🌊 Flow Visualization (New)
- **Interactive Streamlines**: Real-time visualization of the velocity field and flow lines around the airfoil.
- **Pressure Mapping**: High-fidelity pressure coefficient ($C_p$) distribution plots.

### 📂 Integrated UIUC Database
- **1,600+ Profiles**: Instant access to the world's largest coordinate database (Clark Y, Eppler, etc.).
- **Smart Search**: Filter and load any profile with live aerodynamic previews.

### 📊 Advanced Aerodynamic Analysis
- **Schlichting Drag Model**: Accurate profile drag prediction considering surface roughness.
- **Stall Prediction**: Empirical modeling of flow separation and post-stall behavior.
- **L/D Optimization**: Automatically find the optimal geometry for maximum aerodynamic efficiency.

### 🛠 Professional Export Suite
- **CAD/CAM Support**: High-precision DXF and 3D-printable STL exports.
- **Technical Reporting**: One-click professional PDF reports with embedded plots and data.

---

## 📖 User Guide

### 1. Generating NACA Airfoils
- Select **NACA Generator** mode.
- Enter the 4 or 5-digit code (e.g., `2412`).
- Adjust the **Points** slider for resolution.

### 2. Aerodynamic Analysis
- Use the **Alpha** slider to change the angle of attack.
- Input the **Reynolds Number** for your flight regime.
- Set **Roughness (k/c)** to simulate real-world surface conditions (e.g., `0.001` for standard paint).

### 3. Comparison & Optimization
- Click **Add to Comparison** to keep a reference profile on the plot.
- Use **Maximize L/D** to let the engine find the most efficient shape for your current Alpha/Re.

---

## 👨‍💻 Developer Guide

### Project Structure
- `gui.py`: Main PyQt6 interface and visualization logic.
- `airfoil_pro.py`: The computational core (NACA math, Panel Method, Aero models).
- `report_gen.py`: PDF generation engine using `fpdf2`.
- `uiuc_database.json`: Local index for the airfoil database.

### Installation
```bash
git clone https://github.com/Ali-Marandi/naca-airfoil-kit.git
pip install PyQt6 matplotlib numpy requests fpdf2
python gui.py
```

### Building the EXE
```bash
pyinstaller --onefile --windowed --name "NACA-Airfoil-Kit-Pro" --add-data "uiuc_database.json;." gui.py
```

---
*Developed by Manus AI - Engineering Excellence*
