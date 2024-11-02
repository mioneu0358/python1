import requests
from datetime import datetime
import json
now = datetime.now()
tm = input("조회시간을 입력하시오(YYYYMMDDHHMI): ") or now.strftime("%Y%m%d")+'0000'  #
# print(tm)
print("지점번호:  47102: 백령도,  47104: 북강릉, 47230: 덕적북리, 47122: 오산, 47138:포항, 47155: 창원, 47158: 광주, 47169: 흑산도, 47186: 국가태풍센터")
stn = input("지점번호를 입력하시오: ") or 0
pa = input("기압면을 입력하시오: ") or 0
help = input("도움말이 필요하면 1을 입력하시오: ") or 0
authKey = "td466HyuQfueOuh8rmH7Hg"
# URL과 저장 경로 변수를 지정합니다.
url = (f'https://apihub.kma.go.kr/api/typ01/url/upp_temp.php?tm={tm}&stn={stn}&pa={pa}&help'
       f'={help}&authKey={authKey}')
print(url)
response = requests.get(url).text
print(response)
# print(response)
response = response.replace('\n\n','\n').split('\n')
# print(response)
a1,a2 = response[1:3]
import pandas as pd
index = list(map(lambda x: x[0]+f'({x[1]})',zip(a1.split(), a2.split())))[1:]
# print(index)
df = pd.DataFrame(data=list(map(lambda x: x.split(), response[3:])),columns= index)
df.to_excel(f"{now.year}_{now.month}_{now.day}_TEMP.xlsx")
# 날짜: YYMMDDHHMI   지점번호:STN      등압면:PA      높이: GH      기온: TA      이슬점 온도: TD     풍향: WD     풍속: WS

# TODO: 높이를 기준으로 기온, 풍향, 풍속을 도수분포표로 표현 + 각 유형별 그래프 표현하기
# 기온은 6개 단위로(시작: 0 ~ ???, ??? ~ ????), 맨 밑의 2개의 데이터는 None
# -999에 대해 처리하기

print(list(df['GH(m)']))
counts = []
nine = 0
for data in list(df['GH(m)']):
    if data == 'None': continue
    if data == '-999.0':
        nine += 1
    elif nine:
        counts.append(nine)
        nine = 0
        counts.append(data)
print(counts)
import numpy as np
heights = [0]
for i in range(len(counts)-1):
    if type(counts[i]) == int:
        l = heights[-1]
        r = float(counts[i+1])
        temp = np.linspace(l,r,counts[i]+2)
        heights += list(map(int,temp))[1:-1]
    else:
         heights.append(int(float(counts[i])))
print(heights)

