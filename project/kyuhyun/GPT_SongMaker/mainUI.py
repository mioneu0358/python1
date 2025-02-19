from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFrame, QLabel, QScrollArea, QCheckBox, QVBoxLayout, \
    QWidget, QLineEdit, QComboBox, QAction, QFileDialog, qApp,QMessageBox
import sys
import os


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(10, 10, 1200, 860)
        self.setWindowTitle("GPT_SongMaker")

        frame1 = self.makeFrame(self, 10, 30, 1180, 820, bd=2)     # 가장 바깥 프레임
        frame2 = self.makeFrame(frame1, 20, 100, 550, 810, bd=2)   # 악기, BPM, 장르, 가사 프레임
        frame3 = self.makeFrame(frame1, 610,100, 550, 810, bd=2)   # 질의문창,재생창,
        btn_new_project = self.makeButton(frame1, 0, 0, 100, 40, "새 프로젝트", self.selectFolder)

        # 악기 선택 프레임
        frame_music_instrument = self.makeFrame(frame2, 0, 0, 550, 400, bd=2)
        label_music_instrument = self.makeLabel(frame_music_instrument, 0, 0, 550, 50, "악기 선택", bd=2)

        # 스크롤바 및 체크박스 리스트
        self.scrollbar_music_instrument = self.makeScrollbar(frame_music_instrument, 2, 50, 546, 250)
        self.scroll_content = QWidget()
        self.vbox_music_instrument = QVBoxLayout()
        self.scroll_content.setLayout(self.vbox_music_instrument)
        self.scrollbar_music_instrument.setWidget(self.scroll_content)

        # 기본 악기 추가
        initial_instruments = ["기타", "베이스", "피아노", "드럼", "보컬"]
        font_music_instrument = QFont()
        font_music_instrument.setPointSize(20)

        for instrument in initial_instruments:
            checkbox = self.makeCheckBox(None, 0, 0, 250, 100, instrument, font=font_music_instrument)
            self.vbox_music_instrument.addWidget(checkbox)

        # 악기 추가 입력 및 버튼
        self.line_music_instrument = QLineEdit(frame_music_instrument)
        self.line_music_instrument.setGeometry(10, 310, 300, 80)
        font_line = QFont()
        font_line.setPointSize(12)
        self.line_music_instrument.setPlaceholderText("추가할 악기를 입력하시오.")
        self.line_music_instrument.setFont(font_line)

        self.btn_addMusicInstrument = self.makeButton(frame_music_instrument, 330, 310, 120, 80, "악기\n추가하기",
                                                      self.addMusicInstrument)

        # BPM 텍스트 및 입력
        txt_bpm = self.makeLabel(frame2, 10, 410, 100, 80, "BPM: ", bd=2)
        font = QFont()
        font.setPointSize(20)
        txt_bpm.setFont(font)

        self.line_bpm = QLineEdit(frame2)
        self.line_bpm.setGeometry(110, 410, 120, 80)
        self.line_bpm.setFont(font)
        self.line_bpm.setPlaceholderText('00')
        self.line_bpm.setAlignment(QtCore.Qt.AlignRight)

        # 장르 선택
        label_genre_menu = self.makeLabel(frame2, 235, 410, 100, 80, "장르: ", bd=2)
        label_genre_menu.setFont(font)
        self.genre = ['KPOP', "클래식", "POP","HIPHOP","ROCK", "EDM", "JAZZ", "FUNK", "R&B", ]
        self.combo_genre = QComboBox(frame2)
        self.combo_genre.setGeometry(335, 410, 200, 80)
        self.combo_genre.addItems(self.genre)
        font_genre = QFont()
        font_genre.setPointSize(20)
        self.combo_genre.setFont(font_genre)



        # 가사 선택
        label_lyrics_menu = self.makeLabel(frame2,10,500,100,40,text="선택된 가사",bd=2)
        self.label_selected_lyrics = self.makeLabel(frame2,108,500,202,40,text="선택된 가사가 없습니다.",bd=2)
        self.btn_getlyrics = self.makeButton(frame2, 335, 500, 200, 40, text='가사 선택하기', function=self.get_lyrics)
        self.label_lyrics = self.makeLabel(frame2,10,550,530,160,bd=2)
        self.scrollbar_lylics = self.makeScrollbar(self.label_lyrics,0,0,530,160)
        self.lyrics_content = QWidget()
        self.vbox_lyrics = QVBoxLayout()
        self.lyrics_content.setLayout(self.vbox_lyrics)
        self.scrollbar_lylics.setWidget(self.lyrics_content)
        self.label_selected_lyrics.setAlignment(QtCore.Qt.AlignCenter)



        # 메뉴 바 설정
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)


        # Frame3 ---------------------------------------------------------------------------------------------------
        label_query = self.makeLabel(frame3, 0, 0, 550, 50, "질의문 작성", bd=2)
        self.text_query = QLineEdit(frame3)

        self.text_query.setGeometry(2, 50, 440, 250)
        font_query = QFont()
        font_query.setPointSize(20)
        self.text_query.setPlaceholderText("상세한 설명을 적어주세요.")
        self.text_query.setFont(font_query)

        self.btn_run = self.makeButton(frame3, 440, 50, 108, 250, "GPT에\n요청\n하기",
                                                      self.request_GPT)
        font_run = QFont()
        font_run.setPointSize(18)
        self.btn_run.setFont(font_run)

    def makeFrame(self, parent, x, y, width, height, bd=0):
        frame = QFrame(parent)
        frame.setGeometry(x, y, width, height)
        frame.setFrameShape(QFrame.Box)
        frame.setLineWidth(bd)
        return frame

    def makeButton(self, parent, x, y, width, height, text, function, font = None):
        btn = QPushButton(parent, text=text)
        btn.setGeometry(x, y, width, height)
        btn.clicked.connect(function)
        if font:
            btn.setFont(font)
        return btn

    def makeLabel(self, parent, x, y, width, height, text='', bd=0):
        label = QLabel(parent, text=text)
        label.setGeometry(x, y, width, height)
        label.setFrameShape(3)
        label.setAlignment(QtCore.Qt.AlignCenter)
        return label  # 수정된 부분: QLabel 반환

    def makeScrollbar(self, parent, x, y, width, height):
        scroll = QScrollArea(parent)
        scroll.setGeometry(x, y, width, height)
        scroll.setWidgetResizable(True)

        return scroll

    def makeCheckBox(self, parent, x, y, width, height, text, font=None):
        checkbox = QCheckBox(parent, text=text)
        checkbox.setGeometry(x, y, width, height)
        if font:
            checkbox.setFont(font)
        return checkbox

    def selectFolder(self):
        selected_folder = QFileDialog.getExistingDirectory(self, '파일선택', '')
        if not selected_folder:
            return  # 사용자가 폴더를 선택하지 않은 경우

        project_list = os.listdir(selected_folder)

        # GPT_SongMaker 폴더 생성
        base_folder_name = "GPT_SongMaker"
        new_folder_name = base_folder_name
        num = 1
        while new_folder_name in project_list:
            new_folder_name = f"{base_folder_name}{num}"
            num += 1

        os.mkdir(os.path.join(selected_folder, new_folder_name))

    def get_lyrics(self):
        # 파일 선택 대화상자 (txt 파일만 선택 가능하도록 필터 추가)
        lyrics_file, _ = QFileDialog.getOpenFileName(self, "가사 파일 선택", "", "Text Files (*.txt);;All Files (*)")

        if not lyrics_file:  # 사용자가 파일을 선택하지 않은 경우
            return

            # 파일 확장자 검사
        if not lyrics_file.endswith('.txt'):
            QMessageBox.warning(self, "파일 형식 오류", "TXT 파일만 선택할 수 있습니다.")
            return

        # 파일명 표시
        file_name = os.path.basename(lyrics_file)
        self.label_selected_lyrics.setText(file_name)

        # 가사 파일 읽기
        with open(lyrics_file, 'r', encoding='utf8') as file:
            self.lyrics = file.readlines()  # 한 줄씩 읽기

        # 기존 가사 삭제
        for i in reversed(range(self.vbox_lyrics.count())):
            self.vbox_lyrics.itemAt(i).widget().deleteLater()

        # 가사 내용 추가
        for line in self.lyrics:
            label_line = QLabel(line.strip())  # 한 줄씩 QLabel에 추가
            label_line.setWordWrap(True)  # 줄바꿈 가능하도록 설정
            self.vbox_lyrics.addWidget(label_line)
        # self.vbox_lyrics.setAlignment(QtCore.Qt.AlignCenter)



    def addMusicInstrument(self):
        curr_text = self.line_music_instrument.text().strip()

        if not curr_text or curr_text.startswith('추가할'):
            return  # 빈 문자열 또는 기본 텍스트일 경우 무시

        # 새로운 체크박스 생성 후 기존 스크롤바 레이아웃에 추가
        font_music_instrument = QFont()
        font_music_instrument.setPointSize(20)
        new_checkbox = self.makeCheckBox(None, 0, 0, 250, 100, curr_text, font=font_music_instrument)

        self.vbox_music_instrument.addWidget(new_checkbox)

        # 입력창 초기화
        self.line_music_instrument.clear()

    def request_GPT(self):
        return
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec_()
