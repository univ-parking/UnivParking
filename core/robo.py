import json, cv2
from roboflow import Roboflow
import numpy as np
import time
import requests

# 변수 선언
is_parked = np.zeros(23, dtype="int")
type_id = 1
lastdata = list()
host = "http://univ-parking.xyz/"
# host = "http://localhost:8000/"

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
        # img modeling - api.py
        data = model.predict('test.jpg', confidence=40, overlap=30).json()
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

        if is_parked.tolist() == lastdata:
            pass
        else:
            response = requests.patch(host+"api/v1/parking/", json=response_data,)
            if response.status_code == 200:
                response = requests.get(host+"api/v1/parking/data/save")
                if response.status_code == 200:
                    response = requests.get(host+"api/v1/parking/"+str(type_id)+"/", )
                    data = json.loads(response.text)
                    lastdata = data.get('data').get('array')
                else:
                    print("저장 실패. 상태 코드:", response.status_code)
                    print(response.reason)
            else:
                print("업데이트 실패. 상태 코드:", response.status_code)
                print(response.reason)
        time.sleep(1)
    except KeyboardInterrupt:
        break

