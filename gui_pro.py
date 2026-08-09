import sys
import os
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QFormLayout, QLineEdit, QComboBox, 
                             QPushButton, QCheckBox, QLabel, QGroupBox, QFileDialog,
                             QStatusBar, QTabWidget, QSlider, QSplitter)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QColor, QPalette
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from airfoil_pro import NACAGeneratorPro, AirfoilAnalysis, export_stl

# Modern Dark Theme Stylesheet
STYLESHEET = """
QMainWindow {
    background-color: #1e1e1e;
}
QWidget {
    color: #e0e0e0;
    font-family: 'Segoe UI', sans-serif;
}
QGroupBox {
    border: 2px solid #333;
    border-radius: 8px;
    margin-top: 1ex;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    padding: 0 3px;
    color: #00aaff;
}
QLineEdit, QComboBox, QSlider {
    background-color: #2d2d2d;
    border: 1px solid #444;
    border-radius: 4px;
    padding: 4px;
    color: white;
}
QPushButton {
    background-color: #0078d4;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #0086f0;
}
QPushButton:pressed {
    background-color: #005a9e;
}
QTabWidget::pane {
    border: 1px solid #333;
    background-color: #1e1e1e;
}
QTabBar::tab {
    background-color: #2d2d2d;
    padding: 8px 16px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #0078d4;
}
"""

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#1e1e1e')
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('#1e1e1e')
        self.axes.tick_params(colors='white')
        for spine in self.axes.spines.values():
            spine.set_edgecolor('#444')
        super().__init__(self.fig)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NACA Airfoil Kit Pro - Commercial Edition")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(STYLESHEET)
        
        self.init_ui()
        self.update_all()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Left Sidebar (Controls)
        sidebar = QWidget()
        sidebar.setFixedWidth(350)
        sidebar_layout = QVBoxLayout(sidebar)
        
        # Geometry Group
        geom_group = QGroupBox("Geometry Engine")
        geom_layout = QFormLayout()
        
        self.series_combo = QComboBox()
        self.series_combo.addItems(["NACA 4-Digit", "NACA 5-Digit"])
        self.series_combo.currentTextChanged.connect(self.update_all)
        geom_layout.addRow("Series:", self.series_combo)
        
        self.code_input = QLineEdit("2412")
        self.code_input.textChanged.connect(self.update_all)
        geom_layout.addRow("NACA Code:", self.code_input)
        
        self.points_slider = QSlider(Qt.Orientation.Horizontal)
        self.points_slider.setRange(20, 500)
        self.points_slider.setValue(100)
        self.points_slider.valueChanged.connect(self.update_all)
        geom_layout.addRow("Points:", self.points_slider)
        
        self.spacing_combo = QComboBox()
        self.spacing_combo.addItems(["cosine", "linear", "half-cosine"])
        self.spacing_combo.currentTextChanged.connect(self.update_all)
        geom_layout.addRow("Spacing:", self.spacing_combo)
        
        self.closed_te_check = QCheckBox("Closed Trailing Edge")
        self.closed_te_check.stateChanged.connect(self.update_all)
        geom_layout.addRow(self.closed_te_check)
        
        geom_group.setLayout(geom_layout)
        sidebar_layout.addWidget(geom_group)

        # Analysis Group
        analysis_group = QGroupBox("Aerodynamic Analysis")
        analysis_layout = QFormLayout()
        
        self.alpha_slider = QSlider(Qt.Orientation.Horizontal)
        self.alpha_slider.setRange(-10, 20)
        self.alpha_slider.setValue(0)
        self.alpha_slider.valueChanged.connect(self.update_all)
        analysis_layout.addRow("Alpha (deg):", self.alpha_slider)
        
        self.cl_label = QLabel("Cl: 0.000")
        self.cl_label.setStyleSheet("font-size: 18px; color: #00ff00; font-weight: bold;")
        analysis_layout.addRow(self.cl_label)
        
        analysis_group.setLayout(analysis_layout)
        sidebar_layout.addWidget(analysis_group)

        # Export Group
        export_group = QGroupBox("Commercial Export")
        export_layout = QVBoxLayout()
        
        btn_dat = QPushButton("Export Selig DAT")
        btn_dat.clicked.connect(lambda: self.export_action("dat"))
        export_layout.addWidget(btn_dat)
        
        btn_stl = QPushButton("Export 3D STL")
        btn_stl.clicked.connect(lambda: self.export_action("stl"))
        export_layout.addWidget(btn_stl)
        
        btn_dxf = QPushButton("Export CAD DXF")
        btn_dxf.clicked.connect(lambda: self.export_action("dxf"))
        export_layout.addWidget(btn_dxf)
        
        export_group.setLayout(export_layout)
        sidebar_layout.addWidget(export_group)
        
        sidebar_layout.addStretch()
        
        # Branding
        brand = QLabel("MANUS AI PRO ENGINE v2.0")
        brand.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand.setStyleSheet("color: #555; font-size: 10px; letter-spacing: 2px;")
        sidebar_layout.addWidget(brand)

        # Right Side (Tabs for Plots)
        self.tabs = QTabWidget()
        
        # Tab 1: Geometry Plot
        self.geom_canvas = MplCanvas(self)
        self.tabs.addTab(self.geom_canvas, "Geometry View")
        
        # Tab 2: Pressure Plot
        self.press_canvas = MplCanvas(self)
        self.tabs.addTab(self.press_canvas, "Pressure Distribution")
        
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.tabs)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def get_coords(self):
        code = self.code_input.text()
        n_pts = self.points_slider.value()
        spacing = self.spacing_combo.currentText()
        closed = self.closed_te_check.isChecked()
        
        if self.series_combo.currentText() == "NACA 4-Digit":
            return NACAGeneratorPro.naca4(code, n_pts, spacing, closed), code
        else:
            return NACAGeneratorPro.naca5(code, n_pts, spacing, closed), code

    def update_all(self):
        coords, code = self.get_coords()
        if not coords:
            self.status_bar.showMessage("Invalid NACA Code", 2000)
            return
        
        xu, yu, xl, yl = coords
        alpha = self.alpha_slider.value()
        
        # Update Geometry Plot
        ax = self.geom_canvas.axes
        ax.clear()
        ax.plot(xu, yu, color='#00aaff', linewidth=2, label='Upper')
        ax.plot(xl, yl, color='#ff5500', linewidth=2, label='Lower')
        ax.fill(np.concatenate([xu, xl[::-1]]), np.concatenate([yu, yl[::-1]]), color='#333', alpha=0.5)
        ax.set_aspect('equal')
        ax.grid(True, color='#333', linestyle='--')
        ax.set_title(f"NACA {code} Geometry", color='white')
        ax.legend()
        self.geom_canvas.draw()
        
        # Update Analysis
        cl, cp, xc = AirfoilAnalysis.compute_aerodynamics(xu, yu, xl, yl, alpha)
        self.cl_label.setText(f"Cl: {cl:.4f}")
        
        # Update Pressure Plot
        axp = self.press_canvas.axes
        axp.clear()
        axp.plot(xc, cp, color='#00ff00', linewidth=2)
        axp.invert_yaxis()  # Cp is usually plotted inverted
        axp.grid(True, color='#333', linestyle='--')
        axp.set_title(f"Pressure Distribution (Alpha={alpha}°)", color='white')
        axp.set_xlabel("x/c", color='white')
        axp.set_ylabel("Cp", color='white')
        self.press_canvas.draw()

    def export_action(self, fmt):
        coords, code = self.get_coords()
        if not coords: return
        
        xu, yu, xl, yl = coords
        path, _ = QFileDialog.getSaveFileName(self, "Save File", f"NACA_{code}.{fmt}")
        if not path: return
        
        try:
            if fmt == 'stl':
                export_stl(xu, yu, xl, yl, path)
            elif fmt == 'dat':
                with open(path, 'w') as f:
                    f.write(f"NACA {code}\n")
                    for i in range(len(xu)-1, -1, -1): f.write(f"{xu[i]:.6f} {yu[i]:.6f}\n")
                    for i in range(1, len(xl)): f.write(f"{xl[i]:.6f} {yl[i]:.6f}\n")
            elif fmt == 'dxf':
                with open(path, 'w') as f:
                    f.write("0\nSECTION\n2\nENTITIES\n")
                    for i in range(len(xu)-1):
                        f.write(f"0\nLINE\n8\n0\n10\n{xu[i]}\n20\n{yu[i]}\n11\n{xu[i+1]}\n21\n{yu[i+1]}\n")
                    for i in range(len(xl)-1):
                        f.write(f"0\nLINE\n8\n0\n10\n{xl[i]}\n20\n{yl[i]}\n11\n{xl[i+1]}\n21\n{yl[i+1]}\n")
                    f.write("0\nENDSEC\n0\nEOF\n")
            self.status_bar.showMessage(f"Successfully exported to {path}", 5000)
        except Exception as e:
            self.status_bar.showMessage(f"Export Error: {str(e)}", 5000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
