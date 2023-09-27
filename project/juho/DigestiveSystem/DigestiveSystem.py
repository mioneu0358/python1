import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtGui import QPixmap

form_class = uic.loadUiType("DigestiveSystem_UI.ui")[0]

BLUE = (0,0,255)
BLACK = (0,0,0)
GREEN = (106,171,115)




class WindowClass(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Digetive System2")
        self.loadImageFromFile()

        # 탄,단,지 textLabel
        self.labelNutrients = QLabel(self)
        self.labelNutrients.setAlignment(QtCore.Qt.AlignCenter) # 가로 정렬

        self.idx = 0

        # 버튼 별 기능 할당
        self.btn_carbs.clicked.connect(self.func_carbs)
        self.btn_protein.clicked.connect(self.func_protein)
        self.btn_fat.clicked.connect(self.func_fat)


    # 메인 이미지 불러오기
    def loadImageFromFile(self):
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load("digestive_organ2.png")
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(640)
        self.mainLabel.setPixmap(self.qPixmapVar)



    # 탄수화물 버튼 기능
    def func_carbs(self):
        self.labelNutrients.setGeometry(100,200,200,60)
        self.labelNutrients.setText("탄수화물")
        self.labelNutrients.setFont(QtGui.QFont('초롱바탕', 28))
    # 단백질 버튼 기능
    def func_protein(self):
        self.labelNutrients.setGeometry(100,200,200,60)
        self.labelNutrients.setText("단백질")
        self.labelNutrients.setFont(QtGui.QFont('초롱바탕', 28))
    # 지방 버튼 기능
    def func_fat(self):
        self.labelNutrients.setGeometry(100,200,200,60)
        self.labelNutrients.setText("지 방")
        self.labelNutrients.setFont(QtGui.QFont('초롱바탕', 28))




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()