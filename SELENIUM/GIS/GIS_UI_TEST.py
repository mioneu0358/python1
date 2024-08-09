import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from PyQt5.uic import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
form_ui = loadUiType("GIS_UI_TEST.ui")[0]

class MainWindow(QMainWindow, form_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_UI()
        self.initialize_data()
        self.show()
    def init_UI(self):
        self.startYear.addItem('시작연도')
        self.endYear.addItem('종료연도')
        self.sido.addItem("시도를 선택하시오.")
        self.sigungu.addItem("시군구를 선택하시오.")
        # 가운데 정렬 방식
        self.sido.lineEdit().setAlignment(Qt.AlignCenter)
        self.sigungu.lineEdit().setAlignment(Qt.AlignCenter)
        self.sido.currentTextChanged.connect(self.changeSigungu)
        # self.sido_sigungu = {'서울특별시': [':: 전체 ::', '강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구'], '부산광역시': [':: 전체 ::', '강서구', '금정구', '기장군', '남구', '동구', '동래구', '부산진구', '북구', '사상구', '사하구', '서구', '수영구', '연제구', '영도구', '중구', '해운대구'], '대구광역시': [':: 전체 ::', '군위군', '남구', '달서구', '달성군', '동구', '북구', '서구', '수성구', '중구'], '인천광역시': [':: 전체 ::', '강화군', '계양구', '남구(구)', '남동구', '동구', '미추홀구', '부평구', '서구', '연수구', '옹진군', '중구'], '광주광역시': [':: 전체 ::', '광산구', '남구', '동구', '북구', '서구'], '대전광역시': [':: 전체 ::', '대덕구', '동구', '서구', '유성구', '중구'], '울산광역시': [':: 전체 ::', '남구', '동구', '북구', '울주군', '중구'], '세종특별자치시': [':: 전체 ::', '세종특별자치시'], '경기도': [':: 전체 ::', '가평군', '고양시', '- 고양시 덕양구', '- 고양시 일산동구', '- 고양시 일산서구', '과천시', '광명시', '광주시', '구리시', '군포시', '김포시', '남양주시', '동두천시', '부천시', '부천시소사구(구)', '부천시오정구(구)', '부천시원미구(구)', '성남시', '- 성남시 분당구', '- 성남시 수정구', '- 성남시 중원구', '수원시', '- 수원시 권선구', '- 수원시 영통구', '- 수원시 장안구', '- 수원시 팔달구', '시흥시', '안산시', '- 안산시 단원구', '- 안산시 상록구', '안성시', '안양시', '- 안양시 동안구', '- 안양시 만안구', '양주시', '양평군', '여주군(구)', '여주시', '연천군', '오산시', '용인시', '- 용인시 기흥구', '- 용인시 수지구', '- 용인시 처인구', '의왕시', '의정부시', '이천시', '파주시', '평택시', '포천시', '하남시', '화성시'], '강원특별자치도': [':: 전체 ::', '강릉시', '고성군', '동해시', '삼척시', '속초시', '양구군', '양양군', '영월군', '원주시', '인제군', '정선군', '철원군', '춘천시', '태백시', '평창군', '홍천군', '화천군', '횡성군'], '충청북도': [':: 전체 ::', '괴산군', '단양군', '보은군', '영동군', '옥천군', '음성군', '제천시', '증평군', '진천군', '청원군(구)', '청주시', '- 청주시 상당구', '- 청주시 서원구', '- 청주시 청원구', '- 청주시 흥덕구', '충주시'], '충청남도': [':: 전체 ::', '계룡시', '공주시', '금산군', '논산시', '당진군(구)', '당진시', '보령시', '부여군', '서산시', '서천군', '아산시', '연기군(구)', '예산군', '천안시', '천안시(구)', '- 천안시 동남구', '- 천안시 서북구', '청양군', '태안군', '홍성군'], '전라북도': [':: 전체 ::', '고창군', '군산시', '김제시', '남원시', '무주군', '부안군', '순창군', '완주군', '익산시', '임실군', '장수군', '전주시', '- 전주시 덕진구', '- 전주시 완산구', '정읍시', '진안군'], '전라남도': [':: 전체 ::', '강진군', '고흥군', '곡성군', '광양시', '구례군', '나주시', '담양군', '목포시', '무안군', '보성군', '순천시', '신안군', '여수시', '영광군', '영암군', '완도군', '장성군', '장흥군', '진도군', '함평군', '해남군', '화순군'], '경상북도': [':: 전체 ::', '경산시', '경주시', '고령군', '구미시', '군위군(구)', '김천시', '문경시', '봉화군', '상주시', '성주군', '안동시', '영덕군', '영양군', '영주시', '영천시', '예천군', '울릉군', '울진군', '의성군', '청도군', '청송군', '칠곡군', '포항시', '- 포항시 남구', '- 포항시 북구'], '경상남도': [':: 전체 ::', '거제시', '거창군', '고성군', '김해시', '남해군', '마산시(구)', '밀양시', '사천시', '산청군', '양산시', '의령군', '진주시', '진해시(구)', '창녕군', '창원시', '- 창원시 마산합포구', '- 창원시 마산회원구', '- 창원시 성산구', '- 창원시 의창구', '- 창원시 진해구', '창원시(구)', '통영시', '하동군', '함안군', '함양군', '합천군'], '제주도': [':: 전체 ::', '서귀포시', '제주시']}
        # for key in self.sido_sigungu:
        #     self.sido.addItem(key)
        # test_combo = QComboBox(self)
        # test_combo.()


    def initialize_data(self):
            options = Options()
            options.add_experimental_option('detach', True)  # 창 자동으로 종료되는 것을 방지
            options.add_argument("disable-blink-features=AutomationControlled")
            options.add_argument('headless')
            driver = webdriver.Chrome(options=options)

            driver.get("https://taas.koroad.or.kr/gis/mcm/mcl/initMap.do?menuId=GIS_GMP_STS_RSN")
            for y in range(2007, 2025):
                self.startYear.addItem(str(y))

            self.sido_sigungu = {}
            high_part_area = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafSido"))
            for h_op in high_part_area.options:
                key = h_op.text
                high_part_area.select_by_visible_text(key)
                self.sido.addItem(key)
                print(key)
                time.sleep(1)
                low_part_area = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafSigungu"))
                values = list(map(lambda x: x.text, low_part_area.options))
                self.sido_sigungu[key] = values
                time.sleep(1)
            print(self.sido_sigungu)
    def changeSigungu(self):
        key = self.sido.currentText()
        print(key)
        self.sigungu.clear()
        for val in self.sido_sigungu[key][1:]:
            self.sigungu.addItem(val)



if __name__ == "__main__":
    app =QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
