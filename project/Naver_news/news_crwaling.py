import os
import sys

import re
# 정규 표현식 삭제(태그 지우기)
def remove_tags(text):
    clean_text = re.sub('<.*?>', '', text)
    return clean_text

import urllib.request
import json
import pandas as pd
client_id = "bU73pEDSQ6YYIuk_F_XB"      # 네이버 api 애플리케이션 ID
client_secret = "Y3isHLBcQs"            # 네이버 api 애플리케이션 Secret

keyword = input("검색할 키워드를 입력하시오: ")
encText = urllib.parse.quote(keyword)
url = "https://openapi.naver.com/v1/search/news?query=" + encText # JSON 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    response_data = response_body.decode('utf-8')
    # print(response_data)
else:
    print("Error Code:" + rescode)


result = json.loads(response_data)

date = []
title = []
links = []
descriptions = []
for items in result['items']:
        date.append(items['pubDate'])
        title.append(items['title'])
        links.append(items['originallink'])
        descriptions.append(items['description'])




# # print(date)
#
toexcel = pd.DataFrame({
        'date':date,
        'title':title,
        'link':links,
        'description': descriptions
})
toexcel.to_excel('장마.xlsx')