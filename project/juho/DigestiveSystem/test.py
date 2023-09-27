import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5 import uic

ui = uic.loadUiType("DigestiveSystem_UI.ui")

# 탄수화물: carbohydrate or carbs
# 영양소 : Nutrients
class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("DigestiveSystem2")
        self.move(400,50)
        self.resize(950,970)
        # self.btn_carbs = self.make_psbtn('탄수화물')

        # 메인 이미지 digestive_organ.png
        self.main_label = QLabel(self)
        self.main_label.setGeometry(20,30,600,900)
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load("digestive_organ.png")
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
        self.main_label.setPixmap(self.qPixmapVar)




    def make_psbtn(self,text):
        new_btn = QPushButton(text = text,parent=self)
        new_btn.setGeometry(50,60,200,100)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()