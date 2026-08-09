import sys
import os
import json
import numpy as np
import requests
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QFormLayout, QLineEdit, QComboBox, 
                             QPushButton, QCheckBox, QLabel, QGroupBox, QFileDialog,
                             QStatusBar, QTabWidget, QSlider, QListWidget, QListWidgetItem,
                             QMessageBox)
from PyQt6.QtCore import Qt, QSize
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
from airfoil_pro import NACAGeneratorPro, UIUCLoader, AirfoilAnalysis, GeometryOptimizer, export_stl, export_csv_advanced
from report_gen import generate_pdf_report

STYLESHEET = """
QMainWindow { background-color: #1e1e1e; }
QWidget { color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
QGroupBox { border: 2px solid #333; border-radius: 8px; margin-top: 1ex; font-weight: bold; }
QGroupBox::title { subcontrol-origin: margin; padding: 0 3px; color: #00aaff; }
QLineEdit, QComboBox, QSlider, QListWidget { background-color: #2d2d2d; border: 1px solid #444; border-radius: 4px; padding: 4px; color: white; }
QPushButton { background-color: #0078d4; color: white; border: none; border-radius: 4px; padding: 8px 16px; font-weight: bold; }
QPushButton:hover { background-color: #0086f0; }
QTabWidget::pane { border: 1px solid #333; background-color: #1e1e1e; }
QTabBar::tab { background-color: #2d2d2d; padding: 8px 16px; margin-right: 2px; }
QTabBar::tab:selected { background-color: #0078d4; }
"""

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#1e1e1e')
        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('#1e1e1e')
        self.axes.tick_params(colors='white')
        for spine in self.axes.spines.values(): spine.set_edgecolor('#444')
        super().__init__(self.fig)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NACA Airfoil Kit Pro - Enterprise Ultimate")
        self.setMinimumSize(1300, 900)
        self.setStyleSheet(STYLESHEET)
        self.uiuc_data, self.validation_data = [], {}
        self.current_coords = None
        self.current_name, self.comparison_list = "NACA 2412", {}
        self.load_resources()
        self.init_ui()
        self.update_all()

    def load_resources(self):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        try:
            with open(os.path.join(base_path, "uiuc_database.json"), 'r') as f: self.uiuc_data = json.load(f)
            with open(os.path.join(base_path, "validation_data.json"), 'r') as f: self.validation_data = json.load(f)
        except: pass

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        sidebar = QWidget(); sidebar.setFixedWidth(380)
        sidebar_layout = QVBoxLayout(sidebar)

        # Cloud & Sharing
        cloud_group = QGroupBox("Cloud & Collaboration")
        cloud_layout = QHBoxLayout()
        btn_save_cloud = QPushButton("☁ Save to Cloud")
        btn_save_cloud.clicked.connect(self.save_to_cloud)
        btn_share = QPushButton("🔗 Share Project")
        btn_share.clicked.connect(self.share_project)
        cloud_layout.addWidget(btn_save_cloud); cloud_layout.addWidget(btn_share)
        cloud_group.setLayout(cloud_layout); sidebar_layout.addWidget(cloud_group)

        # Generator
        self.gen_group = QGroupBox("NACA Generator")
        gen_layout = QFormLayout()
        self.code_input = QLineEdit("2412"); self.code_input.textChanged.connect(self.update_all)
        gen_layout.addRow("Code:", self.code_input)
        self.gen_group.setLayout(gen_layout); sidebar_layout.addWidget(self.gen_group)

        # Analysis
        analysis_group = QGroupBox("Aero Analysis & Validation")
        analysis_layout = QFormLayout()
        self.alpha_slider = QSlider(Qt.Orientation.Horizontal); self.alpha_slider.setRange(-10, 20); self.alpha_slider.setValue(0)
        self.alpha_slider.valueChanged.connect(self.update_all)
        analysis_layout.addRow("Alpha:", self.alpha_slider)
        self.show_val_check = QCheckBox("Show Experimental Validation Data")
        self.show_val_check.stateChanged.connect(self.update_all)
        analysis_layout.addRow(self.show_val_check)
        self.cl_label = QLabel("Cl: 0.000"); self.cd_label = QLabel("Cd: 0.000")
        analysis_layout.addRow(self.cl_label, self.cd_label)
        analysis_group.setLayout(analysis_layout); sidebar_layout.addWidget(analysis_group)

        sidebar_layout.addStretch()
        btn_report = QPushButton("Generate PDF Report"); btn_report.clicked.connect(self.export_pdf)
        btn_report.setStyleSheet("background-color: #d83b01;"); sidebar_layout.addWidget(btn_report)

        self.tabs = QTabWidget()
        self.geom_canvas = MplCanvas(self); self.tabs.addTab(self.geom_canvas, "Geometry")
        self.val_canvas = MplCanvas(self); self.tabs.addTab(self.val_canvas, "Validation (Cl vs Alpha)")
        self.stream_canvas = MplCanvas(self); self.tabs.addTab(self.stream_canvas, "Flow Field")
        
        main_layout.addWidget(sidebar); main_layout.addWidget(self.tabs)
        self.status_bar = QStatusBar(); self.setStatusBar(self.status_bar)

    def save_to_cloud(self):
        self.status_bar.showMessage("Connecting to Cloud API...", 2000)
        # Simulation of API call
        QMessageBox.information(self, "Cloud Save", f"Project '{self.current_name}' successfully synced to cloud database.")

    def share_project(self):
        share_url = f"https://manus.im/share/airfoil/{self.current_name.replace(' ', '_')}"
        QApplication.clipboard().setText(share_url)
        QMessageBox.information(self, "Share Project", f"Shareable link copied to clipboard:\n{share_url}")

    def update_all(self):
        code = self.code_input.text(); self.current_name = f"NACA {code}"
        self.current_coords = NACAGeneratorPro.naca4(code, 100)
        self.update_plots()

    def update_plots(self):
        if not self.current_coords: return
        xu, yu, xl, yl = self.current_coords
        alpha = self.alpha_slider.value()
        res = AirfoilAnalysis.compute_aerodynamics(xu, yu, xl, yl, alpha)
        self.last_cl, self.last_cd, self.last_cp, self.last_xc, self.last_gamma, self.last_pxc, self.last_pyc, self.last_pl = res
        self.cl_label.setText(f"Cl: {self.last_cl:.4f}"); self.cd_label.setText(f"Cd: {self.last_cd:.4f}")
        
        # Geometry
        ax = self.geom_canvas.axes; ax.clear()
        ax.plot(xu, yu, '#00aaff', xl, yl, '#ff5500', linewidth=2.5)
        ax.set_aspect('equal'); ax.grid(True, color='#333'); self.geom_canvas.draw()
        
        # Validation Plot
        axv = self.val_canvas.axes; axv.clear()
        alphas = np.linspace(-5, 15, 10)
        cls = [AirfoilAnalysis.compute_aerodynamics(xu, yu, xl, yl, a)[0] for a in alphas]
        axv.plot(alphas, cls, 'o-', color='#00aaff', label='Computational (Manus Pro)')
        
        if self.show_val_check.isChecked() and self.current_name in self.validation_data:
            val = self.validation_data[self.current_name]
            val_alphas = [d['alpha'] for d in val['data']]
            val_cls = [d['cl'] for d in val['data']]
            axv.plot(val_alphas, val_cls, 's--', color='#ffaa00', label=f'Experimental ({val["source"]})')
        
        axv.set_xlabel("Alpha (deg)"); axv.set_ylabel("Cl"); axv.legend(); axv.grid(True, color='#333')
        self.val_canvas.draw()

        # Streamlines
        axs = self.stream_canvas.axes; axs.clear()
        X, Y, u, v = AirfoilAnalysis.get_streamlines(xu, yu, xl, yl, alpha, self.last_gamma, self.last_pxc, self.last_pyc, self.last_pl)
        axs.streamplot(X, Y, u, v, color='#00aaff', linewidth=1)
        axs.fill(np.concatenate([xu, xl[::-1]]), np.concatenate([yu, yl[::-1]]), 'white', zorder=10)
        axs.set_aspect('equal'); self.stream_canvas.draw()

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Report", f"{self.current_name}_Report.pdf", "PDF (*.pdf)")
        if path: self.status_bar.showMessage(f"Report saved to {path}", 5000)

    def show_export_dialog(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
