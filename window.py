from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTabWidget, QHBoxLayout, \
    QSlider, QLabel
from myCanvas import MyCanvas

class Application:
    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle("Fast Voxel intersection algorithm")
        self.font = QFont("Arial", 16)

        self.canvas = MyCanvas()
        self.slider = QSlider(Qt.Horizontal)

        main_layout = QVBoxLayout()

        self.onglets = QTabWidget()
        self.onglets.addTab(self.create_canvas_tab(), "Canvas")
        self.onglets.addTab(self.create_calculation_tab(), "Calculation")

        main_layout.addWidget(self.onglets)
        self.window.setLayout(main_layout)

    def create_canvas_tab(self):
        onglet1 = QWidget()
        horizontal_layout = QHBoxLayout()

        vertical_layout = QVBoxLayout()
        label_slider = QLabel("Vox size")
        label_slider.setFont(self.font)
        self.slider.setFixedSize(200,20)
        self.slider.setMinimum(5)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.setTickInterval(15)
        self.slider.valueChanged.connect(self.slider_value_changed)
        vertical_layout.addWidget(label_slider, alignment=Qt.AlignHCenter)
        vertical_layout.addWidget(self.slider)
        vertical_layout.addStretch()

        horizontal_layout.addWidget(self.canvas)
        horizontal_layout.setSpacing(30)
        horizontal_layout.addLayout(vertical_layout)

        onglet1.setLayout(horizontal_layout)
        return onglet1

    def create_calculation_tab(self):
        onglet2 = QWidget()
        return onglet2

    def run(self):
        self.window.show()
        self.app.exec_()

    def slider_value_changed(self):
        self.canvas.set_bloc_size(self.slider.value())
        self.canvas.update()
