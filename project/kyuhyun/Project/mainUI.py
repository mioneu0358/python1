from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon



class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,1200,860,)
        self.setWindowTitle("GPT_SongMaker")
        frame1 = self.makeFrame(self, 10,10,1180, 840,bd=2)     # 가장 바깥 프레임
        btn_new_poject = self.makeButton(frame1, 10,10,100,70,"프로젝트\n새로만들기",self.selectFolder)

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

    def makeFrame(self,where, x, y, width, height, bd=0):
        frame = QFrame(where)
        frame.setGeometry(x, y, width, height)
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(bd)
        return frame

    def makeButton(self, where,x,y,width,height,text, function):
        btn = QPushButton(where,text=text)
        btn.setGeometry(x,y,width,height)
        btn.clicked.connect(function)
        return btn

    def selectFolder(self):
        print(QFileDialog.selectedUrls())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec_()



# 프로젝트 새로 만들기

# import os
# import time
#
# # 현재 경로 기준으로 Project생성하기
# # curr_path = os.getcwd()     # 현재 경로
# curr_path = os.getcwd()+"/GPT_SongMaker"
# project_list = os.listdir(curr_path)
# project_list.sort()
#
# if project_list:
#     last_num = int(project_list[-1][-1])+1 if project_list[-1][-1].isdigit() else 1
#     os.mkdir(f"{curr_path}/Project{last_num}")
# else:
#     os.mkdir(f"{curr_path}/Project")