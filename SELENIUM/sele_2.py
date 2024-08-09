import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

options = Options()
options.add_experimental_option('detach',True)  # 창 자동으로 종료되는 것을 방지

options.add_argument("user-data-dir=C:\\user_data\\selenium_naver") # 실행 시 해당 경로에 폴더 생성, 폴더 내에 유저 정보 저장
options.add_argument("disable-blink-features=AutomationControlled")
# options.add_experimental_option('excludeSwitches', ["enalbe-logging"]) # 브라우저 실행시 로그 출력 비활성화 설정

# 네이버 로그인하기
driver = webdriver.Chrome(options=options)
driver.maximize_window()

driver.get("https://www.naver.com")

# """
# <input id="query" name="query" type="search" title="검색어를 입력해 주세요." placeholder="검색어를 입력해 주세요."
#  maxlength="255" autocomplete="off" class="search_input" data-atcmp-element="">
# """

driver.find_element(By.CLASS_NAME, "search_input").send_keys("블랙핑크")
time.sleep(2)

driver.find_element(By.ID, "query").send_keys("뉴진스")
time.sleep(2)

driver.find_element(By.NAME, "query").send_keys("에스파")
time.sleep(2)

driver.find_element(By.CSS_SELECTOR, "#query").send_keys("아이브")
time.sleep(2)

driver.find_element(By.CSS_SELECTOR, ".search_input").send_keys("아일릿")
time.sleep(2)

