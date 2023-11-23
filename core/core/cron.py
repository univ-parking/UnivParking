import json, cv2
from roboflow import Roboflow
import numpy as np
import requests

# 카메라 객체 생성

# 변수 선언
is_parked = np.zeros(23, dtype="int")
type_id = 1


# 카메라 설정
# Car Object Detaction Model init - api.py
rf = Roboflow(api_key="J4XztfjQQ1yt8xcmCquy")
project = rf.workspace().project("car5-rliby")
model = project.version(4).model

with open('coordinate/img_labeling_list.json', 'r') as file:
    coordinate = json.load(file)

# 이미지 캡처
while 1:
    try:
        data = model.predict('test.jpg', confidence=50, overlap=30).json()
        for datas in data.get("predictions"):
            x_coordinate = datas.get('x')
            y_coordinate = datas.get('y')
            for coordinates in coordinate:
                x_list, y_list = coordinates.get('x'), coordinates.get('y')
                if x_list[0] <= x_coordinate <= x_list[1]:
                    if y_list[0] <= y_coordinate <= y_list[1]:
                        is_parked[coordinates.get('id')] = True
        response_data = {
            "category": "list",
            "detail": {
                "type": type_id,
                "data": is_parked.tolist()
                }
            }

        url = "http://univ-parking.xyz/api/v1/parking/"+str(type_id)+"/"
        response = requests.get(url,)
        data = json.loads(response.text)

        if is_parked.tolist() == data.get('data').get('array'):
            print("same data")
            pass
        else:
            response = requests.patch(url, json=response_data,)

            if response.status_code == 200:
                print("업데이트 성공!")
                response = requests.get("http://univ-parking.xyz/api/v1/parking/data/save")
                if response.status_code == 200:
                    print("버킷 저장 성공!")
                else:
                    print("저장 실패. 상태 코드:", response.status_code)
                    print(response.reason)
            else:
                print("업데이트 실패. 상태 코드:", response.status_code)
                print(response.reason)
    except KeyboardInterrupt:
        break
