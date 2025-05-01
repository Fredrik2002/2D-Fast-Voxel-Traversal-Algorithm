from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QFont, QPen, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTabWidget, QHBoxLayout, \
    QSlider, QLabel, QLineEdit

from FastVoxelTransversal import FastVoxelTraversal

WIDTH = 500
HEIGHT = 500
RADIUS = 2

class Application:
    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle("Fast Voxel traversal algorithm visualizer")
        self.font = QFont("Arial", 16)

        self.canvas = MyCanvas(self)
        self.slider = QSlider(Qt.Horizontal)

        self.point1_x_entry: QLineEdit = None
        self.point1_y_entry: QLineEdit = None

        self.point2_x_entry: QLineEdit = None
        self.point2_y_entry: QLineEdit = None

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.create_canvas_tab())
        main_layout.addWidget(self.create_calculation_tab())

        self.window.setLayout(main_layout)

    def create_canvas_tab(self):
        onglet1 = QWidget()
        horizontal_layout = QHBoxLayout()

        vertical_layout = QVBoxLayout()
        label_slider = QLabel("Vox size")
        label_slider.setFont(self.font)
        self.slider.setMinimum(5)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.setTickInterval(15)
        self.slider.valueChanged.connect(self.slider_value_changed)

        reset_button = QPushButton("Reset points")
        reset_button.setFont(self.font)
        reset_button.clicked.connect(self.reset_button_pressed)

        point1_label = QLabel("Point 1 :")
        point1_label.setFont(self.font)
        point1_coordinates = self.create_point_coordinates_entry()
        self.point1_x_entry : QLineEdit = point1_coordinates.itemAt(1).widget()
        self.point1_y_entry : QLineEdit = point1_coordinates.itemAt(3).widget()
        self.point1_x_entry.textEdited.connect(self.entry_management)
        self.point1_y_entry.textEdited.connect(self.entry_management)

        point2_label = QLabel("Point 2 :")
        point2_label.setFont(self.font)
        point2_coordinates = self.create_point_coordinates_entry()
        self.point2_x_entry : QLineEdit = point2_coordinates.itemAt(1).widget()
        self.point2_y_entry : QLineEdit = point2_coordinates.itemAt(3).widget()
        self.point2_x_entry.textEdited.connect(self.entry_management)
        self.point2_y_entry.textEdited.connect(self.entry_management)

        vertical_layout.addWidget(label_slider, alignment=Qt.AlignHCenter)
        vertical_layout.addWidget(self.slider)
        vertical_layout.addWidget(reset_button)
        vertical_layout.addWidget(point1_label)
        vertical_layout.addLayout(point1_coordinates)
        vertical_layout.addWidget(point2_label)
        vertical_layout.addLayout(point2_coordinates)
        vertical_layout.addStretch()

        horizontal_layout.addWidget(self.canvas)
        horizontal_layout.setSpacing(30)
        horizontal_layout.addLayout(vertical_layout)

        onglet1.setLayout(horizontal_layout)
        return onglet1

    def create_point_coordinates_entry(self):
        horizontal_layout = QHBoxLayout()
        x_label = QLabel("𝑥 :")
        x_label.setFont(self.font)
        y_label = QLabel("𝑦 :")
        y_label.setFont(self.font)

        x_entry = QLineEdit()
        x_entry.setFont(self.font)
        x_entry.setFixedWidth(100)
        y_entry = QLineEdit()
        y_entry.setFont(self.font)
        y_entry.setFixedWidth(100)

        horizontal_layout.addWidget(x_label)
        horizontal_layout.addWidget(x_entry)
        horizontal_layout.addWidget(y_label)
        horizontal_layout.addWidget(y_entry)

        return horizontal_layout

    def create_calculation_tab(self):
        onglet2 = QWidget()
        return onglet2

    def run(self):
        self.window.show()
        self.app.exec_()

    def slider_value_changed(self):
        self.canvas.set_bloc_size(self.slider.value())
        self.reset_button_pressed()

    def reset_button_pressed(self):
        self.canvas.clear_points()
        self.point1_x_entry.setText("")
        self.point1_y_entry.setText("")
        self.point2_x_entry.setText("")
        self.point2_y_entry.setText("")

    def entry_management(self):
        try:
            p1_x = float(self.point1_x_entry.text())
            p1_y = float(self.point1_y_entry.text())
            if p1_x < 0 or p1_y < 0:
                raise ValueError()
            self.canvas.p1 = QPoint(*self.canvas.coordinates_to_pixels(p1_x, p1_y))

        except ValueError:
            self.canvas.p1 = None

        try:
            p2_x = float(self.point2_x_entry.text())
            p2_y = float(self.point2_y_entry.text())
            if p2_x < 0 or p2_y < 0:
                raise ValueError()
            self.canvas.p2 = QPoint(*self.canvas.coordinates_to_pixels(p2_x, p2_y))
        except ValueError:
            self.canvas.p2 = None
        self.canvas.update()


