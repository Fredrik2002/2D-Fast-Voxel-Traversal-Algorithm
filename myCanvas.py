from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget


class MyCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.WIDTH, self.HEIGHT = 501, 501
        self.setMinimumSize(self.WIDTH, self.HEIGHT)
        self.bloc_size = 50

    def set_bloc_size(self, bloc_size):
        self.bloc_size = bloc_size

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.black, 1)
        painter.setPen(pen)
        self.draw_grid(painter)


    def draw_grid(self, painter):
        nb_x = self.WIDTH // self.bloc_size
        nb_y = self.HEIGHT // self.bloc_size
        offset_x = (self.WIDTH % self.bloc_size)//2
        offset_y = (self.HEIGHT % self.bloc_size)//2
        for i in range(nb_x+1):
            painter.drawLine(i*self.bloc_size+offset_x, offset_y, i*self.bloc_size+offset_x, nb_x*self.bloc_size+offset_y)
        for i in range(nb_y+1):
            painter.drawLine(offset_x, i*self.bloc_size+offset_y, nb_y*self.bloc_size+offset_x, i*self.bloc_size+offset_y)