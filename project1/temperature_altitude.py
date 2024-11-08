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
import numpy as np
from math import isnan
pd.set_option('display.max_rows', None)

standard = ['GH(m)', 'TA(C)', 'WD(degree)', 'WS(m/s)']  # 높이, 기온, 풍향, 풍속
# print(standard)
parse_df = df.loc[:,standard]

for key in parse_df:
# 높이 가정치 구하기
    new_values = [0]                   # 높이 가정치
    nine = 0
    for val in parse_df[key]:
        if val == None or isnan(val): continue
        if val == -999.0:
            nine += 1
        else:
            last = new_values[-1]
            s = np.linspace(last, val,nine + 2)
            new_values += list(map(int,s))[1:-1]
            nine = 0
            new_values.append(val)

    #  가정치 대입
    for i in range(len(new_values)-1):
        parse_df.loc[i, key] = new_values[i+1]
# print(parse_df)

row = len(parse_df)         # 마지막 행 번호

# 불필요한 부분(끝 값이 -999.0이거나, NaN인 경우) 제외
while row > 0:
    row -= 1
    if list(map(lambda x: isnan(x) or x == -999.0, parse_df.loc[row])).count(True) == 0:
        break

parse_df = parse_df.loc[:row, :]
print(parse_df)

print(list(parse_df.loc[:,"WD(degree)"]))

