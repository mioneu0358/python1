"""
날씨 앱 제작 과정
1. 사용할 gui 정의 :  tkinter, pyqt5
2. 앱에 사용할 data 가져오기: api 사용
3. 데이터와 앱을 연결하기
"""

# 지표별 단계
# 미세먼지: 0~30(좋음), 31~80(보통), 81~150(나쁨), 150~(매우나쁨)
# 자외선: ~2(낮음),3~5(보통),6~7(높음),8~10(매우높음),11~(위험)
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
UV_apiKey = os.getenv("UV_API_KEY")
params = {
    'tm': "202504050000",
    'stn': 0,
    "authKey" : UV_apiKey
}
UV_url = "https://apihub.kma.go.kr/api/typ01/url/kma_sfctm_uv.php"
UV_response = requests.get(UV_url,params=params)

# ------- 미세먼지 데이터 ---------------------------------


PM_apiKey = os.getenv("PM_API_KEY")
PM_url = 'http://apis.data.go.kr/B552584/ArpltnStatsSvc/getCtprvnMesureLIst'
params ={'serviceKey' : PM_apiKey, 'returnType' : 'json', 'itemCode' : 'PM10', 'dataGubun' : 'HOUR', 'searchCondition' : 'WEEK' }

response = requests.get(PM_url, params=params).content
PM_jsondata = json.loads(response)  # json => dict
# print(PM_jsondata)

print(PM_jsondata['response']['body']['items'][0]['gyeonggi'])  # 1시간 전의 경기도 데이터