class MyCanvas(QWidget):
    def __init__(self, window : Application):
        super().__init__()
        self.main_app = window
        self.setMinimumSize(WIDTH+2*RADIUS+5, HEIGHT+2*RADIUS+5)
        self.bloc_size = 50
        self.p1 = None
        self.p2 = None

        self.voxel_number_x = WIDTH // self.bloc_size
        self.voxel_number_y = HEIGHT // self.bloc_size

        self.offset_x = (WIDTH % self.bloc_size) // 2 + RADIUS
        self.offset_y = (HEIGHT % self.bloc_size) // 2 + RADIUS

    def set_bloc_size(self, bloc_size):
        self.bloc_size = bloc_size
        self.voxel_number_x = WIDTH // self.bloc_size
        self.voxel_number_y = HEIGHT // self.bloc_size

        self.offset_x = (WIDTH % self.bloc_size) // 2 + RADIUS
        self.offset_y = (HEIGHT % self.bloc_size) // 2 + RADIUS

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.black, 1)
        painter.setPen(pen)
        self.draw_grid(painter)
        self.draw_segment_and_rectangles(painter)
        self.draw_points(painter)

    def draw_grid(self, painter):
        for i in range(self.voxel_number_x+1):
            painter.drawLine(i*self.bloc_size+self.offset_x, self.offset_y,
                             i*self.bloc_size+self.offset_x, self.voxel_number_x*self.bloc_size+self.offset_y)
        for i in range(self.voxel_number_y+1):
            painter.drawLine(                                   self.offset_x, i*self.bloc_size+self.offset_y,
                             self.voxel_number_y*self.bloc_size+self.offset_x, i*self.bloc_size+self.offset_y)

    def draw_points(self, painter):
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        if self.p1 is not None:
            painter.drawEllipse(self.p1.x()-RADIUS, self.p1.y()-RADIUS, 2*RADIUS, 2*RADIUS)
        if self.p2 is not None:
            painter.drawEllipse(self.p2.x()-RADIUS, self.p2.y()-RADIUS, 2*RADIUS, 2*RADIUS)

    def update_entry(self):
        if self.p1 is not None:
            x_value = (self.p1.x()-self.offset_x)/self.bloc_size
            y_value = self.voxel_number_y - (self.p1.y()-self.offset_y) /self.bloc_size
            self.main_app.point1_x_entry.setText(str(round(x_value, 2)))
            self.main_app.point1_y_entry.setText(str(round(y_value, 2)))
        if self.p2 is not None:
            x_value = (self.p2.x() - self.offset_x) / self.bloc_size
            y_value = self.voxel_number_y - (self.p2.y() - self.offset_y) / self.bloc_size
            self.main_app.point2_x_entry.setText(str(round(x_value, 2)))
            self.main_app.point2_y_entry.setText(str(round(y_value, 2)))

    def mousePressEvent(self, event):
        point: QPoint = event.pos()
        if point.x() < self.offset_x:
            point.setX(self.offset_x)
        if point.x() > self.voxel_number_x*self.bloc_size + self.offset_x:
            point.setX(self.voxel_number_x*self.bloc_size + self.offset_x)
        if point.y() < self.offset_y:
            point.setY(self.offset_y)
        if point.y() > self.voxel_number_y*self.bloc_size + self.offset_y:
            point.setY(self.voxel_number_y*self.bloc_size + self.offset_y)
        if self.p1 is None:
            self.p1 = point
            self.update_entry()
            self.update()
        elif self.p2 is None:
            self.p2 = point
            self.update_entry()
            self.update()

    def draw_segment_and_rectangles(self, painter):
        if self.p1 is None or self.p2 is None:
            return

        start = (float(self.main_app.point1_x_entry.text()), float(self.main_app.point1_y_entry.text()))
        end = (float(self.main_app.point2_x_entry.text()), float(self.main_app.point2_y_entry.text()))

        pen = QPen(Qt.green, 1)
        painter.setBrush(QBrush(Qt.green))
        painter.setPen(pen)

        voxels = FastVoxelTraversal(start, end)
        print(voxels)
        for x,y in voxels:
            x_coord = self.offset_x + self.bloc_size*x
            y_coord = self.offset_y + self.bloc_size*(self.voxel_number_y - y - 1)
            painter.drawRect(x_coord+1, y_coord+1, self.bloc_size-2, self.bloc_size-2)

        pen = QPen(Qt.black, 3)
        painter.setPen(pen)
        painter.drawLine(self.p1, self.p2)


    def coordinates_to_pixels(self, x, y):
        return int(x*self.bloc_size+self.offset_x), int((self.voxel_number_y-y)*self.bloc_size+self.offset_y)

    def clear_points(self):
        self.p1 = None
        self.p2 = None
        self.update()
