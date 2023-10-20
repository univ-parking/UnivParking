from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ParkingSerializer
from .models import SVC_I_PARK, SVC_T_PARK
from core.module import s3_connection

import pandas as pd
from datetime import datetime

from botocore.exceptions import NoCredentialsError

from django.utils.decorators import decorator_from_middleware, method_decorator
from .middleware import AutoTokenRefreshMiddleware
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

current_time = str(datetime.now().strftime('%Y-%m-%d %H:%M'))

class ParkingDataAPIView(APIView):
    def get(self):
        pass


    def post(self, request):
        s3, bucket_name = s3_connection()
        object_name = 'data/' + current_time + ' parking data.csv'

        queryset = SVC_I_PARK.objects.all()
        serializer = ParkingSerializer(queryset, many=True)

        df = pd.DataFrame(list(queryset.values()))
        df['DT'] = pd.to_datetime(df['updated_data']).dt.strftime('%Y-%m-%d %H:%M')
        df = df.drop(['created_data', 'updated_data', 'id', 'PT'], axis=1)

        df.to_csv('./data/data.csv')

        try:
            s3.upload_file('./data/test.csv', bucket_name, object_name)
            print(f'Successfully uploaded data.csv to {bucket_name}/{object_name}')
        except NoCredentialsError:
            print('AWS credentials not available.')
        return Response(serializer.data)

