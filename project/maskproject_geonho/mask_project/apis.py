import requests
# import xmltodict
import json
import datetime
import time


def get_api():
    # 한국환경공단_에어코리아_대기오염통계 현황
    # https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15073855#tab_layer_detail_function
    serviceKey = "msYRhJ6JOgdasigGM0PhgnBk3Cgm2oqEwEw90bD4dD9hqTzqMYU8w27FFzW59HzhWPFIuMUwGzA7pRJjqYgMBQ=="
    url = 'http://apis.data.go.kr/B552584/ArpltnStatsSvc/getCtprvnMesureLIst'
    #
    # # -------------------------------------------- 미세먼지(pm10) 데이터 불러오기 ---------------------------------------------------
    pm10_params = {'serviceKey': serviceKey, 'returnType': 'json', 'numOfRows': '100', 'pageNo': '1',
                   'itemCode': 'PM10', 'dataGubun': 'HOUR', 'searchCondition': 'WEEK'}
    pm10_response = requests.get(url, params=pm10_params).content
    pm10_result = json.loads(pm10_response)
    least = pm10_result['response']['body']['items'][0]  # 1시간 전의 데이터
    pm10_gyeonggi = least['gyeonggi']  # 경기도 미세먼지 농도
    pm10_incheon = least['incheon']  # 인천 미세먼지 농도
    pm10_avg = (int(pm10_incheon) + int(pm10_gyeonggi)) / 2

    # # ------------------------------------------- 초 미세먼지(pm2.5) 데이터 불러오기 -------------------------------------------------
    pm25_params = {'serviceKey': serviceKey, 'returnType': 'json', 'numOfRows': '100', 'pageNo': '1',
                   'itemCode': 'PM25', 'dataGubun': 'HOUR', 'searchCondition': 'WEEK'}
    rs = requests.session()
    rs.mount('http://', requests.adapters.HTTPAdapter(pool_connections=3, pool_maxsize=10, max_retries=3))
    rs.headers = {'Content-Type': 'application/json'}
    pm25_response = rs.get(url, params=pm25_params).content
    # pm25_response = requests.get(url, params=pm25_params).content
    pm25_result = json.loads(pm25_response)
    least = pm25_result['response']['body']['items'][0]  # 1시간 전의 데이터
    pm25_gyeonggi = least['gyeonggi']  # 경기도 미세먼지 농도
    pm25_incheon = least['incheon']  # 인천 미세먼지 농도
    pm25_avg = (int(pm25_incheon) + int(pm25_gyeonggi)) / 2

    return pm10_avg, pm25_avg
    #

    # ------------------------------------------- 코로나 발생 현황 -------------------------------------------------
    # covid_url = 'http://apis.data.go.kr/1352000/ODMS_COVID_04/callCovid04Api'
    # covid_serviceKey = "msYRhJ6JOgdasigGM0PhgnBk3Cgm2oqEwEw90bD4dD9hqTzqMYU8w27FFzW59HzhWPFIuMUwGzA7pRJjqYgMBQ=="
    # today = str(datetime.datetime.today()).split()[0]
    # # print(today,type(today))
    # covid_params ={'serviceKey': covid_serviceKey,
    #                'pageNo' : '2',
    #                'numOfRows' : '500',
    #                "std_day" : "2023-09-01"}
    #
    # covid_response = requests.get(covid_url, params=covid_params).content
    # print(covid_response)
    # jsonString = json.loads(json.dumps(xmltodict.parse(covid_response)))
    # # covid_result = jsonString["response"]["body"]["item"][0]
    # # print(covid_result)
    # print(jsonString)
    # -------------------------------------------------- 이미지 투명도 기준 ---------------------------------------------------------------------------
    # pm10(미세먼지) 수치별 기준: 0 ~ 80: 좋음, 80~150: 약간 나쁨,  150~ 300: 주의보(나쁨), 300~: 경보(매우 나쁨)
    # pm2.5(초미세먼지) 수치별 기준:0~ 40: 좋음, 40~ 75: 약간 나쁨,  75~150: 주의보(나쁨),  150~ 경보(매우나쁨)
    # 코로나 수치별 기준:    좋음, 약간 나쁨, 나쁨, 매우 나쁨
    # pm10_avg = (pm10_incheon + pm25_gyeonggi) / 2
    # pm20_avg = (pm25_incheon + pm25_gyeonggi) / 2
    # covid_avg = (covid_incheon + covid_gyeonggi)/2
    # total_avg = (pm10_avg + pm20_avg + covid_avg) // 3

    # img_path = f"mask_{total_avg}.png"


if __name__ == "__main__":
    pm10_avg,pm25_avg = get_api()
    # (인천 미세먼지 + 경기 미세먼지) / 2 => 평균 미세먼지
    print(f"pm10_avg = {pm10_avg}")
    # (인천 초미세먼지+ 경기 초미세먼지)/2 => 평균 초미세먼지
    print(f"pm25_avg = {pm25_avg}")