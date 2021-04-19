import logging
import sys

import PySide2
import numpy as np
from itertools import product, combinations
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import axes3d
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QKeySequence, QColor
from PySide2.QtWidgets import (QAction, QApplication, QComboBox, QHBoxLayout,
                               QHeaderView, QLabel, QMainWindow, QSlider,
                               QTableWidget, QTableWidgetItem, QVBoxLayout,
                               QWidget)

import Ingest
import Sort
import palletize
from lib.Container import Container
from lib.Item import Item

import hashlib


def init(data) -> list:
    items = []
    for item in data.iterrows():
        obj = Item(item[1]["Length"], item[1]["Width"], item[1]["Height"], item[1]["Weight"],
                   str(item[1]["Code/Serial Number"]))
        items.append(obj)
    return items


class ApplicationWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        logi = [0, 0, 0]
        self.container = Container(0, 0, 0, logi, 100, 10, 5)

        self.column_names = ["Color", "Serial"]

        # Central widget
        self._main = QWidget()
        self.setCentralWidget(self._main)

        # Main menu bar
        self.menu = self.menuBar()
        self.menu_file = self.menu.addMenu("File")
        exit = QAction("Exit", self, triggered=qApp.quit)
        self.menu_file.addAction(exit)

        self.menu_about = self.menu.addMenu("&About")
        about = QAction("About Qt", self, shortcut=QKeySequence(QKeySequence.HelpContents),
                        triggered=qApp.aboutQt)
        self.menu_about.addAction(about)

        # Figure (Left)
        self.fig = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.fig)

        # Sliders (Left)
        self.slider_azim = QSlider(minimum=0, maximum=360, orientation=Qt.Horizontal)
        self.slider_elev = QSlider(minimum=0, maximum=360, orientation=Qt.Horizontal)

        self.slider_azim_layout = QHBoxLayout()
        self.slider_azim_layout.addWidget(QLabel("{}".format(self.slider_azim.minimum())))
        self.slider_azim_layout.addWidget(self.slider_azim)
        self.slider_azim_layout.addWidget(QLabel("{}".format(self.slider_azim.maximum())))

        self.slider_elev_layout = QHBoxLayout()
        self.slider_elev_layout.addWidget(QLabel("{}".format(self.slider_elev.minimum())))
        self.slider_elev_layout.addWidget(self.slider_elev)
        self.slider_elev_layout.addWidget(QLabel("{}".format(self.slider_elev.maximum())))

        # Table (Right)
        self.table = QTableWidget()
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # ComboBox (Right)
        self.combo = QComboBox()
        self.load_list()
        items = []
        for i in range(len(self.shipment)):
            items.append(f"Crate {1 + i}")
        self.combo.addItems(items)

        # Right layout
        rlayout = QVBoxLayout()
        rlayout.setContentsMargins(1, 1, 1, 1)
        rlayout.addWidget(QLabel("Plot type:"))
        rlayout.addWidget(self.combo)
        rlayout.addWidget(self.table)

        # Left layout
        llayout = QVBoxLayout()
        rlayout.setContentsMargins(1, 1, 1, 1)
        llayout.addWidget(self.canvas, 88)
        llayout.addWidget(QLabel("Azimuth:"), 1)
        llayout.addLayout(self.slider_azim_layout, 5)
        llayout.addWidget(QLabel("Elevation:"), 1)
        llayout.addLayout(self.slider_elev_layout, 5)

        # Main layout
        layout = QHBoxLayout(self._main)
        layout.addLayout(llayout, 70)
        layout.addLayout(rlayout, 30)

        # Signal and Slots connections
        self.combo.currentTextChanged.connect(self.combo_option)
        self.slider_azim.valueChanged.connect(self.rotate_azim)
        self.slider_elev.valueChanged.connect(self.rotate_elev)

        # Initial setup
        self.plot_dyn_cube(self.shipment, 0)
        self._ax.view_init(30, 30)
        self.slider_azim.setValue(30)
        self.slider_elev.setValue(30)
        # self.fig.canvas.mpl_connect("button_release_event", self.on_click)

    # Matplotlib slot method
    def on_click(self, event):
        azim, elev = self._ax.azim, self._ax.elev
        self.slider_azim.setValue(azim + 180)
        self.slider_elev.setValue(elev + 180)

    # Utils methods

    def set_table_data(self, X, Y, Z):
        for i in range(len(X)):
            self.table.setItem(i, 0, QTableWidgetItem("{:.2f}".format(X[i])))
            self.table.setItem(i, 1, QTableWidgetItem("{:.2f}".format(Y[i])))
            self.table.setItem(i, 2, QTableWidgetItem("{:.2f}".format(Z[i])))

    def clear_table_data(self):
        for i in range(self.table.rowCount()):
            for j in range(self.table.colorCount()):
                self.table.setItem(i, j, QTableWidgetItem(""))

    def set_table_data_container(self, data):
        self.clear_table_data()
        table_row = 0
        seen = []
        for i in range(len(data)):
            if data[i].item is None or data[i].item.get_serial() in seen:
                continue

            color = QColor()
            hex_code = f'#{self.serial_hash(data[i].item.get_serial())}'
            color.setNamedColor(hex_code)
            print(hex_code, table_row)
            item = QTableWidgetItem("new Item").setBackground(color)
            self.table.setItem(table_row, 0, item)
            # self.table.item(table_row, 0)
            self.table.setItem(table_row, 1, QTableWidgetItem(data[i].item.get_serial()))
            table_row += 1
            seen.append(data[i].item.get_serial())

    def set_canvas_table_configuration_containers(self, row_count, data):
        self.fig.set_canvas(self.canvas)
        self._ax = self.canvas.figure.add_subplot(projection="3d")

        self.table.setRowCount(row_count)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(self.column_names)
        self.set_table_data_container(data)

    def serial_hash(self, item_serial: str) -> str:
        sha = hashlib.sha256()
        sha.update(item_serial.encode())
        return sha.hexdigest()[:6]

    def load_list(self, packing_list="Book1.xlsx"):
        self.data = Ingest.ingest("../", packing_list)
        self.items = init(self.data)
        self.items = Sort.item_sort(self.items)
        print(self.items[0])
        print(self.items[len(self.items) - 1])
        logi = [0, 0, 0]
        self.containerTemplate = Container(0, 0, 0, logi, 2000, 2000, 2500)
        self.shipment = palletize.palletize(self.items, self.containerTemplate)
        print(self.shipment)

    # Plot methods

    def plot_dyn_cube(self, shipment: list, index: int):
        if hasattr(self, "_ax"):
            self._ax.cla()
        self.set_canvas_table_configuration_containers(len(self.shipment), self.shipment[index])

        for container in shipment[index]:
            print(container)
            if container.item is None:
                continue
            verts = np.array([
                [container.x, container.y, container.z],  # 0
                [container.x + container.item.get_length(), container.y, container.z],  # 1
                [container.x, container.y + container.item.get_width(), container.z],  # 2
                [container.x + container.item.get_length(), container.y + container.item.get_width(), container.z],  # 3
                [container.x, container.y, container.z + container.item.get_height()],  # 4
                [container.x + container.item.get_length(), container.y, container.z + container.item.get_height()],
                # 5
                [container.x, container.y + container.item.get_width(), container.z + container.item.get_height()],  # 6
                [container.x + container.item.get_length(), container.y + container.item.get_width(),
                 container.z + container.item.get_height()],  # 7
            ])
            faces = [
                [verts[0], verts[1], verts[3], verts[2]],  # Top
                [verts[4], verts[5], verts[7], verts[6]],  # Bottom
                [verts[2], verts[3], verts[7], verts[6]],  # North
                [verts[0], verts[1], verts[5], verts[4]],  # South
                [verts[0], verts[2], verts[6], verts[4]],  # East
                [verts[1], verts[3], verts[7], verts[5]]  # West
            ]

            self._ax.scatter3D(verts[:, 0], verts[:, 1], verts[:, 2], alpha=0)
            color = self.serial_hash(container.item.get_serial())
            self._ax.add_collection3d(
                Poly3DCollection(faces, facecolors=f'#{color}', linewidths=1, edgecolors='b', alpha=.5))

        verts = np.array([
            [self.containerTemplate.x, self.containerTemplate.y, self.containerTemplate.z],  # 0
            [self.containerTemplate.x + self.containerTemplate.length, self.containerTemplate.y,
             self.containerTemplate.z],  # 1
            [self.containerTemplate.x, self.containerTemplate.y + self.containerTemplate.width,
             self.containerTemplate.z],  # 2
            [self.containerTemplate.x + self.containerTemplate.length,
             self.containerTemplate.y + self.containerTemplate.width, self.containerTemplate.z],  # 3
            [self.containerTemplate.x, self.containerTemplate.y,
             self.containerTemplate.z + self.containerTemplate.height],  # 4
            [self.containerTemplate.x + self.containerTemplate.length, self.containerTemplate.y,
             self.containerTemplate.z + self.containerTemplate.height],  # 5
            [self.containerTemplate.x, self.containerTemplate.y + self.containerTemplate.width,
             self.containerTemplate.z + self.containerTemplate.height],  # 6
            [self.containerTemplate.x + self.containerTemplate.length,
             self.containerTemplate.y + self.containerTemplate.width,
             self.containerTemplate.z + self.containerTemplate.height],  # 7
        ])
        self._ax.scatter3D(verts[:, 0], verts[:, 1], verts[:, 2])

        self._ax.set_xlabel('X')
        self._ax.set_ylabel('Y')
        self._ax.set_zlabel('Z')
        self.canvas.draw()

    # Slots
    @Slot()
    def combo_option(self, text):
        for i in range(len(self.shipment)):
            if text == f"Crate {1 + i}":
                self.plot_dyn_cube(self.shipment, i)

    @Slot()
    def rotate_azim(self, value):
        self._ax.view_init(self._ax.elev, value)
        self.fig.set_canvas(self.canvas)
        self.canvas.draw()

    @Slot()
    def rotate_elev(self, value):
        self._ax.view_init(value, self._ax.azim)
        self.fig.set_canvas(self.canvas)
        self.canvas.draw()


def start():
    app = QApplication(sys.argv)
    w = ApplicationWindow()
    w.setFixedSize(1280, 720)
    w.show()
    app.exec_()


if __name__ == "__main__":
    start()
