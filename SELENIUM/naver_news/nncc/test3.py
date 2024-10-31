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
# options.add_experimental_option('detach', True)  # 창 자동으로 종료되는 것을 방지
options.add_argument("disable-blink-features=AutomationControlled")
# options.add_argument('headless')

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
time.sleep(1)


if sortby != 3:
    optionBtn = driver.find_element(By.CSS_SELECTOR,
                                    "#snb > div.mod_group_option_filter._search_option_simple_wrap > div > div.option_filter > a")
    optionBtn.click()

# 기간
period = int(input("기간을 선택하시오:(0.전체, 1. n시간전, 2. 1일전, 3. 1주전, 4. 1개월전, 5. 3개월전, 6. 6개월전, 7. 1년전, 8. 직접입력) "))
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
        if datetime.now() > datetime.strptime(end, "%Y-%m-%d") and datetime.strptime(end,"%Y-%m-%d") >= datetime.strptime(f"{start[0]}-{start[1]}-{start[2]}", "%Y-%m-%d"):
            break
    driver.find_element(By.CSS_SELECTOR,
                        "#snb > div.mod_group_option_sort._search_option_detail_wrap > ul > li.bx.term > div > div.mod_select_option.type_calendar._calendar_select_layer > div.set_calendar > span:nth-child(3) > a").click()
    # 종료일을 연, 월, 일로 나누어 리스트로 저장
    end = list(map(int, end.split('-')))
    setDate(end)

    # 적용버튼 클릭
    submitBtn = driver.find_element(By.CSS_SELECTOR,"#snb > div.mod_group_option_sort._search_option_detail_wrap > ul > li.bx.term > div > div.mod_select_option.type_calendar._calendar_select_layer > div.btn_area > button")
    submitBtn.click()
time.sleep(1)

naverNewsUrls = []      # naver기사들의 url들을 저장할 리스트
# 순서
newsCnt = int(input("스크랩할 기사의 개수를 입력하시오: "))
newsList = driver.find_element(By.CSS_SELECTOR,"#main_pack > section.sc_new.sp_nnews._fe_news_collection._prs_nws > div.api_subject_bx > div.group_news > ul")
while len(newsList.find_elements(By.TAG_NAME,"li")) < newsCnt:
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

# 1. 뉴스들이 들어있는 탭 가져오기
news_tab = driver.find_element(By.CSS_SELECTOR,"#main_pack > section.sc_new.sp_nnews._fe_news_collection._prs_nws > div.api_subject_bx > div.group_news")
# 2. 가져온 탭 내에서 각 뉴스별 url가져오기
info_group = news_tab.find_elements(By.CLASS_NAME,"info_group")
for info in info_group:
    links = info.find_elements(By.CSS_SELECTOR,"a")
    for link in links:
        url = link.get_attribute('href')
        # 3. 만약 url안에 news.naver.com이 들어있다면 리스트에 저장
        if 'news.naver.com' in url:
            naverNewsUrls.append(url)

print(naverNewsUrls)

# 4. 다 가져왔다면 리스트 내의 url을 가지고 다시 브라우저를 열기
crawled_data = {"title": [],"url":[], "date": [],"content":[], "comments":[]}
for url in naverNewsUrls:
    driver.get(url)
    title = driver.find_element(By.CSS_SELECTOR, '#title_area > span').text
    date = driver.find_element(By.CSS_SELECTOR,
                               "#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span").text
    content = driver.find_element(By.TAG_NAME, 'article').text
    content = ' '.join(content.replace('\n', ' ').split())
    total_comments_cnt = int(driver.find_element(By.CLASS_NAME, "u_cbox_count").text)
    curr_comments_cnt = int(driver.find_element(By.CLASS_NAME, "u_cbox_info_txt").text)
    comments = []
    print(title)
    print(date)
    print([content])
    print(f'총 댓글수: {total_comments_cnt}, 현재 댓글수: {curr_comments_cnt}')
    if curr_comments_cnt:
        # 댓글 더보기 버튼 클릭
        driver.find_element(By.CSS_SELECTOR,
                            "#cbox_module > div.u_cbox_wrap.u_cbox_ko.u_cbox_type_sort_favorite > div.u_cbox_view_comment > a > span.u_cbox_in_view_comment").click()
        commentsTab = driver.find_element(By.CLASS_NAME, "u_cbox_list")
        while True:
            try:
                driver.find_element(By.CLASS_NAME,"u_cbox_page_more").click()
            except:
                print('더보기 끝')
                break

        commentList = driver.find_elements(By.CLASS_NAME, "u_cbox_contents")
        for com in commentList:
            print(com.text)
            comments.append(com.text)
    # crawled_data에 title, url, date, content, comments 저장하기
        crawled_data["title"].append(title)
        crawled_data["url"].append(url)
        crawled_data["date"].append(date)
        crawled_data["content"].append(content)
        crawled_data["comments"].append('\n'.join(comments))


    # TODO:
    #  1. 열 링크,제목,날짜, 본문, 댓글들 엑셀로 저장 하기
    #  2. 저장된 엑셀 불러오기
    #  3. 불러온 댓글들에서 명사들로만 이루어진 리스트 생성하기

import pandas as pd
import datetime
index = list(range(1,len(crawled_data["title"])+1))                 # 행 번호
columns = ["title","url","date","content","comments"]               # 각 열 이름

df = pd.DataFrame(crawled_data, columns=columns)
# 엑셀 저장하기
now = datetime.datetime.now()
excelfilename = f"{now.year}_{now.month}_{now.day}_{query}.xlsx"
df.to_excel(excelfilename)

# 엑셀 불러오기
loadExcel = pd.read_excel(excelfilename)
print(loadExcel)

from konlpy.tag import Okt
okt = Okt()         # 형태소 분석기
nouns_comments = []

for commentList in list(loadExcel['comments']):
    comments = commentList.split('\n')
    nounsList = []
    for comment in comments:
        nouns = okt.nouns(comment)  # 명사만 추출
        nounsList.append(nouns)
    nouns_comments.append(nounsList)
print(nouns_comments)