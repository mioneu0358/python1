import pandas as pd

# Sample DataFrames for demonstration
# Creating a DataFrame similar to 'airquality' in the example
data = {
    'Month': [5, 5, 6, 6, 7, 7],
    'Temp': [72, 75, 78, 85, 88, 90],
    'Wind': [7.4, 8.0, 7.1, 6.9, 8.7, 7.3]
}
df = pd.DataFrame(data)

data1 = {
    'key': ['a', 'b', 'c'],
    'val1': [1, 2, 3]
}
data2 = {
    'key': ['a', 'b', 'd'],
    'val2': ['X', 'Y', 'Z']
}
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)

# Display sample data
# print(df)
# print(df1)
# print(df2)

# # 데이터 정렬
# print(df.sort_values(by='Temp'))
#
# # 조건에 맞는 행 선택
# print(df[df['Temp'] > 80])
#
# # 특정 열 선택
# print(df[['Temp', 'Wind']])
#
# # 새 열 추가
df['TempC'] = (df['Temp'] - 32) / 1.8
print(df)
#
# # 요약 통계
mean_temp = df['Temp'].mean()
print(mean_temp)
#
# # 그룹별 요약 통계
print(df.groupby('Month')['Temp'].mean().reset_index())
#
# # Temp열의 중복된 값을 제외한 나머지 값들로만
print(df['Temp'].drop_duplicates())
#
# # 특정 행 추가
# print(df.iloc[0:3])
#
# # 샘플 추가
print(df.sample(frac=0.5))
#
# # 열 방향으로 병합
print(pd.concat([df1, df2], axis=1))
#
# # inner 조인: key 열을 기준으로
# print(pd.merge(df1, df2, on='key', how='inner'))
#
