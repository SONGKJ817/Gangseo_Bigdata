import requests, json
import pandas as pd
import time

# data import
df_senior = pd.read_csv("./data/강서구_경로당_정보.csv", encoding='cp949')

# KAKAO API
def get_location(address):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
    headers = {"Authorization": "KakaoAK fb7d6fb86b02ac2f2cc4ba8a4394c73d"} # Rest API 키 입력
    api_json = json.loads(str(requests.get(url,headers=headers).text))
    api_json['documents'][0]['address']
    match_first = api_json['documents'][0]['address']
    return match_first['h_code'], float(match_first['x']), float(match_first['y'])

# 경로당 좌표 구하기
li_unknowned = []
li_x = []
li_y = []

for i in range(len(df_senior)):

    address = df_senior.iloc[i, 1]
    
    try:
        _, x, y = get_location(address) # 주소지 검색이 불가능한 경우
    except IndexError:
        li_unknowned.append(df_senior.iloc[i, 0])
        li_x.append(0) # x에 0을 넣기
        li_y.append(0) # y에 0을 넣기
        continue
    
    if _ == '': # 주소지가 자세하게 표시되지 않은 경우
        li_unknowned.append(df_senior.iloc[i, 0])
        li_x.append(0) # x에 0을 넣기
        li_y.append(0) # y에 0을 넣기
        continue
    else:
        li_x.append(x)
        li_y.append(y)

df_senior['x'] = li_x
df_senior['y'] = li_y

# 좌표를 찾지 못한 나머지들에 대해서는 주소를 수정하여 다시 채워 넣기
# 단지, 아파트 경로당의 경우 단지, 아파트 주소로 대체
dict_unknowned = {li_unknowned[0] : "서울 강서구 마곡중앙1로 72",
                  li_unknowned[1] : "서울 강서구 마곡서1로 131",
                  li_unknowned[2] : "error",
                  li_unknowned[3] : "서울 강서구 마곡서1로 111-11", 
                  li_unknowned[4] : "서울 강서구 마곡중앙3로 74",
                  li_unknowned[5] : "서울 강서구 마곡중앙로 36",
                  li_unknowned[6] : "서울 강서구 마곡서1로 146",
                  li_unknowned[7] : "서울 강서구 화곡로66길 186-12",
                  li_unknowned[8] : "error",
                  li_unknowned[9] : "error",
                  li_unknowned[10] : "error",
                  li_unknowned[11] : "error",
                  li_unknowned[12] : "error",
                  li_unknowned[13] : "서울 강서구 남부순환로19길 105",
                  li_unknowned[14] : "서울 강서구 화곡로44가길 52-4",
                  li_unknowned[15] : "서울 강서구 강서로74길 11",
                  li_unknowned[16] : "서울 강서구 강서로56나길 41",
                  li_unknowned[17] : "error",
                  li_unknowned[18] : "서울 강서구 공항대로 351-21 1층",
                  li_unknowned[19] : "서울 강서구 개화길 52",
                  li_unknowned[20] : "error",
                  li_unknowned[21] : "서울 강서구 화곡로63가길 18",
                  li_unknowned[22] : "error",
                  li_unknowned[23] : "서울 강서구 마곡중앙로 33 1층",
                  li_unknowned[24] : "서울 강서구 양천로55길 55",
                  li_unknowned[25] : "error",
                  li_unknowned[26] : "서울 강서구 등촌로 113",
                  li_unknowned[27] : "error",
                  li_unknowned[28] : "error",
                  li_unknowned[29] : "서울 강서구 공항대로45길 24",
                  li_unknowned[30] : "error",
                  li_unknowned[31] : "서울 강서구 강서로68길 36",
                  li_unknowned[32] : "서울 강서구 곰달래로35길 109",
                  li_unknowned[33] : "서울 강서구 양천로30길 20",
                  li_unknowned[34] : "서울 강서구 우현로 67",
                  li_unknowned[35] : "서울 강서구 마곡서로 175",
                  li_unknowned[36] : "서울 강서구 수명로2길 63",
                  li_unknowned[37] : "서울 강서구 내발산동 강서로47길 108",
                  li_unknowned[38] : "서울 강서구 수명로2가길 22",
                  li_unknowned[39] : "서울 강서구 화곡로68길 8",
                  li_unknowned[40] : "서울 강서구 양천로47길 94",
                  li_unknowned[41] : "서울 강서구 양천로53길 66",
                  li_unknowned[42] : "error",
                  li_unknowned[43] : "서울 강서구 마곡서로 133",
                  li_unknowned[44] : "error",
                  li_unknowned[45] : "서울 강서구 마곡서1로 132",
                  li_unknowned[46] : "서울 강서구 마곡서1로 100"
                 }

for key, value in dict_unknowned.items():

    address = value
    index = df_senior[df_senior["사업장명"] == key].index.tolist()[0]
    try:
        _, x, y = get_location(address) # 주소지 검색이 불가능한 경우
    except IndexError:
        df_senior.loc[index, "x"] = 0 # x에 0을 넣기
        df_senior.loc[index, "y"] = 0 # y에 0을 넣기
        continue
    
    if _ == '': # 주소지가 자세하게 표시되지 않은 경우
        df_senior.loc[index, "x"] = 0 # x에 0을 넣기
        df_senior.loc[index, "y"] = 0 # y에 0을 넣기
        continue
    else:
        df_senior.loc[index, "x"] = x
        df_senior.loc[index, "y"] = y


# export data
df_senior.to_csv("./data/강서구_경로당_좌표.csv", index = False, encoding = "cp949")        