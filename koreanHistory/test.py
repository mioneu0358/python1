import requests
from bs4 import BeautifulSoup
import json

king = '태조'
content = '조물군 전투'
def get_first_result_link(query):
    base_url = 'https://encykorea.aks.ac.kr/Article/Search/'+ query
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    first_result = soup.find('ul',class_ = "encyclopedia-list").find('a')['href']
    if first_result:
        return "https://encykorea.aks.ac.kr/" + first_result
    # .find('a')['href']

    return first_result


# 사용 예시
search_query = '태조 조선 전통'
first_result_link = get_first_result_link(f"{king} {content}")
# print("First result link:", first_result_link)
