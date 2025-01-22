#
import requests
from bs4 import BeautifulSoup
# TODO: myTopic widget

# naver뉴스 IT/과학 파트 최신 6개
naver_url = "https://news.naver.com/breakingnews/section/105/230"
naver_response = requests.get(naver_url)
# print(naver_response.status_code)

naver_soup = BeautifulSoup(naver_response.text, 'html.parser')
# print(naver_soup)
naver_news_list = naver_soup.select_one("#newsct > div.section_latest > div > div.section_latest_article._CONTENT_LIST._PERSIST_META > div:nth-child(1) > ul")
# print(naver_news_list)
title_list = naver_news_list.select("li")
# print(naver_news_list.text.replace('\n\n',''))
for title in title_list:
    print(title.select_one('strong').text)
    print(title.select_one('a').attrs['href'])
