#  프로젝트: 인구 피라미드
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = "Malgun Gothic"
matplotlib.rcParams['font.size'] = 15
matplotlib.rcParams['axes.unicode_minus'] = False   # 한글 폰스 사용시 , 마이너스 글자가 꺠지는 현상 해결

# 데이터: https://jumin.mois.go.kr/ageStatMonth.do#none  연령별 인구현황
# 조회기간: 월간 2013년 8월 ~ 2013년 8월
# 연령구분: 10세, 만           연령구분: 0 ~ 100이상

# 남자 연령별 전국 데이터 정의
df_m_2013 = pd.read_excel('201308_201308_연령별인구현황_월간.xlsx',skiprows=3, index_col='행정기관', usecols='B,R:AB')
#skiprows: 맨 위의 3행 무시, index_col: 사용할 column값 설정, usecols, 사용할 행 정의

# columns값을 확인해보면 .1이 붙어 있으므로 수정
new_columns = []
for col in df_m_2013.columns:
    new_columns.append(col[:-2])
df_m_2013.columns = new_columns

# 데이터 타입을 정수로 변경하는 과정 1,741.601 => 1741601
df_m_2013.iloc[0] = df_m_2013.iloc[0].str.replace(',','').astype(int)


# 여자 연령별 전국 데이터 정의
df_w_2013 = pd.read_excel('201308_201308_연령별인구현황_월간.xlsx',skiprows=3, index_col='행정기관', usecols='B,AE:AO')
df_w_2013.columns = df_m_2013.columns

df_w_2013.iloc[0] = df_w_2013.iloc[0].str.replace(',','').astype(int)


# 데이터 시각화
plt.figure(figsize=(10,6))     # 창 비율 
plt.title("2013 대한민국 인구 피라미드")
plt.barh(df_m_2013.columns,-df_m_2013.iloc[0] // 1000)      # barh(column, 데이터): 가로 막대, 데이터 // 1000 이므로 단위는 1천명 단위 
plt.barh(df_m_2013.columns,df_w_2013.iloc[0] // 1000)
plt.savefig('2013 대한민국 인구 피라미드.png', dpi = 100)    # 이미지 파일로 저장, dpi: 해상도
plt.show()
