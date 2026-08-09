import sys
import os
import json
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QFormLayout, QLineEdit, QComboBox, 
                             QPushButton, QCheckBox, QLabel, QGroupBox, QFileDialog,
                             QStatusBar, QTabWidget, QSlider, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt, QSize
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
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
        self.setWindowTitle("NACA Airfoil Kit Pro - Enterprise Edition")
        self.setMinimumSize(1300, 850)
        self.setStyleSheet(STYLESHEET)
        self.uiuc_data, self.current_coords = [], None
        self.current_name, self.comparison_list = "NACA 2412", {}
        self.load_uiuc_db()
        self.init_ui()
        self.update_all()

    def load_uiuc_db(self):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_path, "uiuc_database.json")
        try:
            with open(db_path, 'r') as f: self.uiuc_data = json.load(f)
        except: self.uiuc_data = []

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        sidebar = QWidget(); sidebar.setFixedWidth(380)
        sidebar_layout = QVBoxLayout(sidebar)

        mode_group = QGroupBox("Operation Mode")
        mode_layout = QVBoxLayout()
        self.mode_combo = QComboBox(); self.mode_combo.addItems(["NACA Generator", "UIUC Database"])
        self.mode_combo.currentIndexChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.mode_combo)
        mode_group.setLayout(mode_layout); sidebar_layout.addWidget(mode_group)

        self.gen_group = QGroupBox("NACA Generator")
        gen_layout = QFormLayout()
        self.series_combo = QComboBox(); self.series_combo.addItems(["NACA 4-Digit", "NACA 5-Digit"])
        self.series_combo.currentTextChanged.connect(self.update_all)
        gen_layout.addRow("Series:", self.series_combo)
        self.code_input = QLineEdit("2412"); self.code_input.textChanged.connect(self.update_all)
        gen_layout.addRow("Code:", self.code_input)
        self.points_slider = QSlider(Qt.Orientation.Horizontal); self.points_slider.setRange(20, 500); self.points_slider.setValue(100)
        self.points_slider.valueChanged.connect(self.update_all)
        gen_layout.addRow("Points:", self.points_slider)
        self.gen_group.setLayout(gen_layout); sidebar_layout.addWidget(self.gen_group)

        self.db_group = QGroupBox("UIUC Database")
        db_layout = QVBoxLayout()
        self.search_input = QLineEdit(); self.search_input.setPlaceholderText("Search airfoil...")
        self.search_input.textChanged.connect(self.filter_db)
        db_layout.addWidget(self.search_input)
        self.db_list = QListWidget(); self.db_list.itemClicked.connect(self.load_uiuc_airfoil)
        db_layout.addWidget(self.db_list)
        self.db_group.setLayout(db_layout); self.db_group.hide(); sidebar_layout.addWidget(self.db_group)

        comp_group = QGroupBox("Comparison Suite")
        comp_layout = QVBoxLayout()
        self.comp_list_widget = QListWidget(); self.comp_list_widget.setFixedHeight(100)
        comp_layout.addWidget(self.comp_list_widget)
        btn_add_comp = QPushButton("Add to Comparison"); btn_add_comp.clicked.connect(self.add_to_comparison)
        comp_layout.addWidget(btn_add_comp)
        comp_group.setLayout(comp_layout); sidebar_layout.addWidget(comp_group)

        opt_group = QGroupBox("Smart Optimization")
        opt_layout = QFormLayout()
        self.target_cl_input = QLineEdit("0.5"); opt_layout.addRow("Target Cl:", self.target_cl_input)
        btn_opt_cl = QPushButton("Match Cl"); btn_opt_cl.clicked.connect(self.optimize_cl); opt_layout.addRow(btn_opt_cl)
        btn_opt_ld = QPushButton("Maximize L/D"); btn_opt_ld.clicked.connect(self.optimize_ld); opt_layout.addRow(btn_opt_ld)
        opt_group.setLayout(opt_layout); sidebar_layout.addWidget(opt_group)

        analysis_group = QGroupBox("Aero Analysis")
        analysis_layout = QFormLayout()
        self.alpha_slider = QSlider(Qt.Orientation.Horizontal); self.alpha_slider.setRange(-10, 20); self.alpha_slider.setValue(0)
        self.alpha_slider.valueChanged.connect(self.update_all)
        analysis_layout.addRow("Alpha:", self.alpha_slider)
        self.re_input = QLineEdit("1000000"); self.re_input.textChanged.connect(self.update_all)
        analysis_layout.addRow("Reynolds:", self.re_input)
        self.rough_input = QLineEdit("0.0"); self.rough_input.textChanged.connect(self.update_all)
        analysis_layout.addRow("Roughness (k/c):", self.rough_input)
        self.cl_label = QLabel("Cl: 0.000"); self.cl_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        self.cd_label = QLabel("Cd: 0.000"); self.cd_label.setStyleSheet("color: #ffaa00; font-weight: bold;")
        self.ld_label = QLabel("L/D: 0.00"); self.ld_label.setStyleSheet("color: #00aaff; font-weight: bold;")
        analysis_layout.addRow(self.cl_label, self.cd_label); analysis_layout.addRow(self.ld_label)
        analysis_group.setLayout(analysis_layout); sidebar_layout.addWidget(analysis_group)

        sidebar_layout.addStretch()
        btn_anim = QPushButton("Export Flow Animation (GIF)"); btn_anim.clicked.connect(self.export_animation)
        btn_anim.setStyleSheet("background-color: #00b294;"); sidebar_layout.addWidget(btn_anim)
        btn_report = QPushButton("Generate PDF Report"); btn_report.clicked.connect(self.export_pdf)
        btn_report.setStyleSheet("background-color: #d83b01;"); sidebar_layout.addWidget(btn_report)
        btn_export = QPushButton("Export Suite"); btn_export.clicked.connect(self.show_export_dialog)
        sidebar_layout.addWidget(btn_export)

        self.tabs = QTabWidget()
        self.geom_canvas = MplCanvas(self); self.tabs.addTab(self.geom_canvas, "Geometry")
        self.press_canvas = MplCanvas(self); self.tabs.addTab(self.press_canvas, "Pressure (Cp)")
        self.stream_canvas = MplCanvas(self); self.tabs.addTab(self.stream_canvas, "Flow Field")
        
        main_layout.addWidget(sidebar); main_layout.addWidget(self.tabs)
        self.status_bar = QStatusBar(); self.setStatusBar(self.status_bar); self.filter_db()

    def add_to_comparison(self):
        if self.current_coords:
            name = self.current_name
            if name not in self.comparison_list:
                self.comparison_list[name] = self.current_coords
                self.comp_list_widget.addItem(name); self.update_plots()

    def on_mode_changed(self, index):
        if index == 0: self.gen_group.show(); self.db_group.hide()
        else: self.gen_group.hide(); self.db_group.show()
        self.update_all()

    def filter_db(self):
        self.db_list.clear(); query = self.search_input.text().lower()
        for item in self.uiuc_data:
            if query in item['name'].lower(): self.db_list.addItem(item['name'])

    def load_uiuc_airfoil(self, item):
        name = item.text(); self.current_name = name
        url = next(i['url'] for i in self.uiuc_data if i['name'] == name)
        coords = UIUCLoader.load_from_url(url)
        if coords: self.current_coords = coords; self.update_plots()

    def optimize_cl(self):
        if self.mode_combo.currentIndex() != 0: return
        try:
            target, code = float(self.target_cl_input.text()), self.code_input.text()
            series = '4-digit' if self.series_combo.currentIndex() == 0 else '5-digit'
            self.code_input.setText(GeometryOptimizer.match_cl(code, target, series))
        except: pass

    def optimize_ld(self):
        if self.mode_combo.currentIndex() != 0: return
        try:
            code, alpha, re = self.code_input.text(), self.alpha_slider.value(), float(self.re_input.text())
            series = '4-digit' if self.series_combo.currentIndex() == 0 else '5-digit'
            new_code, best_ld = GeometryOptimizer.optimize_ld(code, alpha, re, series)
            self.code_input.setText(new_code)
            self.status_bar.showMessage(f"Optimized for L/D: {best_ld:.2f}", 5000)
        except: pass

    def update_all(self):
        if self.mode_combo.currentIndex() == 0:
            code = self.code_input.text(); self.current_name = f"NACA {code}"
            n_pts = self.points_slider.value()
            if self.series_combo.currentIndex() == 0: self.current_coords = NACAGeneratorPro.naca4(code, n_pts)
            else: self.current_coords = NACAGeneratorPro.naca5(code, n_pts)
        self.update_plots()

    def update_plots(self):
        if not self.current_coords: return
        xu, yu, xl, yl = self.current_coords
        alpha, re, rough = self.alpha_slider.value(), float(self.re_input.text() or 1e6), float(self.rough_input.text() or 0.0)
        
        res = AirfoilAnalysis.compute_aerodynamics(xu, yu, xl, yl, alpha, re, rough)
        self.last_cl, self.last_cd, self.last_cp, self.last_xc, self.last_gamma, self.last_pxc, self.last_pyc, self.last_pl = res
        self.cl_label.setText(f"Cl: {self.last_cl:.4f}"); self.cd_label.setText(f"Cd: {self.last_cd:.4f}")
        self.ld_label.setText(f"L/D: {self.last_cl/self.last_cd:.2f}" if self.last_cd > 0 else "L/D: N/A")
        
        ax = self.geom_canvas.axes; ax.clear()
        colors = ['#555', '#777', '#999', '#bbb']
        for i, (name, coords) in enumerate(self.comparison_list.items()):
            ax.plot(coords[0], coords[1], color=colors[i % len(colors)], linestyle='--', alpha=0.5)
            ax.plot(coords[2], coords[3], color=colors[i % len(colors)], linestyle='--', alpha=0.5)
        ax.plot(xu, yu, '#00aaff', xl, yl, '#ff5500', linewidth=2.5)
        ax.fill(np.concatenate([xu, xl[::-1]]), np.concatenate([yu, yl[::-1]]), '#333', alpha=0.3)
        ax.set_aspect('equal'); ax.grid(True, color='#333', linestyle=':'); self.geom_canvas.draw()
        
        axp = self.press_canvas.axes; axp.clear()
        axp.plot(self.last_xc, self.last_cp, '#00ff00', linewidth=2); axp.invert_yaxis()
        axp.grid(True, color='#333'); self.press_canvas.draw()

        axs = self.stream_canvas.axes; axs.clear()
        X, Y, u, v = AirfoilAnalysis.get_streamlines(xu, yu, xl, yl, alpha, self.last_gamma, self.last_pxc, self.last_pyc, self.last_pl)
        axs.streamplot(X, Y, u, v, color='#00aaff', linewidth=1, density=1.5)
        axs.fill(np.concatenate([xu, xl[::-1]]), np.concatenate([yu, yl[::-1]]), 'white', zorder=10)
        axs.set_aspect('equal'); axs.set_xlim(-0.5, 1.5); axs.set_ylim(-0.5, 0.5)
        axs.grid(True, color='#333'); self.stream_canvas.draw()

    def export_animation(self):
        if not self.current_coords: return
        path, _ = QFileDialog.getSaveFileName(self, "Save Flow Animation", f"{self.current_name}_Flow.gif", "GIF (*.gif)")
        if not path: return
        self.status_bar.showMessage("Generating animation...", 0)
        fig = Figure(figsize=(8, 4), facecolor='#1e1e1e')
        ax = fig.add_subplot(111); ax.set_facecolor('#1e1e1e')
        xu, yu, xl, yl = self.current_coords
        alphas = np.linspace(-5, 15, 20)
        def update(i):
            ax.clear(); alpha = alphas[i]
            res = AirfoilAnalysis.compute_aerodynamics(xu, yu, xl, yl, alpha)
            _, _, _, _, gamma, pxc, pyc, pl = res
            X, Y, u, v = AirfoilAnalysis.get_streamlines(xu, yu, xl, yl, alpha, gamma, pxc, pyc, pl)
            ax.streamplot(X, Y, u, v, color='#00aaff', linewidth=1, density=1.2)
            ax.fill(np.concatenate([xu, xl[::-1]]), np.concatenate([yu, yl[::-1]]), 'white', zorder=10)
            ax.set_aspect('equal'); ax.set_xlim(-0.5, 1.5); ax.set_ylim(-0.5, 0.5)
            ax.set_title(f"Alpha={alpha:.1f} deg", color='white')
            return ax,
        anim = animation.FuncAnimation(fig, update, frames=len(alphas), interval=100)
        try: anim.save(path, writer='pillow'); self.status_bar.showMessage(f"Saved to {path}", 5000)
        except Exception as e: self.status_bar.showMessage(f"Error: {str(e)}", 5000)

    def export_pdf(self):
        if not self.current_coords: return
        path, _ = QFileDialog.getSaveFileName(self, "Save PDF Report", f"{self.current_name}_Report.pdf", "PDF (*.pdf)")
        if not path: return
        temp_plot = "temp_plot.png"
        self.geom_canvas.fig.savefig(temp_plot, facecolor='#ffffff')
        data = {'name': self.current_name, 'cl': self.last_cl, 'cd': self.last_cd, 'params': {'Alpha': f"{self.alpha_slider.value()} deg", 'Reynolds': self.re_input.text(), 'Roughness': self.rough_input.text()}, 'plot_path': temp_plot}
        try: generate_pdf_report(path, data); self.status_bar.showMessage(f"Report saved", 5000)
        except Exception as e: self.status_bar.showMessage(f"PDF Error: {str(e)}", 5000)
        finally:
            if os.path.exists(temp_plot): os.remove(temp_plot)

    def show_export_dialog(self):
        if not self.current_coords: return
        path, _ = QFileDialog.getSaveFileName(self, "Export Airfoil", "airfoil.csv", "Advanced CSV (*.csv);;STL (*.stl);;DAT (*.dat);;DXF (*.dxf)")
        if not path: return
        xu, yu, xl, yl = self.current_coords
        if path.endswith('.csv'): export_csv_advanced(xu, yu, xl, yl, self.last_xc, self.last_cp, path)
        elif path.endswith('.stl'): export_stl(xu, yu, xl, yl, path)
        elif path.endswith('.dat'):
            with open(path, 'w') as f:
                for i in range(len(xu)-1, -1, -1): f.write(f"{xu[i]:.6f} {yu[i]:.6f}\n")
                for i in range(1, len(xl)): f.write(f"{xl[i]:.6f} {yl[i]:.6f}\n")
        elif path.endswith('.dxf'):
            with open(path, 'w') as f:
                f.write("0\nSECTION\n2\nENTITIES\n")
                for i in range(len(xu)-1): f.write(f"0\nLINE\n8\n0\n10\n{xu[i]}\n20\n{yu[i]}\n11\n{xu[i+1]}\n21\n{yu[i+1]}\n")
                f.write("0\nENDSEC\n0\nEOF\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
