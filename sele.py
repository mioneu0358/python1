import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

options = Options()
options.add_experimental_option('detach',True)  # 창 자동으로 종료되는 것을 방지

options.add_argument("user-data-dir=C:\\user_data\\selenium_naver") # 실행 시 해당 경로에 폴더 생성, 폴더 내에 유저 정보 저장
options.add_argument("disable-blink-features=AutomationControlled")
# options.add_experimental_option('excludeSwitches', ["enalbe-logging"]) # 브라우저 실행시 로그 출력 비활성화 설정

driver = webdriver.Chrome(options=options)
driver.maximize_window()

driver.get("https://taas.koroad.or.kr/gis/mcm/mcl/initMap.do?menuId=GIS_GMP_STS_RSN")


# 사고년도 선택 ----------------------------------------------------------------------------------------------------------------
start_year = Select(driver.find_element(By.CSS_SELECTOR,"#ptsRafYearStart"))
start_year.select_by_value(input("시작연도를 입력하시오: "))
time.sleep(2)
end_year = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafYearEnd"))
end_year.select_by_value(input("종료연도를 입력하시오: "))
time.sleep(2)

# 시도 선택 ----------------------------------------------------------------------------------------------------------------
high_part_area = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafSido"))
high_part_area_options = high_part_area.options
for i in range(len(high_part_area_options)):
    high_part_area_options[i] = high_part_area_options[i].text
print(f"시도: {high_part_area_options}")
high_part_area.select_by_visible_text(input("시도를 선택하시오: "))
time.sleep(3)

# 시군구 선택 ----------------------------------------------------------------------------------------------------------------
low_part_area = Select(driver.find_element(By.CSS_SELECTOR,"#ptsRafSigungu"))
low_part_area_options = low_part_area.options
for i in range(len(low_part_area_options)):
    low_part_area_options[i] = low_part_area_options[i].text
print(f"시군구: {low_part_area_options}")
low_part_area.select_by_visible_text(input("시군구를 선택하시오: "))
time.sleep(3)

# 조건 선택 ----------------------------------------------------------------------------------------------------------------
singo = driver.find_element(By.CSS_SELECTOR,"#ptsRafCh1AccidentContent")
acident_text = list(map(lambda x: x.text, singo.find_elements(By.TAG_NAME, "li")))    # 텍스트 확인용
acident_list = singo.find_elements(By.CSS_SELECTOR, "input[type=checkbox]")
for n,v in enumerate(acident_text,start=1):
    print(n,v)

choose = list(map(int,input("체크할 수들을 입력하시오").split()))
for c in choose:
    if not acident_list[c-1].is_selected():
        acident_list[c-1].click()
        time.sleep(1)
for i in acident_list:
    print(i.is_selected())


# 사고부문
sago = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafSimpleCondition"))
sago_options = sago.options
sago_text = list(map(lambda x: x.text, sago_options))
print(sago_text)
time.sleep(1)
sago.select_by_visible_text(input("사고 부문을 선택하시오: "))
time.sleep(3)

# 검색하기
submit_btn = driver.find_element(By.CSS_SELECTOR,"#regionAccidentFind > div.condition-wrap > p > a")
submit_btn.click()
input()
driver.quit()
