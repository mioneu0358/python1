import requests
import json

def get_masknum():
    serviceKey = "msYRhJ6JOgdasigGM0PhgnBk3Cgm2oqEwEw90bD4dD9hqTzqMYU8w27FFzW59HzhWPFIuMUwGzA7pRJjqYgMBQ=="
    url = 'http://apis.data.go.kr/B552584/ArpltnStatsSvc/getCtprvnMesureLIst'
    pm10_params ={'serviceKey' : serviceKey, 'returnType' : 'json', 'numOfRows' : '100', 'pageNo' : '1', 'itemCode' : 'PM10', 'dataGubun' : 'HOUR', 'searchCondition' : 'MONTH' }

    pm10_response = requests.get(url, params=pm10_params).content
    pm10_result = json.loads(pm10_response)

    pm10_incheon = pm10_result['response']['body']['items'][0]['incheon']
    pm10_geyonggi = pm10_result['response']['body']['items'][0]['gyeonggi']
    pm10_avg = (int(pm10_incheon) + int(pm10_geyonggi)) / 2
    print(f"미세먼지 인천: {pm10_incheon}, 경기:{pm10_geyonggi}, 평균: {pm10_avg}")

    pm25_params ={'serviceKey' : serviceKey, 'returnType' : 'json', 'numOfRows' : '100', 'pageNo' : '1', 'itemCode' : 'PM25', 'dataGubun' : 'HOUR', 'searchCondition' : 'MONTH' }
    pm25_response = requests.get(url, params=pm25_params).content
    pm25_result = json.loads(pm25_response)

    pm25_incheon = pm25_result['response']['body']['items'][0]['incheon']
    pm25_geyonggi = pm25_result['response']['body']['items'][0]['gyeonggi']
    pm25_avg = (int(pm25_incheon) + int(pm25_geyonggi)) / 2
    print(f"초미세먼지 인천: {pm25_incheon}, 경기:{pm25_geyonggi}, 평균: {pm25_avg}")


    # 미세먼지 기준: 0-30:좋음(1단계), 31-80:보통(2단계), 81-150:나쁨(3단계), 151이상:매우나쁨(4단계)
    # 초미세먼지 기준: 0-15: 좋음(1단계), 16~35: 보통(2단계), 36-75:나쁨(3단계), 76이상: 매우나쁨(4단계)


    return

if __name__ == "__main__":
    get_masknum()
