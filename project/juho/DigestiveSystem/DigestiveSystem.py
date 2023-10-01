import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtGui import QPixmap

form_class = uic.loadUiType("DigestiveSystem_UI.ui")[0]


class WindowClass(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Digetive System")
        self.loadImageFromFile()

        # 탄,단,지 textLabel
        self.labelNutrients = QLabel(self)
        self.labelNutrients.setAlignment(QtCore.Qt.AlignCenter) # 가로 정렬


        # 영양소 변화과정 {영양소: [(효소,변화된 영양소),(),()], }
        self.nutrient = ''
        self.nutrients = {
            '탄수화물': [('아밀레이스', '엿당'), ('아밀레이스', '엿당'), ('말테이스', '포도당')],
            '단백질': [('펩신', '폴리팹티드'), ('트립신', '디펩티드'), ('펩티데이스', '아미노산')],
            '지방': [("쓸개즙", '지방 유화'), ('라이페이스', '지방산과 모노글리셀리드')]
        }
        self.carbs_geometry = [(250,180,200,60),(150,650,200,60),(210,800,200,60)]
        self.protein_geometry = [(380,600,200,60),(150,650,200,60),(210,800,200,60)]
        self.fat_geometry = [(140,630,200,60),(180,680,280,60)]

        # 버튼 별 기능 할당
        self.btn_carbs.clicked.connect(self.func_carbs)
        self.btn_protein.clicked.connect(self.func_protein)
        self.btn_fat.clicked.connect(self.func_fat)

        self.btn_prev.clicked.connect(self.func_prev)
        self.btn_next.clicked.connect(self.func_next)


    # 메인 이미지 불러오기
    def loadImageFromFile(self):
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load("digestive_organ.png")
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(640)
        self.mainLabel.setPixmap(self.qPixmapVar)



    # 탄수화물 버튼 기능
    def func_carbs(self):
        # 영양소 위치
        self.idx = -1
        self.labelNutrients.setGeometry(50,200,200,60)
        self.labelNutrients.setStyleSheet("background:#6897FC;" 
                                          #  "backgound: transparent;" - 배경 투명하게
                                          "border-style: solid;"
                                          "border-width: 1px;"
                                          "border-color: black;"
                                          "border-radius: 10px;"
                                          )
        self.labelNutrients.setText("탄수화물")
        self.nutrient = '탄수화물'
        self.labelNutrients.setFont(QtGui.QFont('초롱바탕', 28))

    # 단백질 버튼 기능
    def func_protein(self):
        # 영양소 위치
        self.idx = -1
        self.labelNutrients.setGeometry(50,200,200,60)
        self.labelNutrients.setText("단백질")
        self.nutrient = '단백질'
        self.labelNutrients.setFont(QtGui.QFont('초롱바탕', 28))

    # 지방 버튼 기능
    def func_fat(self):
        # 영양소 위치
        self.idx = -1
        self.labelNutrients.setGeometry(50,200,200,60)
        self.labelNutrients.setText("지 방")
        self.nutrient = '지방'
        self.labelNutrients.setFont(QtGui.QFont('초롱바탕', 28))


    def func_prev(self):
        if self.nutrient:
            if self.idx > 0:
                self.idx -= 1
            self.labelNutrients.setText(self.nutrients[self.nutrient][self.idx][1])
            if len(self.nutrients[self.nutrient][self.idx][1]) > 6:
                self.labelNutrients.setFont(QtGui.QFont('초롱바탕', 17,))
            if self.nutrient == '탄수화물':
                x,y,w,h = self.carbs_geometry[self.idx]
            elif self.nutrient == '단백질':
                x,y,w,h = self.protein_geometry[self.idx]
            else:
                x,y,w,h = self.fat_geometry[self.idx]
            self.labelNutrients.setGeometry(x,y,w,h)

            # self.labelNutrients.setGeometry(self.nut_geometry[self.idx])


    def func_next(self):
        if self.nutrient:
            if self.idx < len(self.nutrients[self.nutrient])-1:
                self.idx += 1
            if self.nutrient == '탄수화물':
                x, y, w, h = self.carbs_geometry[self.idx]
            elif self.nutrient == '단백질':
                x, y, w, h = self.protein_geometry[self.idx]
            else:
                x, y, w, h = self.fat_geometry[self.idx]

            if len(self.nutrients[self.nutrient][self.idx][1]) > 6:
                self.labelNutrients.setFont(QtGui.QFont('초롱바탕', 18))
            self.labelNutrients.setText(self.nutrients[self.nutrient][self.idx][1])
            self.labelNutrients.setGeometry(x, y, w, h)
            # self.labelNutrients.setGeometry(self.nut_geometry[self.idx])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()