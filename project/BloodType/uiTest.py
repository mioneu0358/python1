import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,800,640)

        mainFrame = QFrame(self,)
        mainFrame.setGeometry(10,20,780,600)
        mainFrame.setFrameStyle(1)  # (0: None, 1: box, 2: Panel, 3: WinPanel, 4:Hline, 5:Vline,
        settingFrame = QFrame(mainFrame)
        settingFrame.setFrameStyle(1)
        settingFrame.setGeometry(10,5,760,100)

        whoText = QLabel(settingFrame)
        whoText.setText("가족 구성원")
        whoText.setFrameStyle(1)
        whoText.setEnabled(True)
        whoText.setAlignment(Qt.AlignCenter)
        whoText.setGeometry(30,15,200,30)

        self.whoCombo = QComboBox(settingFrame)
        self.whoCombo.setEditable(True)
        self.whoCombo.lineEdit().setAlignment(Qt.AlignCenter)
        familyText = ["아빠","엄마","나","형","누나",'남동생',"여동생", "할아버지","할머니","외할아버지","외할머니"]
        for fam in familyText:
            self.whoCombo.addItem(fam)
        self.whoCombo.setGeometry(30,45,200,40)

        bloodtypeText = QLabel(settingFrame)
        bloodtypeText.setText("혈액형")
        bloodtypeText.setFrameStyle(1)
        bloodtypeText.setEnabled(True)
        bloodtypeText.setAlignment(Qt.AlignCenter)
        bloodtypeText.setGeometry(250,15, 200, 30)

        self.bloodtypeCombo = QComboBox(settingFrame)
        self.bloodtypeCombo.setEditable(True)
        self.bloodtypeCombo.lineEdit().setAlignment(Qt.AlignCenter)
        for t in ['A','B','O','AB']:
            self.bloodtypeCombo.addItem(t)
        self.bloodtypeCombo.setGeometry(250,45,200,40)


        self.makeBoxBtn = QPushButton(settingFrame,text='생성')
        self.makeBoxBtn.setGeometry(600,20,120,60)
        self.makeBoxBtn.clicked.connect(self.makeBox)


    def makeBox(self):
        who = self.whoCombo.currentText()
        bloodType = self.bloodtypeCombo.currentText()
        print(who,bloodType)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
