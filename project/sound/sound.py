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
        self.idx = -1
        self.organ = ['귓바퀴', '외이도', '고막', '귓속뼈', '달팽이관', '청각신경','대뇌']
        self.explain = ['소리를 외이도로\n모아주는 역할', '소리가 이동하는 통로\n 고막으로 전달', ' 소리를 받아 진동',
                        '진동을 증폭시켜\n달팽이관에 전달', ' 진동을 자극으로 변환하여\n청각신경으로 전달', ' 청각세포에서 받아들인\n자극을 뇌로 전달','소리를 이해']
        self.soundpos = [[50,350,80,50],[200,330,80,50],[330,315,50,30],[380,315,50,30],[430,300,50,30],[450,270,50,30]]
        self.NextBtn_2.clicked.connect(self.NEXT)
        self.PreviousBtn_2.clicked.connect(self.PREVIOUS)
        self.SoundLabel = QLabel(self.SubFrame)
    def LoadSoundImg(self):
        x,y,w,h = self.soundpos[self.idx]
        self.SoundLabel.setGeometry(x,y,w,h)
        SoundImg = QPixmap()
        SoundImg.load("sound_1.png")
        self.SoundLabel.setPixmap(SoundImg.scaledToWidth(w))


    def LoadMainImg(self):
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load("ear_2.png")
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(720)
        self.EarLabel_2.setPixmap(self.qPixmapVar)


    def NEXT(self):
        if self.idx >= 5:
            return
        print(self.idx)
        self.idx += 1
        self.LoadSoundImg()
        self.OrganLabel_3.setText(f" 기 관: {self.organ[self.idx]}")
        self.ExplainLabel_2.setText(self.explain[self.idx])


    def PREVIOUS(self):
        if self.idx <= 0:
            return
        self.idx -= 1
        self.LoadSoundImg()
        self.OrganLabel_3.setText(f" 기 관: {self.organ[self.idx]}")
        self.ExplainLabel_2.setText(self.explain[self.idx])



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()