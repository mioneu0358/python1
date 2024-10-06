import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
options = Options()
options.add_experimental_option('detach', True)  # 창 자동으로 종료되는 것을 방지
options.add_argument("disable-blink-features=AutomationControlled")
# options.add_argument('headless')

# # 다운로드 경로 변경하기
# options.add_experimental_option("prefs", {
#     "download.default_directory": self.downloadPath,
#     "download.prompt_for_download": False,
#     "download.directory_upgrade": True,
#     "safebrowsing.enabled": True
# })

# 1. 검색할 기사의 키워드를 입력하고, 실제로 웹 페이지에서도 키워드를 검색
query = input("검색할 기사의 키워드를 입력하시오: ")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)
driver.get(f"https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query={query}")

# 2. 옵션 설정 (1. 정렬기준, 2. 기간)
optionBtn = driver.find_element(By.CSS_SELECTOR,"#snb > div.mod_group_option_filter._search_option_simple_wrap > div > div.option_filter > a")
                                                 # snb > div.mod_group_option_filter._search_option_simple_wrap > div > div.option_filter > a
optionBtn.click()


# 정렬 기준
sortby = int(input("정렬기준을 선택하시오:(1. 관련도순, 2. 최신순, 3. 오래된순)"))
sortTab = driver.find_element(By.CSS_SELECTOR, "#snb > div.mod_group_option_sort._search_option_detail_wrap > ul > li.bx.lineup > div > div")
sortBtns = sortTab.find_elements(By.TAG_NAME, 'a')

sortBtns[sortby-1].click()
if sortby != 3:
    optionBtn = driver.find_element(By.CSS_SELECTOR,
                                    "#snb > div.mod_group_option_filter._search_option_simple_wrap > div > div.option_filter > a")
    # snb > div.mod_group_option_filter._search_option_simple_wrap > div > div.option_filter > a
    optionBtn.click()

# 기간
period = int(input("기간을 선택하시오:(0.전체, 1. n시간전, 2. 1일전, 3. 1주전, 4. 1개월전, 5. 3개월전, 6. 6개월전, 7. 1년전, 8. 직접입력"))
periodTab = driver.find_element(By.CSS_SELECTOR, "#snb > div.mod_group_option_sort._search_option_detail_wrap > ul > li.bx.term > div > div.option")
periodElems = periodTab.find_elements(By.TAG_NAME,'a')

periodElems[period].click()
if period == 1:
    hoursTab = driver.find_element(By.CSS_SELECTOR, "#snb > div.mod_group_option_sort._search_option_detail_wrap > ul > li.bx.term > div > div.mod_select_option._time_select_layer > div > div > div > div > div > ul")
    hours = hoursTab.find_elements(By.TAG_NAME,'li')
    n = int(input(f"몇 시간전 기사를 찾으실건가요?:(1 ~ {len(hours)}) "))
    hours[n-1].find_element(By.TAG_NAME,'a').click()
elif period == 8:

    def setDate(date):
        YMD = dateTab.find_elements(By.TAG_NAME, 'ul')
        for i in range(len(YMD)):
            elems = YMD[i].find_elements(By.TAG_NAME, 'li')
            if i == 0:
                first_year = int(elems[0].text)
                elems[date[i] - first_year].click()
            else:
                elems[date[i] - 1].click()


    dateTab = driver.find_element(By.CSS_SELECTOR,
                                  "#snb > div.mod_group_option_sort._search_option_detail_wrap > ul > li.bx.term > div > div.mod_select_option.type_calendar._calendar_select_layer > div.select_wrap._root")
    now = datetime.now()
    while True:  # 유효성 검사
        start = input("시작일을 입력하시오: (년-월-일) ")
        if now > datetime.strptime(start, "%Y-%m-%d"):
            break
    start = list(map(int, start.split('-')))
    setDate(start)
    while True:
        end = input("종료일을 입력하시오: (년-월-일) ")
        if datetime.now() > datetime.strptime(end, "%Y-%m-%d") and datetime.strptime(end,
                                                                                     "%Y-%m-%d") >= datetime.strptime(
                f"{start[0]}-{start[1]}-{start[2]}", "%Y-%m-%d"):
            break
    driver.find_element(By.CSS_SELECTOR,
                        "#snb > div.mod_group_option_sort._search_option_detail_wrap > ul > li.bx.term > div > div.mod_select_option.type_calendar._calendar_select_layer > div.set_calendar > span:nth-child(3) > a").click()
    # 종료일을 연, 월, 일로 나누어 리스트로 저장
    end = list(map(int, end.split('-')))
    setDate(end)

input()
