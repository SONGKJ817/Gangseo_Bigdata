import pandas as pd

# 데이터 불러오기
df = pd.read_csv("./data/서울시_경로당_정보.csv", encoding='cp949')

# 소재지전체주소에 "강서구"가 포함되지 않은 데이터 제거
df = df[df['소재지전체주소'].str.contains('강서구')]

# 영업상태명이 운영중이 아닌 데이터 제거
df = df[df['영업상태명'] == '운영중']

# 사업장명, 소재지전체주소 데이터만 추출
df = df[['사업장명', '소재지전체주소']]

df.reset_index(drop = True, inplace = True)
print(f"강서구 총 경로당 수 : {len(df)}")

df.to_csv("./data/강서구_경로당_정보.csv", encoding='cp949', index = False)