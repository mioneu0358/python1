# 소스: https://wonhwa.tistory.com/m/52
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
from tqdm import tqdm


# 크롤링할 url 생성하는 함수 만들기(검색어, 크롤링 종료 페이지)

def makeUrl(search, end_pg):
    urls = []
    for i in range(1, end_pg + 1):
        url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query=" + search + "&start=%20" + str(i)
        urls.append(url)
    return urls

    # html에서 원하는 속성 추출하는 함수 만들기 (기사, 추출하려는 속성값)

def news_attrs_crawler(articles, attrs):
    attrs_content = []
    for i in articles:
        attrs_content.append(i.attrs[attrs])
    return attrs_content

# ConnectionError방지
# 웹 사이트나 서버는 사용자 에이전트를 통해 클라이언트의 정보를 확인하고 적절한 응답을 제공합니다.
# 하지만 때로는 웹 사이트 또는 서버에서 특정 에이전트를 차단하거나 허용하지 않는 경우가 있습니다. 이러한 경우, connectionerror가 발생할 수 있습니다.
# 그러므로 만일 차단당하더라도 클라이언트 정보가 아닌 임의의 값을 넘긴것이므로 우회가 가능해진다.
# User-Agent: Mozilla 정보/버전 + 운영체제 정보 + 렌더링 엔진 정보 + 브라우저
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}


# html을 생성후 기사를 크롤링해줄 함수(url): => link
def articles_crawler(url):
    # html 불러오기
    # requests.get(url) => response
    # 반환된 response객채의 주요 속성
    # status_code: HTTP 응답 상태 코드를 나타내는 정수 값입니다. 예를 들어, 200은 "성공"을 나타냅니다.
    # text: 응답 내용을 나타내는 문자열입니다. 일반적으로 HTML, XML, JSON 등과 같은 형식의 텍스트 데이터가 포함됩니다.
    # content: 응답 내용을 나타내는 bytes 객체입니다. 이를 통해 바이너리 데이터를 다운로드할 수도 있습니다.
    # json(): 응답 내용을 JSON 형식으로 파싱하여 반환하는 메서드입니다.
    original_html = requests.get(url, headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")

    url_naver = html.select(
        "div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
    url = news_attrs_crawler(url_naver, 'href')
    return url