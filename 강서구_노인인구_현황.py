import pandas as pd
import numpy as np

import requests
from bs4 import BeautifulSoup

import re

import warnings
warnings.filterwarnings("ignore")

# 데이터 주소
url = "https://www.gangseo.seoul.kr/welfare/wel030101#none"

response = requests.get(url, verify=False) # SSLCertVerificationError 해결

rating_page = response.text

soup = BeautifulSoup(rating_page, 'html.parser')

column_name = []
for tag in soup.select("table th"):
    column_name.append(tag.get_text())

column_name.remove("노인 인구수")
column_name.remove("강서구 인구수")

data = []
for tag in soup.select("table td"):
    data.append(tag.get_text())

data = [data[i:i+6] for i in range(0, len(data), 6)]

df = pd.DataFrame(columns = column_name, data = data)

df.drop("노인인구비율", axis = 1, inplace = True)

for column in df.columns:
    df[column] = df[column].str.replace(",", "")
    
df.iloc[:, 1:] = df.iloc[:, 1:].astype(int)

df.drop(0, inplace = True)

df['동명'] = df['동명'].str.replace("제", "")

# data export
df.to_csv("./data/강서구_노인인구_현황.csv", encoding='cp949', index = False)