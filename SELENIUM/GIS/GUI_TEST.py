import time
from datetime import datetime
import sys
from PyQt5.uic import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import pickle
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback

form_ui = loadUiType("GUI_TEST.ui")[0]  # 저장한 UI 불러오기

class MainWindow(QMainWindow, form_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()

    # ui 적용시킬 데이터 초기화 or 세팅
    def initUi(self):                        # 실행버튼을 통해 실행중인지 확인
        self.setFixedSize(self.width(),self.height())   # 창 크기 고정
        # 콤보박스에 기본 텍스트 추가 및 가운데 정렬
        self.startYear.addItem("시작 년도")
        self.endYear.addItem("끝 연도")
        self.sido.addItem("시/도를 선택하시오.")
        self.sigungu.addItem("시/군/구를 선택하시오.")
        self.accidentType.addItem("사고 부문을 선택하시오.")
        self.startYear.lineEdit().setAlignment(Qt.AlignCenter)
        self.endYear.lineEdit().setAlignment(Qt.AlignCenter)
        self.sido.lineEdit().setAlignment(Qt.AlignCenter)
        self.sigungu.lineEdit().setAlignment(Qt.AlignCenter)
        self.accidentType.lineEdit().setAlignment(Qt.AlignCenter)

        # 기능 연결
        self.sido.currentTextChanged.connect(self.changeSigungu)        # 시도 변경시 시군구 변경
        self.runBtn.clicked.connect(self.RUN)                           # 실행 버튼에 함수 연결
        self.path_btn.clicked.connect(self.getPath)                     # 경로 변경 함수 연결

        # 다운로드 파일 경로와 이름
        self.downloadFilename = "accidentInfoList.xls"
        self.downloadPath = "C:\\Users\\ParkChanBin\\Downloads"
        self.downloadPath_label.setText(self.downloadPath)
        # 연도 범위 설정 ------------------------------------------------------------------------------
        curr_year = datetime.now().year   # 현재 연도: int
        for y in range(curr_year-1 , curr_year-16 , -1):
            self.startYear.addItem(str(y))
        self.startYear.currentTextChanged.connect(self.changeEndYear)
        # -------------------------------------------------------------------------------------------

        self.file_name = 'GIS_DB.pkl'           # 위젯에 사용할 데이터를 저장할 공간
        self.sido_sigungu = {}                  # {시도: 시군구}
        self.conditions = {}                    # {상위 조건: 하위 조건}
        self.accidentTypeList = []              # [노인보행자사고, 보행자사고, ...]

        if not os.path.isfile(self.file_name):  # DB유무 확인, 없으면 페이지에서 다운로드 있으면 불러오기
            self.downloadData()
        else:
            # self.file_name에 저장된 데이터 불러오기
            with open(self.file_name, 'rb') as file:
                self.sido_sigungu = pickle.load(file, encoding='utf8')
                self.conditions = pickle.load(file, encoding='utf8')
                self.accidentTypeList = pickle.load(file, encoding='utf8')

        # 시도/시군구 정보 등록 ---------------------------------------------------------------------------------
        for sido in self.sido_sigungu:
            self.sido.addItem(sido)

        # 세부 조건 탭 등록 -------------------------------------------------------------------------------------
        self.conditionsTab.clear()                      # 초기에 들어있는 tab들 제거
        for key, values in self.conditions.items():
            layout = QVBoxLayout()                      # tab에 넣을 위젯들을 담을 박스
            for val in values:                          # checkbox 생성 및 추가(체크 된 상태로)
                check = QCheckBox(val)
                check.click()
                layout.addWidget(check)

            tab = QWidget()
            tab.setLayout(layout)
            scroll = QScrollArea()
            scroll.setWidget(tab)
            scroll.setWidgetResizable(True)
            self.conditionsTab.addTab(scroll, key)

        # 사고부문 등록
        for acc in self.accidentTypeList:
            self.accidentType.addItem(acc)

    def downloadData(self):
        # 드라이버 옵션 설정 ---------------------------------------------------------------------------
        options = Options()
        options.add_experimental_option('detach', True)  # 창 자동으로 종료되는 것을 방지
        options.add_argument("disable-blink-features=AutomationControlled")
        # options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        driver.get("https://taas.koroad.or.kr/gis/mcm/mcl/initMap.do?menuId=GIS_GMP_STS_RSN")

        # 시도/시군구 정보 가져오기 ------------------------------------------------------------------------
        high_part_area = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafSido"))
        low_part_area = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafSigungu"))

        for h_op in high_part_area.options:
            key = h_op.text
            high_part_area.select_by_visible_text(key)
            time.sleep(1)
            values = list(map(lambda x: x.text, low_part_area.options))
            self.sido_sigungu[key] = values
        with open(self.file_name, 'wb') as file:
            pickle.dump(self.sido_sigungu, file)

        # 세부 조건 가져오기
        elem_high_part_tab = driver.find_element(By.CSS_SELECTOR, "#regionAccidentFind > div.condition-wrap > ul")
        elem_high_parts = elem_high_part_tab.find_elements(By.TAG_NAME, 'li')
        elem_high_parts_text = list(map(lambda x: x.text, elem_high_parts))
        for i in range(len(elem_high_parts)):
            elem_high_parts[i].click()
            time.sleep(1)
            low_parts = elem_high_parts[i].find_elements(By.CSS_SELECTOR, "li")  # 텍스트용
            low_parts_text = []
            parsed_low_parts = []
            for low in low_parts:
                if '\n' in low.text:
                    continue
                parsed_low_parts.append(low)
                low_parts_text.append(low.text)

            self.conditions[elem_high_parts_text[i]] = low_parts_text
            driver.find_element(By.CSS_SELECTOR, "#ptsRafCh1AccidentContent").click()

        with open(self.file_name, 'ab') as file:
            pickle.dump(self.conditions, file)

        # 사고부문 가져오기 ------------------------------------------------------------------------
        sago = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafSimpleCondition"))
        sago_options = sago.options
        self.accidentTypeList = list(map(lambda x: x.text, sago_options))[1:]
        with open(self.file_name,'ab') as file:
            pickle.dump(self.accidentTypeList,file)

    def changeEndYear(self):
        # 시작년도를 기준으로 이후 2년까지 endYear에 담아준다.
        # 단, 최대 년도인 2023년을 넘은 값은 넣을 수 없다.
        s_year = self.startYear.currentText()
        if not s_year.isdigit(): return
        self.endYear.clear()
        for y in range(min(int(s_year)+2, datetime.now().year-1), int(s_year)-1, -1):
            self.endYear.addItem(str(y))

    def changeSigungu(self):
        # 시도가 변경될 떄마다 시/군/구 정보 수정
        sido = self.sido.currentText()
        if sido not in self.sido_sigungu: return
        self.sigungu.clear()
        for val in self.sido_sigungu[sido]:
            self.sigungu.addItem(val)

    def RUN(self):  # 각 위젯 값들을 불러와 페이지에 전달.
        startYear = self.startYear.currentText()    # 시작 연도 : str/int
        endYear = self.endYear.currentText()        # 끝 연도   : str/int
        sido = self.sido.currentText()              # 시도      : str
        sigungu = self.sigungu.currentText()        # 시군구    : str
        accGrid = {}                                # 사고 경도 체크박스 : {사고유형: True/False}
        checked_conditions = {}                     # 세부 조건         : {상위조건: [하위조건체크(True/False), ...]}
        accType = self.accidentType.currentText()   # 사고부문   : str

     
        # 콤보박스 중 선택하지 않은 값들이 온 경우 아무것도 하지 않는다.
        if not startYear.isdigit() or not endYear.isdigit() or '선택하시오' in sido or '선택하시오'in sigungu or '선택하시오' in accType:
            print("검색조건 다시 선택")
            QMessageBox.about(self,"검색 오류","선택되지 못한 조건이 있습니다.")
            return
        if not os.path.isdir(self.downloadPath):
            print("경로 없음")
            QMessageBox.about(self,"경로 오류","잘못된 다운로드 경로입니다.")
            return


        # 사고 경도 체크박스 값 확인
        for row in range(self.accidentGrid.rowCount()):
            for col in range(self.accidentGrid.columnCount()):
                item = self.accidentGrid.itemAtPosition(row, col)
                if item is not None:
                    widget = item.widget()
                    if isinstance(widget, QCheckBox):  # QCheckBox인지 확인
                        accGrid[widget.text()] = widget.isChecked()

        # 세부 조건 탭 체크 유무 확인
        # self.conditionstab -> scrollarea -> tab(Qwidget) -> layout -> checkbox
        for i in range(self.conditionsTab.count()):
            tab_name = self.conditionsTab.tabText(i)  # 탭의 이름 (키)
            scroll_area = self.conditionsTab.widget(i)  # QScrollArea
            tab_widget = scroll_area.widget()  # 실제 탭의 QWidget
            layout = tab_widget.layout()  # QVBoxLayout

            checked_list = []  # 체크된 항목을 저장할 리스트
            for j in range(layout.count()):
                widget = layout.itemAt(j).widget()  # 레이아웃의 위젯 가져오기
                if isinstance(widget, QCheckBox):  # 체크박스인지 확인
                    checked_list.append(widget.isChecked())
            checked_conditions[tab_name] = checked_list  # 결과 딕셔너리에 저장


        # 지정한 설정값을 기준으로 나온 사고 내역 저장하기
        options = Options()
        # options.add_experimental_option('detach', True)  # 창 자동으로 종료되는 것을 방지
        options.add_argument("disable-blink-features=AutomationControlled")
        options.add_argument('headless')

        # 다운로드 경로 변경하기
        options.add_experimental_option("prefs", {
            "download.default_directory": self.downloadPath,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        driver.get("https://taas.koroad.or.kr/gis/mcm/mcl/initMap.do?menuId=GIS_GMP_STS_RSN")
        time.sleep(1)

        # 연도 설정
        elem_start_year = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafYearStart"))
        elem_start_year.select_by_value(startYear)
        elem_end_year = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafYearEnd"))
        elem_end_year.select_by_value(endYear)
        print("연도 설정 끝")
        # 시도 시군구 설정
        elem_sido = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafSido"))
        elem_sido.select_by_visible_text(sido)
        time.sleep(1)
        elem_sigungu = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafSigungu"))
        elem_sigungu.select_by_visible_text(sigungu)
        print('시도 시군구 설정 끝')
        # 사고 경도 설정
        print(accGrid)
        elem_accDegree_box = driver.find_element(By.CSS_SELECTOR, "#ptsRafCh1AccidentContent")
        elem_accDegree_list = elem_accDegree_box.find_elements(By.CSS_SELECTOR, "input[type=checkbox]")
        vals = list(accGrid.values())
        for i in range(len(vals)):
            if vals[i]:
                if not elem_accDegree_list[i].is_selected():
                    elem_accDegree_list[i].click()
            else:
                if elem_accDegree_list[i].is_selected():
                    elem_accDegree_list[i].click()
        print("사고 경도 체크박스 설정 끝")
        # 세부 조건 설정
        elem_high_part_tab = driver.find_element(By.CSS_SELECTOR, "#regionAccidentFind > div.condition-wrap > ul")
        elem_high_parts = elem_high_part_tab.find_elements(By.TAG_NAME, 'li')
        for i in range(len(elem_high_parts)):
            key = elem_high_parts[i].text
            elem_high_parts[i].click()
            elem_low_parts = elem_high_parts[i].find_elements(By.CSS_SELECTOR, "li")  # 텍스트용
            parsed_low_parts = []
            for low in elem_low_parts:
                if '\n' in low.text:
                    continue
                parsed_low_parts.append(low)
            values = checked_conditions[key]
            for j in range(len(values)):
                if not values[j]:
                    parsed_low_parts[j].find_element(By.TAG_NAME, 'input').click()
        driver.find_element(By.CSS_SELECTOR, "#ptsRafCh1AccidentContent").click()
        print('세부 조건 설정 끝')
        # 사고 부문 설정
        elem_sago = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafSimpleCondition"))
        elem_sago.select_by_visible_text(accType)
        print('사고부문 설정 끝')
        submit_btn = driver.find_element(By.CLASS_NAME, "btn-search")
        submit_btn.click()

        # 사고 내역이 없는 경우 경고창이 열리므로 이를 제어한다.
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            # 경고 창을 거부(취소)하는 동작 수행
            alert.accept()
            QMessageBox.about(self, "알림", "선택한 조건에 해당되는 사건이 없습니다.")

            return
        except Exception as e:
            tr = traceback.format_exc()
            print(tr)
            print(e)

        # 기존의 요소에서 text를 가져옵니다.
        case_cnt = driver.find_element(By.CSS_SELECTOR,
                                      "#regionAccidentFind > div.searc-total > div.total-count > span")
        # 텍스트가 변경된 후 새로운 텍스트를 가져옵니다.
        case_cnt = case_cnt.text
        print(case_cnt)
        print(f"건수: {case_cnt.replace(',','')}")

        # 목록 보기 버튼
        get_data_btn = driver.find_element(By.CSS_SELECTOR,"#regionAccidentFind > div.searc-total > div.btn > p > a")
        get_data_btn.click()
        print('목록보기')
        # 새로 열린 창으로 driver전환 기존 driver가 0번째
        driver.switch_to.window(driver.window_handles[1])
        # excel로 다운로드 버튼(다운로드 경로는 크롬에 설정된 다운로드 경로로 다운로드 된다.)
        to_Excel_btn = driver.find_element(By.CSS_SELECTOR, "body > div > input")
        to_Excel_btn.click()
        print("다운로드 시작")
        time.sleep(5)

        for i in range(20):
            time.sleep(1)
            print(self.downloadPath + '\\' + self.downloadFilename)
            if os.path.isfile(self.downloadPath + '\\' + self.downloadFilename):
                print("저장 완료")
                QMessageBox.about(self,"성공", "다운로드에 성공하였습니다.")
                break
        else:
            print("저장 실패")
            QMessageBox.about(self,"실패", "다운로드에 실패하였습니다.")




    def getPath(self):
        path = QFileDialog.getSaveFileUrl()
        selected_path = path[0].path().split('/')   # "/C:/Users/turing02/Desktop/test"
        print(selected_path)
        self.downloadPath = '\\'.join(selected_path[1:-1])
        # self.downloadFilename = selected_path[-1]
        print(self.downloadPath, self.downloadFilename)
        self.downloadPath_label.setText(self.downloadPath)

# https://disco-railway-5d7.notion.site/108644b8f37380d7858bdb0c5460b88d?pvs=4
# https://disco-railway-5d7.notion.site/271cef58f5244f5ab47a1f47a7a75461?pvs=4


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
