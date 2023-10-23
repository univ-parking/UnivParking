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

