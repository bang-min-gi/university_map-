import folium
import requests
import pandas as pd
import os
import urllib3

# SSL 경고 무시 (테스트용)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# VWorld API 키 설정 (2D 지도 API)
API_KEY = "YOUR_ACTUAL_VWORLD_API_KEY"  # VWorld API에서 발급받은 실제 API 키 입력

# 파일 경로 설정
file_path = '/mnt/data/고등교육기관 하반기 주소록(2024).xlsx'

# 저장 경로 확인 및 생성
output_dir = '/mnt/data'
output_path = os.path.join(output_dir, "university_map_vworld.html")

# Excel 파일에서 데이터 읽기 (5번째 행을 열 이름으로 지정)
df = pd.read_excel(file_path, sheet_name=0, header=4)

# 주소와 학교명 열 지정
address_column = 'Unnamed: 10'  # 주소 열
university_column = 'Unnamed: 4'  # 학교명 열

# VWorld API를 사용하여 주소를 좌표로 변환하는 함수
def get_coordinates_vworld(address):
    url = "https://api.vworld.kr/req/address"
    params = {
        "service": "address",
        "request": "getcoord",
        "version": "2.0",
        "crs": "epsg:4326",
        "address": address,
        "format": "json",
        "type": "road",
        "key": API_KEY
    }
    
    response = requests.get(url, params=params, verify=False)
    data = response.json()
    
    if data['response']['status'] == 'OK' and len(data['response']['result']) > 0:
        x = data['response']['result'][0]['point']['x']
        y = data['response']['result'][0]['point']['y']
        return y, x
    else:
        return None, None

# 좌표 변환 결과 저장 리스트
coordinates = []
failed_addresses = []

for index, row in df.iterrows():
    address = row[address_column]
    university = row[university_column]
    
    # 주소 또는 학교명이 비어있는 경우 스킵
    if pd.isna(address) or pd.isna(university) or address == "주소":
        continue

    lat, lon = get_coordinates_vworld(address)
    if lat is not None and lon is not None:
        coordinates.append((university, address, lat, lon))
    else:
        failed_addresses.append(address)

# 좌표 변환 결과를 DataFrame으로 저장
coordinates_df = pd.DataFrame(coordinates, columns=['University', 'Address', 'Latitude', 'Longitude'])
print("\n좌표 변환 완료: 변환된 좌표 수:", len(coordinates_df))
print("좌표 변환 실패한 주소 수:", len(failed_addresses))

# Folium 지도 생성
map_center = [36.5, 127.5]
university_map = folium.Map(location=map_center, zoom_start=7)

for _, row in coordinates_df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['University']} ({row['Address']})",
        icon=folium.Icon(color="blue")
    ).add_to(university_map)

# 결과 지도 저장
university_map.save(output_path)
print(f"지도 생성 완료: {output_path}")
