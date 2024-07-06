import pandas as pd
import numpy as np

import re

import geopandas as gpd
from geopandas import GeoDataFrame

import pyproj
import folium

# data import
cen_str_df = gpd.read_file('./data/dong.jeojson.geojson',driver='GeoJSON')
senior_df = pd.read_csv("./data/강서구_노인인구_현황.csv", encoding = 'cp949')
dong = list(senior_df["동명"])

# dong 리스트 안에 있는 행만 뽑아내기
df = cen_str_df[cen_str_df["ADM_NM"].isin(dong)].reset_index(drop=True)

# 가양1동과 가양2동이 각각 2개 -> 대전 동구에 가양 1동과 2동이 존재
# 모양 확인 후 제거
df.drop([0, 21], inplace = True)
df.reset_index(drop = True, inplace = True)

# 좌표 생성
polygons = list(df["geometry"])
li_coordinates = []

for i in range(len(polygons)):
    data = str(polygons[i]).replace("MULTIPOLYGON (((", "").replace(")))", "").split(",")
    li_coordinates.append([list(map(float, item.split())) for item in data])
    
df["coordinates"] = li_coordinates

# 좌표계 변환
def project_array(coord, p1_type, p2_type):
    """
    좌표계 변환 함수
    - coord: x, y 좌표 정보가 담긴 NumPy Array
    - p1_type: 입력 좌표계 정보 ex) epsg:5179
    - p2_type: 출력 좌표계 정보 ex) epsg:4326
    """
    p1 = pyproj.Proj(init=p1_type)
    p2 = pyproj.Proj(init=p2_type)
    fx, fy = pyproj.transform(p1, p2, coord[:, 0], coord[:, 1])
    return np.dstack([fx, fy])[0]

p1_type = "epsg:5186"
p2_type = "epsg:4326"

coord_4326 = []

for i in range(len(df)):
    coord = np.array(df.loc[i,'coordinates'])
    result = project_array(coord, p1_type, p2_type)
    coord_4326.append(result)
    
df["coord_4326"] = coord_4326

df.drop("coordinates", axis = 1, inplace = True)
df.drop("geometry", axis = 1, inplace = True)

# data export
for i in range(len(df)):
    dong_df = pd.DataFrame(columns = ["경도", "위도"], data = df["coord_4326"][i])
    dong_index = df["ADM_NM"][i]
    dong_df.to_csv(f"./data/boundary/{dong_index}.csv", index = False, encoding = "cp949")