# NACA Airfoil Kit Pro (Commercial Edition)

A high-performance, commercial-grade toolkit for generating, analyzing, and exporting NACA airfoil coordinates. This professional edition features an advanced aerodynamic analysis engine and a modern, high-fidelity user interface.

## 🚀 Key Features

### 🔹 Advanced Geometry Engine
- **NACA 4-Digit & 5-Digit Support**: High-precision coordinate generation.
- **Enhanced Spacing Options**: Linear, Cosine, and Half-Cosine spacing for optimized CFD meshing.
- **Trailing Edge Control**: Option for open or closed trailing edges.
- **High Resolution**: Support for up to 500 coordinate points.

### 📊 Aerodynamic Analysis (Pro)
- **Vortex Panel Method**: Real-time estimation of the Lift Coefficient ($C_l$).
- **Pressure Distribution**: Interactive plotting of the Pressure Coefficient ($C_p$) along the chord.
- **Variable Alpha**: Analyze performance across a range of angles of attack (-10° to 20°).

### 🛠 Commercial Export Suite
- **Selig DAT**: Standard format for XFOIL and other research tools.
- **CAD DXF**: Ready-to-import geometry for SolidWorks, Fusion 360, and AutoCAD.
- **3D STL**: Direct export for 3D printing and rapid prototyping.

### 🎨 Modern UI/UX
- **Dark Mode Interface**: Optimized for long engineering sessions.
- **Interactive Plots**: Real-time updates as parameters change.
- **Professional Styling**: Clean, responsive layout built with PyQt6.

## 📥 Installation

### For Windows Users
Download the latest `NACA-Airfoil-Kit-Pro.exe` from the [Releases](https://github.com/Ali-Marandi/naca-airfoil-kit/releases) page. It is a standalone executable—no installation or Python environment required.

### For Developers
1. Clone the repository:
   ```bash
   git clone https://github.com/Ali-Marandi/naca-airfoil-kit.git
   ```
2. Install dependencies:
   ```bash
   pip install PyQt6 matplotlib numpy
   ```
3. Run the application:
   ```bash
   python gui.py
   ```

## 🛠 Building from Source
To build the standalone executable yourself, use PyInstaller:
```bash
pyinstaller --onefile --windowed --name "NACA-Airfoil-Kit-Pro" gui.py
```

## 📄 License
This project is licensed under the MIT License.

---
*Developed by Manus AI for Commercial Grade Engineering Applications*
