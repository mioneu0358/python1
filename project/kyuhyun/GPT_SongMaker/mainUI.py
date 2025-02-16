from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(10,10,1200,860)
        # self.setFixedSize(1200,860)
        self.setWindowTitle("GPT_SongMaker")
        frame1 = self.makeFrame(self, 10,30,1180, 820,bd=2)     # 가장 바깥 프레임
        btn_new_poject = self.makeButton(frame1, 0,0,100,40,"새 프로젝트",self.selectFolder)   # 새 프로젝트 만들기
        frame_music_instrument = self.makeFrame(frame1,0,100, 550,400,bd=2)      # 악기 프레임
        label_music_instrument = self.makeLabel(frame_music_instrument, 0,0,550,50,"악기 선택",bd=2)
        # TODO: music_instrument_list 만들기: 악기이름을 가지고 있는 체크 박스들이 들어있는 리스트, 이 리스트 scrollbar에 넣기
        scrollbar = self.makeScrollbar(frame_music_instrument,0,50,550,300)






        # 메뉴 바
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)



        self.setWindowTitle('Menubar')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def makeFrame(self,parent, x, y, width, height, bd=0):
        frame = QFrame(parent)
        frame.setGeometry(x, y, width, height)
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(bd)
        return frame

    def makeButton(self, parent,x,y,width,height,text, function):
        btn = QPushButton(parent,text=text)
        btn.setGeometry(x,y,width,height)
        btn.clicked.connect(function)
        return btn

    def makeLabel(self,parent, x,y,width, height, text,bd=0):
        label = QLabel(parent,text=text)
        label.setGeometry(x,y,width,height)
        label.setFrameShape(3)
        label.setAlignment(QtCore.Qt.AlignCenter)

    def makeScrollbar(self,parent,x,y,width,height,*items):
        scroll = QScrollArea(parent)
        scroll.setGeometry(x,y,width,height)
        for item in items:
            scroll.setWidget(item)
        scroll.setWidgetResizable(True)

    def selectFolder(self):
        selected_folder = QFileDialog.getExistingDirectory(self,'파일선택','')
        import os
        import time

        # 현재 경로 기준으로 Project생성하기
        # selcted_path = os.getcwd()     # 현재 경로
        selcted_path= selected_folder
        print(f"selected_path: {selcted_path}")
        project_list=os.listdir(selcted_path)

        if "GPT_SongMaker" not in project_list:
            os.mkdir(f"{selcted_path}/GPT_SongMaker")
        else:
            num = 1
            while f"GPT_SongMaker{num}" in project_list:
                num += 1
            os.mkdir(f"{selcted_path}/GPT_SongMaker{num}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec_()



# 프로젝트 새로 만들기

