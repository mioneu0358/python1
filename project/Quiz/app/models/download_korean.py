from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

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
            filtered_df = filtered_df.loc[:,['표제어','뜻풀이']].dropna()
            # 결과 출력
            # print(filtered_df)
            temp_data = {}
            while len(temp_data) < 10:
                random_word = filtered_df.iloc[random.randint(0,len(filtered_df)-1)]
                temp_data[random_word["표제어"].strip()] = random_word['뜻풀이'].strip()
            korean_data.update(temp_data)

    return korean_data

# 영어 --------------------------------------------------------------------------------------------------------
import random
import nltk
from nltk.corpus import words, brown
from collections import Counter

def get_english():
    # NLTK 데이터 다운로드 (한번만 실행하면 됩니다)
    nltk.download('words')
    nltk.download('brown')
    # nltk.download('averaged_perceptron_tagger')
    nltk.download('averaged_perceptron_tagger_eng')
    # 생성하고자 하는 영단어 개수를 입력
    word_count = 100

    # 모든 영어 단어 목록
    word_list = words.words()

    # Brown 코퍼스의 단어 목록과 빈도 계산
    brown_words = brown.words()
    word_freq = Counter(brown_words)

    # 빈도가 높은 상위 단어 5000개 선택
    common_words = {word for word, freq in word_freq.most_common(5000)}

    # word_list에서 상위 빈도 단어만 선택
    filtered_word_list = list(filter(lambda x: x.islower() and x in word_list, common_words))
    # print(filtered_word_list)

    # 품사 태깅하여 명사와 동사만 필터링
    tagged_words = nltk.pos_tag(filtered_word_list)
    # 명사와 동사 품사 태그 목록
    noun_tags = {'NN', 'NNS', 'NNP', 'NNPS'}
    verb_tags = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}

    # 명사와 동사만 필터링
    filtered_nouns_and_verbs = list(filter(lambda x: x[1] in noun_tags or x[1] in verb_tags, tagged_words))
    # # 그 중 랜덤하게 500개의 단어를 선택합니다.
    random_words = random.sample(filtered_nouns_and_verbs, word_count)
    english_data = {}
    for word,_ in random_words:
        print(word)
        driver.get(f"https://en.dict.naver.com/#/search?query={word}")
        kor_mean = []

        try:
            mean_box = driver.find_element(By.CSS_SELECTOR,
                                           "#searchPage_entry > div > div:nth-child(1) > ul:nth-child(2)")
            mean = mean_box.text.replace('.\n', ' ').replace(';', '').split('\n')
            kor_mean.extend(mean)
        except Exception as e:
            print(e)
            break
        english_data[word] = kor_mean
    return english_data

