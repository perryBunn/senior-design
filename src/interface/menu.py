import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui


class Menu(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.pack_button = QtWidgets.QPushButton("Pack!")
        self.config_button = QtWidgets.QPushButton("Config")
        self.list_button = QtWidgets.QPushButton("Packing list")

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setGeometry(QtCore.QRect(0, 0, 3, 3))
        self.layout.addWidget(self.pack_button, 0, 1)
        self.layout.addWidget(self.list_button, 0, 0)
        self.layout.addWidget(self.config_button, 1, 0, 1, 2)

        self.pack_button.clicked.connect(self.pack)
        self.config_button.clicked.connect(self.config)
        self.list_button.clicked.connect(self.list)

    @QtCore.Slot()
    def pack(self):
        print("pack")
        pass

    @QtCore.Slot()
    def list(self):
        print("list")
        pass

    @QtCore.Slot()
    def config(self):
        print("config")
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Menu()
    widget.resize(800, 400)
    widget.setWindowTitle("Menu")
    widget.show()

    sys.exit(app.exec_())