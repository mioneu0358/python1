import requests
from datetime import datetime
import pandas as pd
import numpy as np
from math import isnan

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
index = list(map(lambda x: x[0]+f'({x[1]})',zip(a1.split(), a2.split())))[1:]
# print(index)
df = pd.DataFrame(data=list(map(lambda x: x.split(), response[3:])),columns= index)
df.to_excel(f"{now.year}_{now.month}_{now.day}_TEMP.xlsx")
# 날짜: YYMMDDHHMI   지점번호:STN      등압면:PA      높이: GH      기온: TA      이슬점 온도: TD     풍향: WD     풍속: WS


import pandas as pd
import numpy as np
from math import isnan

pd.set_option('display.max_rows', None)

standard = ['GH(m)', 'TA(C)', 'WD(degree)', 'WS(m/s)']  # 높이, 기온, 풍향, 풍속
# print(standard)
parse_df = df.loc[ : ,standard]

for key in parse_df:
# 높이 가정치 구하기
    new_values = [0]                   # 높이 가정치
    nine = 0
    for val in parse_df[key]:
        if val == None or isnan(float(val)): continue
        if val == '-999.0':
            nine += 1
        else:
            last = new_values[-1]
            s = np.linspace(last, float(val),nine + 2)
            new_values += list(map(int,s))[1:-1]
            nine = 0
            new_values.append(float(val))

    #  가정치 대입
    for i in range(len(new_values)-1):
        parse_df.loc[i, key] = new_values[i+1]
# print(parse_df)

row = len(parse_df)         # 마지막 행 번호

# 불필요한 부분(끝 값이 -999.0이거나, NaN인 경우) 제외
while row > 0:
    row -= 1
    if list(map(lambda x: x is None or x == '-999.0' or isnan(x) , parse_df.loc[row])).count(True) == 0:
        break

parse_df = parse_df.loc[:row, :]
print(parse_df)
#
# 'GH(m)' 열의 실제 값에 기반하여 데이터의 범위를 6개의 구간으로 나누고,
# 각 구간에 대해 'TA(C)', 'WD(degree)', 'WS(m/s)'의 평균값을 구하는 코드

# 1. 'GH(m)' 열의 값에 따른 0, 20%, 40%, 60%, 80%, 100% 분위수를 계산하여 구간 경계를 정합니다.
quantiles = [0] + list(np.quantile(parse_df['GH(m)'].dropna(), [0, 0.2, 0.4, 0.6, 0.8, 1]))

# 2. 각 구간을 (하한, 상한) 형태로 저장하여 구간 리스트를 만듭니다.
range_intervals = [(quantiles[i], quantiles[i + 1]) for i in range(len(quantiles) - 1)]
# print(range_intervals)
results_quantile_based = []

# 3. 각 구간별로 'TA(C)', 'WD(degree)', 'WS(m/s)'의 평균을 계산합니다.
for lower, upper in range_intervals:
    # 'GH(m)' 값이 해당 구간에 속하는 데이터만 선택
    range_df = parse_df[(parse_df['GH(m)'] > lower) & (parse_df['GH(m)'] <= upper)]
    ta_mean = range_df['TA(C)'].mean()  # 선택된 구간 내 기온(TA(C))의 평균값
    wd_mean = range_df['WD(degree)'].mean()  # 선택된 구간 내 풍향(WD(degree))의 평균값
    ws_mean = range_df['WS(m/s)'].mean()  # 선택된 구간 내 풍속(WS(m/s))의 평균값

    # 결과를 리스트에 저장
    results_quantile_based.append({
        'Height Range (GH(m))': f"{lower:.1f} - {upper:.1f}",  # 구간 표시
        'Mean TA(C)': ta_mean,  # 해당 구간 내 기온 평균
        'Mean WD(degree)': wd_mean,  # 해당 구간 내 풍향 평균
        'Mean WS(m/s)': ws_mean  # 해당 구간 내 풍속 평균
    })


# 완성된 도수분포표
quantile_distribution_df = pd.DataFrame(results_quantile_based)
print(quantile_distribution_df)

from matplotlib import pyplot as plt

quantile_distribution_df.plot(kind='line')
plt.show()
