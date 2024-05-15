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
        self.LoadMainImg()
        # 소리의 이동경로에 대한 변수들
        self.SoundIdx = -1
        self.SoundOrgan = ['귓바퀴', '외이도', '고막', '귓속뼈', '달팽이관', '청각신경','대뇌']
        self.SoundExplain = ['소리를 외이도로\n모아주는 역할', '소리가 이동하는 통로\n 고막으로 전달', ' 소리를 받아 진동',
                        '진동을 증폭시켜\n달팽이관에 전달', ' 진동을 자극으로 변환하여\n청각신경으로 전달', ' 청각세포에서 받아들인\n자극을 뇌로 전달','소리를 이해']
        self.SoundPos = [[50,350,80,50],[200,330,80,50],[330,315,50,30],[380,315,50,30],[430,300,50,30],[450,270,50,30],[540,180,50,80]]
        self.NextBtn_1.clicked.connect(self.SOUNDNEXT)
        self.PreviousBtn_1.clicked.connect(self.SOUNDPREVIOUS)
        self.SoundLabel = QLabel(self.SubFrame_1)

        # 평형감각에 대한 변수들
        self.BalanceIdx = -1
        self.BalanceOrgan = ['전정기관', '반고리관','귀 인두관']
        self.BalanceExplain = ['몸의 움직임,기울임 감지', '몸의 회전을 감지', '중이 내부와 외부의\n압력을 같게 유지']
        self.NextBtn_2.clicked.connect(self.BALANCENEXT)
        self.PreviousBtn_2.clicked.connect(self.BALANCEPREVIOUS)



    def LoadSoundImg(self):
        x,y,w,h = self.SoundPos[self.SoundIdx]
        self.SoundLabel.setGeometry(x,y,w,h)
        SoundImg = QPixmap()
        SoundImg.load("sound_1.png")
        self.SoundLabel.setPixmap(SoundImg.scaledToWidth(w))


    def LoadMainImg(self):
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load("ear1.png")
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(720)
        self.EarLabel_1.setPixmap(self.qPixmapVar)
        self.qPixmapVar.load("ear3.png")
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(700)
        self.EarLabel_2.setPixmap(self.qPixmapVar)


    def SOUNDNEXT(self):
        if self.SoundIdx >= 6:
            return
        print(self.SoundIdx)
        self.SoundIdx += 1
        self.LoadSoundImg()
        self.OrganLabel_1.setText(f" 기 관: {self.SoundOrgan[self.SoundIdx]}")
        self.ExplainLabel_1.setText(self.SoundExplain[self.SoundIdx])


    def SOUNDPREVIOUS(self):
        if self.SoundIdx <= 0:
            return
        print(self.SoundIdx)
        self.SoundIdx -= 1
        self.LoadSoundImg()
        self.OrganLabel_1.setText(f" 기 관: {self.SoundOrgan[self.SoundIdx]}")
        self.ExplainLabel_1.setText(self.SoundExplain[self.SoundIdx])

    def BALANCENEXT(self):
        if self.BalanceIdx >= 2:
            return
        print(self.BalanceIdx)
        self.BalanceIdx += 1
        self.OrganLabel_2.setText(f" 기 관: {self.BalanceOrgan[self.BalanceIdx]}")
        self.ExplainLabel_2.setText(self.BalanceExplain[self.BalanceIdx])

    def BALANCEPREVIOUS(self):
        if self.BalanceIdx <= 0:
            return
        self.BalanceIdx -= 1
        self.OrganLabel_2.setText(f" 기 관: {self.BalanceOrgan[self.BalanceIdx]}")
        self.ExplainLabel_2.setText(self.BalanceExplain[self.BalanceIdx])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()