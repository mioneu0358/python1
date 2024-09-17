import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,450,200)

        self.accidentType = QComboBox(self)
        self.accidentType.setGeometry(10,10,300,30)
        self.accidentType.setEditable(True)
        self.accidentType.lineEdit().setAlignment(Qt.AlignCenter)
        self.accidentType.blockSignals(False)

        self.btn = QPushButton(self,)
        self.btn.setText('실행')
        self.btn.setGeometry(350,10, 70,100)
        self.initialize_data()

        self.path_btn = QPushButton(self)
        self.path_btn.setText("경로 설정")
        self.path_btn.setGeometry(10,100,150,50)
        self.path_btn.clicked.connect(self.getPath)

    def initialize_data(self):
        file_name = "TEST_DB.pkl"
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as file:
                self.accidentTypeList = pickle.load(file, encoding='utf8')
        else:
            options = Options()
            options.add_experimental_option('detach', True)  # 창 자동으로 종료되는 것을 방지
            options.add_argument("disable-blink-features=AutomationControlled")
            # options.add_argument("headless")
            driver = webdriver.Chrome(options=options)
            driver.get("https://taas.koroad.or.kr/gis/mcm/mcl/initMap.do?menuId=GIS_GMP_STS_RSN")  # 원하는 경로 설정

            sago = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafSimpleCondition"))
            sago_options = sago.options
            self.accidentTypeList = list(map(lambda x: x.text, sago_options))
            print(self.accidentTypeList)
            with open(file_name, 'ab') as file:
                pickle.dump(self.accidentTypeList,file)

        for val in self.accidentTypeList:
            self.accidentType.addItem(val)

        self.btn.clicked.connect(self.RUN)


    def RUN(self):
        print(f"사고부문: {self.accidentType.currentText()}")
    def getPath(self):
        path = QFileDialog.getSaveFileUrl()
        print(path)
        selected_path = path[0].path()
        print(selected_path)
        print(type(selected_path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
