import pandas as pd
import random
from numpy import isnan
# 한국어 DB에사용할 사이트  https://krdict.korean.go.kr/kor/mainAction

pd.set_option('display.max_columns', None)
# 엑셀 파일 읽기
file_path = "20241112_korean_1.xls"  # 엑셀 파일 경로
sheet_name = "Sheet0"  # 시트 이름 (필요 시 수정)

# 데이터프레임으로 엑셀 읽기
df = pd.read_excel(file_path, sheet_name=sheet_name)
# print(df)
# 특정 열에서 '명사'라는 단어로 필터링 (예: '열 이름'이 'Type'이라고 가정)
filtered_df = df[df['품사'].str.contains('명사', na=False)]
filtered_df = filtered_df.loc[:,['표제어',"뜻풀이"]].dropna()
# 결과 출력
# print(filtered_df)

korean_db = []
while len(korean_db) < 10:
    random_word = filtered_df.iloc[random.randint(0,len(filtered_df))]

    korean_db.append(dict(random_word))
print(korean_db)