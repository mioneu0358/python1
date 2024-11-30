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

options = Options()
options.add_experimental_option('detach', True)  # 창 자동으로 종료되는 것을 방지
options.add_argument("disable-blink-features=AutomationControlled")
# options.add_argument('headless')


driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)
driver.get(f"https://ko.wiktionary.org/wiki/분류:한국어_명사")

# tbody = driver.find_element(By.CSS_SELECTOR,"#mw-content-text > div.mw-content-ltr.mw-parser-output > table > tbody").find_elements()
korean_start_words = driver.find_elements(By.CLASS_NAME, "BGImage_c")
# words = list(map(lambda x: x.text, korean_start_words))

import random
korean_words = {}
word_pages = [random.choice(korean_start_words) for _ in range(20)]

for page in word_pages:
    page.click()
    word_list = driver.find_element(By.CSS_SELECTOR,"#mw-pages > div > div")
    li_list = word_list.find_elements(By.CLASS_NAME,'a')
    print(len(li_list))
    selected = random.choice(li_list)

    input()
    driver.back()