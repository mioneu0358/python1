import time
from datetime import datetime
import sys
from PyQt5.uic import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
form_ui = loadUiType("GIS_TEST.ui")[0]

class MainWindow(QMainWindow, form_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initialize_data()

    # ui 적용시킬 데이터 초기화 or 세팅
    def initialize_data(self):
        # 시작년도 세팅
        self.startYear.addItem("시작 년도")
        self.endYear.addItem("끝 연도")
        self.startYear.lineEdit().setAlignment(Qt.AlignCenter)
        self.endYear.lineEdit().setAlignment(Qt.AlignCenter)
        curr_year = datetime.now().year # 현재 연도: int
        for y in range(curr_year-1, curr_year-16,-1):
            self.startYear.addItem(str(y))
        self.startYear.currentTextChanged.connect(self.changeEndYear)

        # 사이트에서 데이터 가져오기 -----------------------------------------------------------------------------------------
        options = Options()
        options.add_experimental_option('detach', True)  # 창 자동으로 종료되는 것을 방지
        options.add_argument("disable-blink-features=AutomationControlled")
        # options.add_argument('headless')
        driver = webdriver.Chrome(options=options)

        driver.get("https://taas.koroad.or.kr/gis/mcm/mcl/initMap.do?menuId=GIS_GMP_STS_RSN")

        self.sido.addItem("시/도를 선택하시오.")
        self.sigungu.addItem("시/군/구를 선택하시오.")
        self.sido.lineEdit().setAlignment(Qt.AlignCenter)
        self.sigungu.lineEdit().setAlignment(Qt.AlignCenter)

        self.sido_sigungu = {}

        high_part_area = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafSido"))
        low_part_area = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafSigungu"))

        for h_op in high_part_area.options:
            key = h_op.text
            high_part_area.select_by_visible_text(key)
            self.sido.addItem(key)
            print(key)
            time.sleep(1)
            values = list(map(lambda x: x.text, low_part_area.options))
            self.sido_sigungu[key] = values
        print(self.sido_sigungu)

        self.sido.currentTextChanged.connect(self.changeSigungu)



    def changeEndYear(self):
        # 시작년도를 기준으로 이후 2년까지 endYear에 담아준다.
        # 단, 최대 년도인 2023년을 넘은 값은 넣을 수 없다.
        s_year = self.startYear.currentText()
        if not s_year.isdigit(): return
        self.endYear.clear()
        for y in range(min(int(s_year)+2, datetime.now().year-1), int(s_year)-1,-1):
            self.endYear.addItem(str(y))

    def changeSigungu(self):
        sido = self.sido.currentText()
        if sido not in self.sido_sigungu: return
        self.sigungu.clear()
        for val in self.sido_sigungu[sido]:
            self.sigungu.addItem(val)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()