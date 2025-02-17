from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QFont
from PyQt5 import QtCore



class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(10,10,1200,860)
        # self.setFixedSize(1200,860)
        self.setWindowTitle("GPT_SongMaker")
        frame1 = self.makeFrame(self, 10,30,1180, 820,bd=2)     # 가장 바깥 프레임
        frame2 = self.makeFrame(frame1,0,100,550,810,bd=2)
        btn_new_poject = self.makeButton(frame1, 0,0,100,40,"새 프로젝트",self.selectFolder)   # 새 프로젝트 만들기
        frame_music_instrument = self.makeFrame(frame2,0,0, 550,400,bd=2)      # 악기 프레임
        label_music_instrument = self.makeLabel(frame_music_instrument, 0,0,550,50,"악기 선택",bd=2)
        # TODO: list_music_instrument 만들기: 악기이름을 가지고 있는 체크 박스들이 들어있는 리스트, 이 리스트 scrollbar에 넣기
        list_music_instrument = ["기타", "베이스",'피아노','드럼','보컬']

        self.scrollbar_music_instrument = self.makeScrollbar(frame_music_instrument,2,50,546,250)
        font_music_instrument = QFont()
        font_music_instrument.setPointSize(20)
        scroll_content = QWidget()
        vbox = QVBoxLayout()
        for i in range(len(list_music_instrument)):
            list_music_instrument[i] = (self.makeCheckBox(None,0,0,250,100,list_music_instrument[i],font=font_music_instrument))
            vbox.addWidget(list_music_instrument[i])
        scroll_content.setLayout(vbox)
        self.scrollbar_music_instrument.setWidget(scroll_content)
        self.line_music_instrument = QLineEdit(frame_music_instrument)
        self.line_music_instrument.setGeometry(10,310,300,80)
        font_line = QFont()
        font_line.setPointSize(12)
        self.line_music_instrument.setPlaceholderText("추가할 악기를 입력하시오.")
        self.line_music_instrument.setFont(font_line)
        self.btn_addMusicInstrument = self.makeButton(frame_music_instrument,330,310,120,80,"악기\n추가하기",self.addMusicInstrument)

        # BPM TEXT, LINEEDIT
        txt_bpm = QLabel(frame2)
        font = QFont()
        font.setPointSize(20)
        txt_bpm.setText("BPM: ")
        txt_bpm.setGeometry(0,410,100,80)
        txt_bpm.setFrameStyle(2)
        txt_bpm.setFont(font)
        self.line_bpm = QLineEdit(frame2)
        self.line_bpm.setGeometry(100,410,120,80)
        self.line_bpm.setFont(font)
        self.line_bpm.setPlaceholderText('00')
        self.line_bpm.setAlignment(QtCore.Qt.AlignRight)




        txt_genre = QLabel(frame2)
        font = QFont()
        font.setPointSize(20)
        txt_genre.setText("장르: ")
        txt_genre.setGeometry(235,410,100,80)
        txt_genre.setFrameStyle(2)
        txt_genre.setFont(font)
        self.combo_genre = QComboBox(frame2)
        self.combo_genre.setGeometry(340,410,200,80)






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
        return scroll

    def makeCheckBox(self,parent, x, y, width, hegith, text, font = None):
        checkbox = QCheckBox(parent,text=text)
        checkbox.setGeometry(x,y,width,hegith)
        if font:
            checkbox.setFont(font)
        return checkbox



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

    def addMusicInstrument(self):
        curr_text = self.line_music_instrument.text()
        print([curr_text])
        if curr_text.startswith('추가할'):
            return
        # TODO: curr_text에 들어있는 악기를 music_instrument에 추가하기



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec_()



# 프로젝트 새로 만들기
