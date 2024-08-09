import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

options = Options()
options.add_experimental_option('detach',True)  # 창 자동으로 종료되는 것을 방지

options.add_argument("disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(options=options)
# driver.maximize_window()

driver.get("https://taas.koroad.or.kr/gis/mcm/mcl/initMap.do?menuId=GIS_GMP_STS_RSN") # 원하는 경로 설정

# 연도 선택
start_year = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafYearStart"))
start_year.select_by_value(input("연도를 입력하시오: "))

end_year = Select(driver.find_element(By.CSS_SELECTOR, "#ptsRafYearEnd"))
end_year.select_by_value(input("연도를 입력하시오: "))


# 시도 선택 - 시군구 선택
sido = Select(driver.find_element(By.CSS_SELECTOR,"#ptsRafSido"))
sido_text = list(map(lambda x : x.text, sido.options))
print(sido_text)
sido.select_by_visible_text(input("시도를 선택하시오: "))
time.sleep(3)

sigungu = Select(driver.find_element(By.CSS_SELECTOR,"#ptsRafSigungu"))
sigungu_text = list(map(lambda x: x.text, sigungu.options))
print(sigungu_text)
sigungu.select_by_visible_text(input("시군구를 선택하시오: "))


# 사고유형 선택

# 체크박스들이 들어있는 frame을 가져온다.
accident_table = driver.find_element(By.CSS_SELECTOR, '#ptsRafCh1AccidentContent')
accident_list = accident_table.find_elements(By.TAG_NAME, "input")  # 체크박스들
# frame안에 있는 사망사고, 중상사고, 경상사고, 부상신고 체크박스들을 담은 리스트를 만든다.
accident_text = list(map(lambda x: x.text, accident_table.find_elements(By.TAG_NAME, "li")))
# 이 체크박스들의 텍스트를 보여준다.(1.사망사고 2. 중상사고 3.경상사고 4.부상신고)
print(list(enumerate(accident_text, start=1)))
# 내가 체크할 번호들을 입력받는다. ex) 1 2 3
accident_nums = list(map(int, input("체크할 항목들의 번호를 입력하시오: ").split()))
# 1 3 4 => [1,3,4]
# 입력받은 번호에 대한 체크박스들을 클릭한다.
for num in range(len(accident_list)):
    if num + 1 in accident_nums:
        if not accident_list[num].is_selected():
            accident_list[num].click()
    else:
        if accident_list[num].is_selected():
            accident_list[num].click()
    print(accident_list[num].is_selected())
    time.sleep(1)

input()
driver.quit()
