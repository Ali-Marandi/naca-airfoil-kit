# NACA Airfoil Kit Pro

A professional-grade toolkit for generating, visualizing, and exporting NACA airfoil coordinates. Developed to meet commercial standards with a modern graphical user interface and advanced geometric computations.

## Features

- **Multi-Series Support**:
  - **NACA 4-Digit**: Standard series with camber and thickness control.
  - **NACA 5-Digit**: Advanced series for specific lift and moment characteristics.
- **Advanced Geometry Engine**:
  - **Cosine Spacing**: Improved resolution at leading and trailing edges for better CFD results.
  - **Trailing Edge Control**: Options for open or closed trailing edges.
  - **High Precision**: Double-precision floating-point calculations.
- **Modern GUI**:
  - Built with **PyQt6** for a native look and feel.
  - Real-time interactive plotting using **Matplotlib**.
  - Intuitive parameter controls.
- **Export Capabilities**:
  - **Selig DAT**: Standard format compatible with XFOIL and other analysis tools.
  - **CSV**: For spreadsheet analysis and custom scripts.
  - **DXF**: Ready for import into CAD software like AutoCAD, SolidWorks, or Fusion 360.

## Installation

### For Users (Windows)
Download the latest `NACA-Airfoil-Kit-Pro.exe` from the [Releases](https://github.com/user/naca-airfoil-kit/releases) page. No installation required.

### For Developers
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/naca-airfoil-kit.git
   ```
2. Install dependencies:
   ```bash
   pip install PyQt6 matplotlib numpy scipy
   ```
3. Run the application:
   ```bash
   python gui.py
   ```

## Usage
1. Select the NACA series (4-digit or 5-digit).
2. Enter the NACA code (e.g., `2412` or `24012`).
3. Adjust the number of points and spacing type.
4. Click Export to save the coordinates in your preferred format.

## License
This project is licensed under the MIT License.

---
*Developed by Manus AI*
