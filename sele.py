import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

options = Options()
options.add_experimental_option('detach',True)  # 창 자동으로 종료되는 것을 방지

# options.add_argument("user-data-dir=C:\\user_data\\selenium_naver") # 실행 시 해당 경로에 폴더 생성, 폴더 내에 유저 정보 저장
options.add_argument("disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)
driver.maximize_window()

driver.get("https://taas.koroad.or.kr/gis/mcm/mcl/initMap.do?menuId=GIS_GMP_STS_RSN") # 원하는 경로 설정
#
# # 사고년도 선택 ----------------------------------------------------------------------------------------------------------------
start_year = Select(driver.find_element(By.CSS_SELECTOR,"#ptsRafYearStart"))
start_year.select_by_value(input("시작연도를 입력하시오: "))
time.sleep(2)
end_year = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafYearEnd"))
end_year.select_by_value(input("종료연도를 입력하시오: "))
time.sleep(2)

# # 시도 선택 ----------------------------------------------------------------------------------------------------------------
high_part_area = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafSido"))
high_part_area_options = high_part_area.options
for i in range(len(high_part_area_options)):
    high_part_area_options[i] = high_part_area_options[i].text
print(f"시도: {high_part_area_options}")
high_part_area.select_by_visible_text(input("시도를 선택하시오: "))
time.sleep(3)

# # 시군구 선택 ----------------------------------------------------------------------------------------------------------------
low_part_area = Select(driver.find_element(By.CSS_SELECTOR,"#ptsRafSigungu"))
low_part_area_options = low_part_area.options
for i in range(len(low_part_area_options)):
    low_part_area_options[i] = low_part_area_options[i].text
print(f"시군구: {low_part_area_options}")
low_part_area.select_by_visible_text(input("시군구를 선택하시오: "))
time.sleep(3)
#
# # 조건 선택 ----------------------------------------------------------------------------------------------------------------
singo = driver.find_element(By.CSS_SELECTOR,"#ptsRafCh1AccidentContent")
acident_text = list(map(lambda x: x.text, singo.find_elements(By.TAG_NAME, "li")))    # 텍스트 확인용
acident_list = singo.find_elements(By.CSS_SELECTOR, "input[type=checkbox]")
for n,v in enumerate(acident_text,start=1):
    print(n,v)

choose = list(map(int,input("체크할 수들을 입력하시오: ").split()))    # [1,2,3,4]
for c in choose:
    if not acident_list[c-1].is_selected():
        acident_list[c-1].click()
        time.sleep(1)
for i in acident_list:
    print(i.is_selected())

#
# # 유형 선택
#regionAccidentFind > div.condition-wrap > ul
high_part_tab = driver.find_element(By.CSS_SELECTOR, "#regionAccidentFind > div.condition-wrap > ul")
high_parts = high_part_tab.find_elements(By.TAG_NAME,'li')
high_parts_text = list(map(lambda x: x.text, high_parts))
print(high_parts_text)
high_parts_input = input("대분류를 선택하시오: ")
idx = high_parts_text.index(high_parts_input)
print(idx)
selected_high_part = high_parts[idx]
selected_high_part.click()
time.sleep(2)

# # 유형 하부 탭 설정
low_parts = selected_high_part.find_elements(By.CSS_SELECTOR, "li > input") # 체크용
low_parts_text = selected_high_part.find_elements(By.CSS_SELECTOR, "li")# 텍스트용
low_parts_text = ['전체선택'] + list(map(lambda x: x.text, low_parts_text))

print(list(enumerate(low_parts_text)))
choose_checkbox_idx = list(map(int,input().split()))

if choose_checkbox_idx[0] != 0:
    for i in range(1,len(low_parts)+1): # i: 1 ~ 12
        if i not in choose_checkbox_idx:
            low_parts[i-1].click()
        print(low_parts_text[i], low_parts[i-1].is_selected())
        time.sleep(1)

driver.find_element(By.CSS_SELECTOR,"#ptsRafCh1AccidentContent").click()
#

# # 사고부문
sago = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafSimpleCondition"))
sago_options = sago.options
sago_text = list(map(lambda x: x.text, sago_options))
print(sago_text)
time.sleep(1)
sago.select_by_visible_text(input("사고 부문을 선택하시오: "))
time.sleep(3)

# 검색하기
submit_btn = driver.find_element(By.CLASS_NAME,"btn-search")
submit_btn.click()
input()
driver.quit()
