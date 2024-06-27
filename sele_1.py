from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
import time
chromedriver_autoinstaller.install()

driver = webdriver.Chrome()
driver.get("https://www.google.com")
time.sleep(3)




# # -------------------------------------------------------------------------
# selector = "#shortcutArea > ul > li:nth-child(4) > a > span.service_icon.type_shopping"
# # 데이터 출력하기
# data = driver.find_element(By.CSS_SELECTOR, selector)
# print(data.text)
#
# data.click()
# # 1-1 get() 원하는 페이지로 이동
# driver.get("https://www.google.com")
# time.sleep(3)
# # back: 뒤로가기
# driver.back()
# time.sleep(3)
# # forward: 앞으로 가기
# driver.forward()
# time.sleep(3)
# # refresh(): 새로고침
# driver.refresh()
# time.sleep(3)
# # -------------------------------------------------------------------------
# 2. browser information
# 2-1. title: 웹 사이트의 타이틀을 가져옴
# title = driver.title
# print(f"title: {title}")
# # 2-2 current_url 주소창을 그대로 가져온다.
# curr_url = driver.current_url
# print(f"curr_url: {curr_url}")
# # -------------------------------------------------------------------------
# 3-1 3초때 로딩이 끝나서 element를 찾음wait
# 3-2 30초 까지는 기다린다.
# 3-3 30초 넘어가면 에러 발생

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 드라이버를 10초간 대기, EC.presence_of_element_located()안에 들어있는 항목이 나올 때까지
try:
    selector = "#shortcutArea > ul > li:nth-child(5) > a > span.service_icon.type_news"
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    print('코드 수행')
except:
    print('예외 발생')
print("종료")
