import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import os

options = Options()
options.add_experimental_option('detach',True)  # 창 자동으로 종료되는 것을 방지

# options.add_argument("user-data-dir=C:\\user_data\\selenium_naver") # 실행 시 해당 경로에 폴더 생성, 폴더 내에 유저 정보 저장
options.add_argument("disable-blink-features=AutomationControlled")

# 다운로드 경로 변경하기
download_directory = "C:\\Users\\turing15\\Desktop"
options.add_experimental_option("prefs", {
  "download.default_directory": download_directory,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})


driver = webdriver.Chrome(options=options)
driver.maximize_window()

driver.get("https://taas.koroad.or.kr/gis/mcm/mcl/initMap.do?menuId=GIS_GMP_STS_RSN") # 원하는 경로 설정
time.sleep(1)
# 검색 버튼
search_btn = driver.find_element(By.CSS_SELECTOR,"#regionAccidentFind > div.condition-wrap > p > a")
search_btn.click()
time.sleep(1)
# 사건 수 확인
case_cnt = driver.find_element(By.CSS_SELECTOR,"#regionAccidentFind > div.searc-total > div.total-count > span").text
print(case_cnt)
if int(case_cnt) != 0:
    # 목록 보기 버튼
    get_data_btn = driver.find_element(By.CSS_SELECTOR,"#regionAccidentFind > div.searc-total > div.btn > p > a")
    get_data_btn.click()
    # 새로 열린 창으로 driver전환 기존 driver가 0번째
    driver.switch_to.window(driver.window_handles[1])
    # excel로 다운로드 버튼(다운로드 경로는 크롬에 설정된 다운로드 경로로 다운로드 된다.)
    to_Excel_btn = driver.find_element(By.CSS_SELECTOR,"body > div > input")
    to_Excel_btn.click()
    time.sleep(5)
    download_file_name = "accidentInfoList.xls"
    while True:
        time.sleep(1)
        if os.path.isfile(download_directory+'\\'+download_file_name):
            print("저장 완료")
            break
        else:
            print("저장 실패")
input()
