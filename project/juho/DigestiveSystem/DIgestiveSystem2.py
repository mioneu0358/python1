import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtGui import QPixmap,QFont

form_class = uic.loadUiType("DigestiveSystem_UI2.ui")[0]


class WindowClass(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Digetive System")
        self.loadImageFromFile()
        self.Labelinit()
    def Labelinit(self):
        # 탄,단,지 textLabel
        self.labelNutrients = QLabel(self)
        self.labelNutrients.setAlignment(QtCore.Qt.AlignCenter) # 가로 정렬
        self.labelNutrients.setGeometry(50, 200, 0,0)
        self.labelNutrients.setStyleSheet("background:#99e5e5;"
                                          #  "backgound: transparent;" - 배경 투명하게
                                          "border-style: solid;"
                                          "border-width: 1px;"
                                          "border-color: black;"
                                          "border-radius: 10px;"
                                          )
        # 소화 효소 textLabel
        self.labelOrgan = QLabel(self)
        self.labelOrgan.setAlignment(QtCore.Qt.AlignCenter)
        self.labelOrgan.setGeometry(730, 153, 200, 70)
        self.labelOrgan.setStyleSheet("background: white;"
                                       "border-style: solid;"
                                       "border-width: 3px;"
                                       "border-color: black;"
                                       )

        self.labelOrgan.setFont(QFont('초롱바탕', 25, QFont.Bold))
        # 소화 효소 textLabel
        self.labelEnzyme = QLabel(self)
        self.labelEnzyme.setAlignment(QtCore.Qt.AlignCenter)
        self.labelEnzyme.setGeometry(730,303,200,70)
        self.labelEnzyme.setStyleSheet("background: white;"
                                          "border-style: solid;"
                                          "border-width: 3px;"
                                          "border-color: black;"
                                          )
        self.labelEnzyme.setFont(QFont('초롱바탕', 25,QFont.Bold))

        # 영양소 변화과정 {영양소: [(효소,변화된 영양소),(),()], }
        self.nutrient = ''
        self.nutrients = {
            '탄수화물': [('','','탄수화물'),('아밀레이스','구강','엿당'), ('아밀레이스','소장', '엿당'), ('말테이스','소장', '포도당')],
            '단백질': [('','','단백질'),('펩신','위','폴리팹티드'), ('트립신','소장', '디펩티드'), ('펩티데이스','소장', '아미노산')],
            '지방': [('','','지방'),("쓸개즙",'소장','지방 유화'), ('라이페이스','소장', '지방산과 모노글리셀리드')]
        }
        self.nutrients_geometry = {
            "탄수화물":[(50, 200, 200, 60),(250,180,200,60),(150,650,200,60),(210,800,200,60)] ,
            "단백질":  [(50, 200, 200, 60),(380,600,200,60),(150,650,200,60),(210,800,200,60)],
            "지방": [(50, 200, 200, 60),(140,630,200,60),(180,680,280,60)]
        }
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
        self.idx = 0
        self.labelNutrients.setGeometry(50, 200, 200, 60)
        self.labelNutrients.setText("탄수화물")
        self.nutrient = '탄수화물'
        self.labelNutrients.setFont(QtGui.QFont('초롱바탕', 28))

    # 단백질 버튼 기능
    def func_protein(self):
        # 영양소 위치
        self.idx = 0
        self.labelNutrients.setGeometry(50,200,200,60)
        self.labelNutrients.setText("단백질")
        self.nutrient = '단백질'
        self.labelNutrients.setFont(QtGui.QFont('초롱바탕', 28))

    # 지방 버튼 기능
    def func_fat(self):
        # 영양소 위치
        self.idx = 0
        self.labelNutrients.setGeometry(50,200,200,60)
        self.labelNutrients.setText("지 방")
        self.nutrient = '지방'
        self.labelNutrients.setFont(QtGui.QFont('초롱바탕', 28))


    def func_prev(self):
        if self.nutrient:
            if self.idx > 0:
                self.idx -= 1
            # Enzyme_name:소화효소 이름, Nutrient_name: 영양소 이름
            Enzyme_name,Organ_name, Nutrient_name = self.nutrients[self.nutrient][self.idx]
            self.labelNutrients.setText(Nutrient_name)
            self.labelOrgan.setText(Organ_name)
            self.labelEnzyme.setText(Enzyme_name)
            # 지방산과 모노글리셀리드 같이 긴 글자는 폰트를 줄임
            if len(self.nutrients[self.nutrient][self.idx][1]) > 6:
                self.labelNutrients.setFont(QtGui.QFont('초롱바탕', 17,))
            x, y, w, h = self.nutrients_geometry[self.nutrient][self.idx]
            self.labelNutrients.setGeometry(x,y,w,h)


    def func_next(self):
        if self.nutrient:
            if self.idx < len(self.nutrients[self.nutrient])-1:
                self.idx += 1

            x, y, w, h = self.nutrients_geometry[self.nutrient][self.idx]
            self.labelNutrients.setGeometry(x, y, w, h)
            if len(self.nutrients[self.nutrient][self.idx][1]) > 6:
                self.labelNutrients.setFont(QtGui.QFont('초롱바탕', 18))
            Enzyme_name,Organ_name,Nutrient_name = self.nutrients[self.nutrient][self.idx]
            self.labelNutrients.setText(Nutrient_name)
            self.labelOrgan.setText(Organ_name)
            self.labelEnzyme.setText(Enzyme_name)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()