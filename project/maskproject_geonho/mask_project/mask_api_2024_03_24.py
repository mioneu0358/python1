import requests
import json

serviceKey = "msYRhJ6JOgdasigGM0PhgnBk3Cgm2oqEwEw90bD4dD9hqTzqMYU8w27FFzW59HzhWPFIuMUwGzA7pRJjqYgMBQ=="


# 미세먼지 초 미세먼지 데이터를 가져올 함수
def get_pm(area):
    convert_area = {'서울': 'seoul', '부산': 'busan', '대구': 'daegu', '인천': 'incheon',
                   '광주': 'gwangju', '대전': 'daejeon', '울산': 'ulsan', '경기': "gyeonggi",
                   '강원': 'gangwon', '충북': 'chungbuk', '충남': 'chungnam', '전북': 'jeonbuk',
                   '전남': 'jeonnam', '경북': 'gyeongbuk', '경남': 'gyeongnam', '제주': 'jeju'}
    area = convert_area[area]
    pm_data = []
    url = 'http://apis.data.go.kr/B552584/ArpltnStatsSvc/getCtprvnMesureLIst'

    for itemcode in ["PM10", "PM25"]:
        params = {'serviceKey': serviceKey, 'returnType': 'json', 'numOfRows': '1', 'pageNo': '1', 'itemCode': itemcode,
                  'dataGubun': 'HOUR', 'searchCondition': 'WEEK',}

        response = requests.get(url, params=params).text
        result = json.loads(response)
        print(result)
        parsing = result['response']['body']['items'][0]  # 1시간 전의 데이터
        pm_data.append(int(parsing[area]))

    return pm_data

# 질병 위험도 데이터를 가져올 함수
def get_disease(area):
    url = 'http://apis.data.go.kr/B550928/dissForecastInfoSvc/getDissForecastInfo'
    convert_area = {'서울': '11', '부산': '26', '대구': '27', '인천': '28',
                    '광주': '29', '대전': '30', '울산': '31', '경기': '41',
                    '강원': '42', '충북': '43', '충남': '44', '전북': '45',
                    '전남': '46', '경북': '47', '경남': '48', '제주': '49'}
    area = convert_area[area]
    params = {'serviceKey': serviceKey, 'numOfRows': '10', 'pageNo': '1', 'type': 'json',
              'dissCd': '1', 'znCd': area}
    response = requests.get(url, params=params).text
    result = json.loads(response)
    disease_data = result['response']['body']['items'][0]['risk']

    return disease_data

if __name__ == "__main__":
    print(get_pm("경기"))
    get_disease('경기')