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
                king_name = columns[1].get_text(strip=True)  # 왕 이름은 테이블 2번째 열
                year_text = columns[2].get_text(strip=True)  # 연도 및 사건 내용은 테이블 3번째 열
                if "왕명" in king_name: continue
                try:
                    for yt in year_text.strip().split('.'):
                        if not yt: continue

                        year = int(yt[2: yt.index('(')].replace('년',''))
                        event = yt[yt.index(')')+1: ]
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


# 결과 출력
if __name__ == "__main__":
    korean_dynasty_data = get_korean_dynasty()
    print(korean_dynasty_data)
    for king, values in korean_dynasty_data.items():
        print(king)
        print(values)



# if korean_dynasty_data:
#     for king, events in korean_dynasty_data.items():
#         print(f"왕 이름: {king}")
#         for event in events:
#             print(f"연도: {event['year']}")
#             print(f"사건 내용: {event['event']}")
#         print()
