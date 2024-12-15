import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import traceback
import os
import zipfile
import pandas as pd
import random
download_path = os.getcwd()


# 다운로드 할지 말지

options = Options()
options.add_experimental_option("prefs", {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# options.add_experimental_option('detach', True)  # 창 자동으로 종료되는 것을 방지
options.add_argument("disable-blink-features=AutomationControlled")
options.add_argument('headless')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)


def get_korean():
    driver.get(f"https://krdict.korean.go.kr/kor/mainAction")
    driver.find_element(By.CSS_SELECTOR,
                        "#footer > div > div.foot_menu > ul > li:nth-child(6) > a").click()  # 사전 전체 내려받기 버튼 클릭
    driver.switch_to.window(driver.window_handles[1])  # 새로 생긴 창으로 전환
    driver.find_element(By.CSS_SELECTOR, "#downloadBox > button:nth-child(1)").click()       # 다운로드 받기

    # 다운로드 되었다면 압축 풀기
    download_state = False
    while not download_state:
        for f_name in os.listdir(download_path):
            if f_name.startswith("전체 내려받기"):
                with zipfile.ZipFile(f_name, "r") as zip_ref:
                    zip_ref.extractall("./")
                download_state = True
                break

    korean_data = {}
    # 압축 풀은 엑셀 파일 읽기
    for f_name in os.listdir(download_path):
        if f_name.endswith(".xls"):
            # 데이터프레임으로 엑셀 읽기
            print(f_name)
            df = pd.read_excel(f_name)
            # print(df)
            # 특정 열에서 '명사'라는 단어로 필터링 (예: '열 이름'이 'Type'이라고 가정)
            filtered_df = df[df['품사'].str.contains('명사', na=False)]
            filtered_df = filtered_df.loc[:,['표제어',"뜻풀이"]].dropna()
            # 결과 출력
            # print(filtered_df)
            temp_data = {}
            while len(temp_data) < 10:
                random_word = filtered_df.iloc[random.randint(0,len(filtered_df)-1)]
                temp_data[random_word["표제어"].strip()] = random_word['뜻풀이'].strip()
            korean_data.update(temp_data)

    return korean_data
