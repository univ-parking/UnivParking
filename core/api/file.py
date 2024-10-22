from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ParkingSerializer
from .models import SVC_I_PARK, SVC_T_PARK
from core.module import s3_connection

import pandas as pd
from datetime import datetime

from botocore.exceptions import NoCredentialsError

current_time = str(datetime.now().strftime('%H:%M:%S'))
base_path = str(datetime.now().strftime('%Y-%m-%d'))


#  만약, 객체탐지 이후 변경졈이 있다면, s3버킷에 저장하는 형태로 간다.
#  변경점이 없다면 유지
class ParkingDataSaveAPIView(APIView):
    allowed_methods = ['GET', 'POST', 'OPTIONS']  # Include 'OPTIONS'

    def get(self, request):
        s3, bucket_name = s3_connection()
        object_name = 'data/' + base_path + '/' + current_time + ' Data.csv'

        queryset = SVC_I_PARK.objects.all()

        df = pd.DataFrame(list(queryset.values()))
        df['DT'] = pd.to_datetime(df['updated_data']).dt.strftime('%Y-%m-%d %H:%M')
        df = df.drop(['created_data', 'updated_data', 'id', 'PT'], axis=1)

        df.to_csv("./data/test.csv")

        try:
            s3.upload_file('./data/test.csv', bucket_name, object_name)
        except NoCredentialsError:
            data = {
                'status': status.HTTP_503_SERVICE_UNAVAILABLE,
                'detail': 'AWS credentials not available.'
                }
            return Response(data)
        data = {
            'status': status.HTTP_200_OK,
            'detail': f'Successfully uploaded {bucket_name}/{object_name}'
            }
        return Response(data)

    def post(self, request):
        import numpy as np
        import cv2

        if 'image' not in request.FILES:
            return Response('Empty Content', status=status.HTTP_400_BAD_REQUEST)
        else:
            # 이미지 파일을 읽어옵니다.
            image_file = request.FILES['image']
            image_data = image_file.read()

            # 이미지 데이터를 NumPy 배열로 변환
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # 이미지 처리 작업 수행 (예: 회전, 필터 적용 등)
            # 처리된 이미지를 반환 (이 예제에서는 그대로 반환)
            w, h = 640, 480
            location = np.array([[113, 91], [520, 91], [603, 414], [28, 421]], np.float32)
            location2 = np.array([[0, 0], [w, 0], [w, h], [0, h]], np.float32)
            pers = cv2.getPerspectiveTransform(location, location2)
            dst = cv2.warpPerspective(image, pers, (w, h))

            cv2.imwrite('test.jpg', dst)

            return Response('Empty Content', status=status.HTTP_200_OK)
