import sys
import os
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QFormLayout, QLineEdit, QComboBox, 
                             QPushButton, QCheckBox, QLabel, QGroupBox, QFileDialog,
                             QStatusBar, QFrame)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from airfoil import NACAGenerator

class AirfoilPlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#f0f0f0')
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        self.axes.set_aspect('equal')
        self.axes.grid(True, linestyle='--', alpha=0.6)
        self.axes.set_xlabel('x/c')
        self.axes.set_ylabel('y/c')
        self.axes.set_title('Airfoil Geometry')

    def plot_airfoil(self, xu, yu, xl, yl, name):
        self.axes.clear()
        self.axes.plot(xu, yu, 'b-', label='Upper Surface', linewidth=2)
        self.axes.plot(xl, yl, 'r-', label='Lower Surface', linewidth=2)
        self.axes.fill_between(np.concatenate([xu, xl[::-1]]), 
                               np.concatenate([yu, yl[::-1]]), 
                               color='gray', alpha=0.3)
        self.axes.set_aspect('equal')
        self.axes.grid(True, linestyle='--', alpha=0.6)
        self.axes.set_xlabel('x/c')
        self.axes.set_ylabel('y/c')
        self.axes.set_title(f'NACA {name} Airfoil')
        self.axes.legend()
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NACA Airfoil Kit Pro")
        self.setMinimumSize(1000, 600)
        self.init_ui()
        self.update_plot()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(300)
        sidebar_layout = QVBoxLayout(sidebar)
        
        # Parameters Group
        param_group = QGroupBox("Airfoil Parameters")
        param_layout = QFormLayout()
        
        self.series_combo = QComboBox()
        self.series_combo.addItems(["NACA 4-Digit", "NACA 5-Digit"])
        self.series_combo.currentTextChanged.connect(self.on_series_changed)
        param_layout.addRow("Series:", self.series_combo)
        
        self.code_input = QLineEdit("2412")
        self.code_input.textChanged.connect(self.update_plot)
        param_layout.addRow("NACA Code:", self.code_input)
        
        self.points_input = QLineEdit("100")
        self.points_input.textChanged.connect(self.update_plot)
        param_layout.addRow("Points:", self.points_input)
        
        self.spacing_combo = QComboBox()
        self.spacing_combo.addItems(["cosine", "linear"])
        self.spacing_combo.currentTextChanged.connect(self.update_plot)
        param_layout.addRow("Spacing:", self.spacing_combo)
        
        self.closed_te_check = QCheckBox("Closed Trailing Edge")
        self.closed_te_check.stateChanged.connect(self.update_plot)
        param_layout.addRow(self.closed_te_check)
        
        param_group.setLayout(param_layout)
        sidebar_layout.addWidget(param_group)

        # Export Group
        export_group = QGroupBox("Export Options")
        export_layout = QVBoxLayout()
        
        btn_export_dat = QPushButton("Export Selig DAT")
        btn_export_dat.clicked.connect(lambda: self.export_file("dat"))
        export_layout.addWidget(btn_export_dat)
        
        btn_export_csv = QPushButton("Export CSV")
        btn_export_csv.clicked.connect(lambda: self.export_file("csv"))
        export_layout.addWidget(btn_export_csv)
        
        btn_export_dxf = QPushButton("Export DXF")
        btn_export_dxf.clicked.connect(lambda: self.export_file("dxf"))
        export_layout.addWidget(btn_export_dxf)
        
        export_group.setLayout(export_layout)
        sidebar_layout.addWidget(export_group)
        
        sidebar_layout.addStretch()
        
        # Branding
        brand_label = QLabel("Developed by Manus AI")
        brand_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        brand_label.setStyleSheet("color: #888; font-style: italic;")
        sidebar_layout.addWidget(brand_label)

        # Main Content
        content_layout = QVBoxLayout()
        self.canvas = AirfoilPlotCanvas(self)
        content_layout.addWidget(self.canvas)
        
        main_layout.addWidget(sidebar)
        main_layout.addLayout(content_layout)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def on_series_changed(self, series):
        if series == "NACA 4-Digit":
            self.code_input.setText("2412")
        else:
            self.code_input.setText("24012")
        self.update_plot()

    def get_coordinates(self):
        try:
            code = self.code_input.text()
            n_points = int(self.points_input.text())
            spacing = self.spacing_combo.currentText()
            closed_te = self.closed_te_check.isChecked()
            
            if self.series_combo.currentText() == "NACA 4-Digit":
                return NACAGenerator.naca4(code, n_points, spacing, closed_te), code
            else:
                return NACAGenerator.naca5(code, n_points, spacing, closed_te), code
        except Exception as e:
            self.status_bar.showMessage(f"Error: {str(e)}", 5000)
            return None, None

    def update_plot(self):
        coords, code = self.get_coordinates()
        if coords:
            xu, yu, xl, yl = coords
            self.canvas.plot_airfoil(xu, yu, xl, yl, code)
            self.status_bar.showMessage("Ready", 2000)

    def export_file(self, fmt):
        coords, code = self.get_coordinates()
        if not coords: return
        
        xu, yu, xl, yl = coords
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", f"NACA_{code}.{fmt}")
        
        if filename:
            try:
                if fmt == "dat":
                    with open(filename, 'w') as f:
                        f.write(f"NACA {code}\n")
                        # Selig format: upper TE to LE, then lower LE to TE
                        for i in range(len(xu)-1, -1, -1):
                            f.write(f"{xu[i]:.6f} {yu[i]:.6f}\n")
                        for i in range(1, len(xl)):
                            f.write(f"{xl[i]:.6f} {yl[i]:.6f}\n")
                elif fmt == "csv":
                    data = np.column_stack([xu, yu, xl, yl])
                    np.savetxt(filename, data, delimiter=',', header="xu,yu,xl,yl", comments='')
                elif fmt == "dxf":
                    # Simple DXF implementation
                    with open(filename, 'w') as f:
                        f.write("0\nSECTION\n2\nENTITIES\n")
                        # Upper surface polyline
                        for i in range(len(xu)-1):
                            f.write(f"0\nLINE\n8\nAirfoil\n10\n{xu[i]}\n20\n{yu[i]}\n11\n{xu[i+1]}\n21\n{yu[i+1]}\n")
                        # Lower surface polyline
                        for i in range(len(xl)-1):
                            f.write(f"0\nLINE\n8\nAirfoil\n10\n{xl[i]}\n20\n{yl[i]}\n11\n{xl[i+1]}\n21\n{yl[i+1]}\n")
                        f.write("0\nENDSEC\n0\nEOF\n")
                
                self.status_bar.showMessage(f"Exported to {filename}", 5000)
            except Exception as e:
                self.status_bar.showMessage(f"Export failed: {str(e)}", 5000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
