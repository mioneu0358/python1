import requests
from bs4 import BeautifulSoup
import re
def get_korean_dynasty():
    url = "https://terms.naver.com/entry.naver?docId=6647597&cid=40942&categoryId=33382"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # 표의 데이터를 저장할 딕셔너리 초기화
        korean_dynasty_dict = {}

        # 표의 tbody 태그를 찾음
        tbody = soup.find('tbody')

        # 표의 각 행(row)을 찾음
        rows = tbody.find_all('tr')

        for row in rows:
            # 각 행에서 데이터 추출
            columns = row.find_all('td')

            # 데이터 추출이 가능한 행인지 확인
            if len(columns) == 3:
                # 각 열에서 텍스트 추출
                king_name = columns[1].get_text(strip=False)  # 왕 이름은 테이블 2번째 열
                year_text = columns[2].get_text(strip=False)  # 연도 및 사건 내용은 테이블 3번째 열
                if "왕명" in king_name: continue
                try:
                    king_name = king_name.replace('\n','').replace('\t','').replace('\xa0',' ')
                    for yt in year_text.strip().split('.'):
                        yt = yt.replace('\n', '').replace('\t','')
                        if not yt: continue
                        year = int(yt[2: yt.index('(')].replace('년',''))
                        event = yt[yt.index(')')+1: ].strip().replace('\t','').replace('\xa0',' ')
                        # 딕셔너리에 데이터 추가
                        if king_name in korean_dynasty_dict:
                            korean_dynasty_dict[king_name].append([year,event])
                        else:
                            korean_dynasty_dict[king_name] = [[year,event]]
                except ValueError:
                    continue
        return korean_dynasty_dict
    else:
        print("Failed to retrieve the webpage.")
        return None


def get_first_result_link(query):
    base_url = 'https://encykorea.aks.ac.kr/Article/Search/'+ query
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    url_list = soup.find('ul',class_ = "encyclopedia-list")
    # print(f"url_list: {url_list}, length: {len(url_list)}")
    if len(url_list) > 1:
        first_result = url_list.find('a')['href']
        # print(first_result)
        if first_result:
            return "https://encykorea.aks.ac.kr" + first_result
        else:
            return ''

# 결과 출력
if __name__ == "__main__":
    korean_dynasty_data = get_korean_dynasty()
    # print(korean_dynasty_data)
    for king, values in korean_dynasty_data.items():
        # print(king)
        for year,content in values:
            if '연호' in content: continue
            print(f"{king} {content}")
            link = get_first_result_link(f"{king[:king.index('(')]} {content}")
            # TODO: 0. 검색 키워드에서 빼야할것들(폐지, 재개, 설치, 주조, 개편 ....)
            # TODO: 1. 검색 방식 변경(구글검색-> 한국민족문화대백과사전페이지검색내용 확인)
            # TODO: 2. 내용이 없으면 해당 왕의 정보사용.

            print(link)

