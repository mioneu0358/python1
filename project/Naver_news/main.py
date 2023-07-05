#####뉴스크롤링 시작#####
from functions import *
# 검색어 입력
search = input("검색할 키워드를 입력해주세요: ")

# 검색 종료할 페이지 입력
end_page = int(input("몇 페이지까지 찾아볼까요(숫자만입력):"))  # ex)1 =1페이지,2=2페이지...

# naver url 생성
url = makeUrl(search, end_page)

# 뉴스 크롤러 실행
news_titles = []
news_url = []
news_contents = []
news_dates = []
for i in url:
    url = articles_crawler(i)
    news_url.append(url)


# 제목, 링크, 내용 1차원 리스트로 꺼내는 함수 생성
def makeList(newlist, content):
    for i in content:
        for j in i:
            newlist.append(j)
    return newlist

# 제목, 링크, 내용 담을 리스트 생성
news_url_1 = []

# 1차원 리스트로 만들기(내용 제외)
makeList(news_url_1, news_url)

# NAVER 뉴스만 남기기
final_urls = []
# for i in tqdm(_iterable, ): iterable한 객체의 크기가 100%로 보았을때
#                           보고 있는 값이 전체의 몇 퍼센트인지를 상태 창으로 보여주는 역할
for i in range(len(news_url_1)):
    if "news.naver.com" in news_url_1[i]:
        final_urls.append(news_url_1[i])

# 뉴스 내용 크롤링

for i in tqdm(final_urls,desc="기사 분류하는중: " ):
    # 각 기사 html get하기
    news = requests.get(i, headers=headers)
    news_html = BeautifulSoup(news.text, "html.parser")

    # 뉴스 제목 가져오기
    title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
    if title == None:
        title = news_html.select_one("#content > div.end_ct > div > h2")

    # 뉴스 본문 가져오기
    content = news_html.select("div#dic_area")
    if content == []:
        content = news_html.select("#articeBody")

    # 기사 텍스트만 가져오기
    # list합치기
    content = ''.join(str(content))

    # html태그제거 및 텍스트 다듬기
    pattern1 = '<[^>]*>'
    # re.sub（정규 표현식, 치환 문자, 대상 문자열）
    title = re.sub(pattern=pattern1, repl='', string=str(title))
    content = re.sub(pattern=pattern1, repl='', string=content)
    # pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
    # content = content.replace(pattern2, '')
    news_titles.append(title)
    news_contents.append(content)

    # 날짜 가져오기
    try:
        html_date = news_html.select_one(
            "div#ct> div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
        news_date = html_date.attrs['data-date-time']
    except AttributeError:
        news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
        news_date = re.sub(pattern=pattern1, repl='', string=str(news_date))
    news_dates.append(news_date)


###데이터 프레임으로 만들기###
import pandas as pd

# 데이터 프레임 만들기
news_df = pd.DataFrame({'date': news_dates, 'title': news_titles, 'link': final_urls, 'content': news_contents})

# 데이터 프레임 저장
now = datetime.now()
news_df.to_excel('{}_{}.xlsx'.format(search, now.strftime('%Y%m%d')))