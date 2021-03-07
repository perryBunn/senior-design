import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.tableWidget = QtWidgets.QTableWidget(10, 2)
        self.button = QtWidgets.QPushButton("Click me!")
        self.update_table_button = QtWidgets.QPushButton("Update Table")
        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)
        self.window3d = QtGui.QWindow()
        self.window3d.setWidth(200)
        self.window3d.setHeight(400)
        self.window3d.setVisible(True)
        self.container3d = QtWidgets.QWidget.createWindowContainer(self.window3d, self)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setGeometry(QtCore.QRect(0, 0, 3, 3))
        self.layout.addWidget(self.text, 1, 0)
        self.layout.addWidget(self.button, 1, 1)
        self.layout.addWidget(self.container3d, 2, 0)
        self.layout.addWidget(self.tableWidget, 2, 1)
        self.layout.addWidget(self.update_table_button, 3, 1)

        self.button.clicked.connect(self.magic)
        self.update_table_button.clicked.connect(self.update_table)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

    @QtCore.Slot()
    def update_table(self):
        for row in range(0, 10):
            for column in range(0, 2):
                temp = QtWidgets.QTableWidgetItem(f"test {row}")
                self.tableWidget.setItem(row, column, temp)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 400)
    widget.show()

    sys.exit(app.exec_())