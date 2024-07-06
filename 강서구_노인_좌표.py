import numpy as np
import pandas as pd

import random
from shapely.geometry import Point, Polygon

df_dong = pd.read_csv("./data/강서구_노인인구_현황.csv", encoding="cp949")

for i in range(len(df_dong)):
    # 데이터 불러오기
    dong_index = df_dong.loc[i, "동명"]
    df = pd.read_csv(f"./data/boundary/{dong_index}.csv", encoding = "cp949")
    
    
    # 동 경계 다각형 정의
    boundary_coords = np.array(df)
    boundary_polygon = Polygon(boundary_coords)
    
    
    # 난수 좌표 생성
    num_points = df_dong.loc[i, "계"]
    points = []
    
    while len(points) < num_points:
        x = random.uniform(df["경도"].min(), df["경도"].max())
        y = random.uniform(df["위도"].min(), df["위도"].max())
        point = Point(x, y)

        if boundary_polygon.contains(point):
            points.append((x, y))

    
    # 좌표 내보내기
    df_point = pd.DataFrame(columns = ["경도", "위도"], data = points)
    df_point.to_csv(f"./data/senior/{dong_index}.csv", index = False, encoding = "cp949")