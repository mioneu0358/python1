import requests
from bs4 import BeautifulSoup
import tkinter as tk
import webbrowser

# 뉴스 제목 최대 길이 설정
MAX_TITLE_LENGTH = 30

def fetch_news():
    """네이버 최신 IT 뉴스 5개를 가져와 리스트로 반환"""
    naver_url = "https://news.naver.com/breakingnews/section/105/230"
    naver_response = requests.get(naver_url)
    naver_soup = BeautifulSoup(naver_response.text, 'html.parser')
    naver_news_list = naver_soup.select_one(
        "#newsct > div.section_latest > div > div.section_latest_article._CONTENT_LIST._PERSIST_META > div:nth-child(1) > ul"
    )

    news_data = []
    if naver_news_list:
        title_list = naver_news_list.select("li")[:5]  # 최신 5개 기사
        for title in title_list:
            news_title = title.select_one('strong').text.strip()
            news_url = title.select_one('a').attrs['href']

            # 제목이 길면 "..." 처리
            if len(news_title) > MAX_TITLE_LENGTH:
                news_title = news_title[:MAX_TITLE_LENGTH] + "..."

            news_data.append((news_title, news_url))
    return news_data

def fetch_weather():
    """네이버에서 현재 위치와 날씨 정보를 가져와 문자열로 반환"""
    weather_url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=날씨"
    weather_res = requests.get(weather_url)
    weather_html = BeautifulSoup(weather_res.text, 'html.parser')

    curr_pos = weather_html.select_one('h2.title').text.strip()  # 현재 위치
    weather_now = weather_html.select_one(
        "#main_pack > section.sc_new.cs_weather_new._cs_weather > div > div:nth-child(1) > div.content_wrap > div.open > div:nth-child(1) > div > div.weather_info"
    )
    _, now_temp = weather_now.select_one(".weather_graphic").text.strip().split('  ')  # 현재 온도
    diff, _, _, bodytemp, tmp, wind_info = weather_now.select_one(".temperature_info").text.strip().split('  ')  # 날씨 세부정보

    return f"{curr_pos} | {now_temp}°C | {diff}\n{bodytemp} | {tmp} | {wind_info}"

def open_news(url):
    """기사 링크를 웹 브라우저에서 열기"""
    webbrowser.open(url)

def update_data():
    """뉴스와 날씨 정보를 업데이트"""
    weather_label.config(text=fetch_weather())

    for widget in news_frame.winfo_children():
        widget.destroy()  # 기존 위젯 삭제

    news_list = fetch_news()
    for title, url in news_list:
        news_item_frame = tk.Frame(news_frame, pady=2)
        news_item_frame.pack(fill="x", padx=10, pady=2)

        news_label = tk.Label(news_item_frame, text=title, fg="blue", cursor="hand2",
                              font=("Arial", 12, "underline"), anchor="w")
        news_label.pack(side="left", fill="x", expand=True)
        news_label.bind("<Button-1>", lambda e, link=url: open_news(link))

# GUI 생성
root = tk.Tk()
root.title("myTopic Widget")
root.geometry("400x300")

# 날씨 정보 표시
weather_label = tk.Label(root, text="날씨 정보를 불러오는 중...", font=("Arial", 10))
weather_label.pack(pady=5)

# 뉴스 프레임
news_frame = tk.Frame(root)
news_frame.pack(fill="both", expand=True, padx=10, pady=5)

# 새로고침 버튼
update_button = tk.Button(root, text="새로고침", command=update_data)
update_button.pack(pady=10)

# 초기 데이터 로드
update_data()

# GUI 실행
root.mainloop()
