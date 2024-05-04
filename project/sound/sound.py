import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtGui import QPixmap

form_class = uic.loadUiType("Ear System.ui")[0]


class WindowClass(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Ear System")
        self.loadImageFromFile()

    def loadImageFromFile(self):
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load("ear.jpg")
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(720)
        self.EarLabel.setPixmap(self.qPixmapVar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()