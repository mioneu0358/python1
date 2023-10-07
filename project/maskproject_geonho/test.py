from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtWidgets import *

form_class = uic.loadUiType("test.ui")[0]


class mainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.show_img_btn.clicked.connect(self.func)

    def func(self):
        self.qpmap = QPixmap()
        self.qpmap.load(f"mask.png")
        self.qpmap = self.qpmap.scaledToWidth(400)
        print(1)
        self.mask_label.setPixmap(self.qpmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec_()