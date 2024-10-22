from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ParkingSerializer, ParkingTypeSerializer

from .models import SVC_I_PARK, SVC_T_PARK

from django.utils.decorators import decorator_from_middleware, method_decorator
from .middleware import AutoTokenRefreshMiddleware
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


result = dict()

class ParkingAPIView(APIView):
    allowed_methods = ['GET', 'POST', 'PATCH', 'OPTIONS']  # Include 'OPTIONS'

    def get(self, request):
        # 모든 모델 인스턴스를 가져오고 직렬화합니다.
        queryset = SVC_I_PARK.objects.all()
        serializer = ParkingSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request):
        data = request.data  # JSON 데이터를 요청에서 가져옵니다.
        serializer = ParkingSerializer(data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        data = request.data  # JSON 데이터를 요청에서 가져옵니다.
        detail = data.get('detail')
        type = detail.get('type')
        data_list = detail.get('data')
        print(data.get('data'))

        if data.get('category') == "list":
            queryset = SVC_I_PARK.objects.filter(type=type)
            if len(detail.get('data')) == len(queryset):
                for i, item in enumerate(queryset):
                    item.PC = data_list[i]
                    item.save()
            else:
                result['error'] = f"{type}번 주차장의 주차공간은 {len(queryset)}개 입니다. 개수에 맞게 data의 값을 수정해 주세요. 현재 : {len(data_list)}개"
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            return Response("Data updated successfully", status=status.HTTP_200_OK)
        else:
            for item in data.get('data'):
                try:
                    # "AN" 값을 기반으로 데이터베이스에서 해당 항목을 찾음
                    park_instance = SVC_I_PARK.objects.get(AN=item['AN'], type=item['type'])
                    park_instance.PC = not park_instance.PC
                    serializer = ParkingSerializer(park_instance, data=item)

                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except SVC_I_PARK.DoesNotExist:
                    # 해당 "AN" 값이 데이터베이스에 없는 경우에 대한 처리
                    return Response({'error': f"AN {item['AN']} not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response("Data updated successfully", status=status.HTTP_200_OK)


class ParkingDetailAPIView(APIView):
    allowed_methods = ['GET', 'OPTIONS']  # Include 'OPTIONS'

    def get(self, request, type_id, AN=None):
        try:
            if AN == None:
                queryset = SVC_I_PARK.objects.filter(type=SVC_T_PARK.objects.get(pk=type_id))
            else:
                queryset = SVC_I_PARK.objects.filter(id=AN, type=SVC_T_PARK.objects.get(pk=type_id))
        except SVC_I_PARK.DoesNotExist:
            return Response({'detail': '해당 객체를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ParkingSerializer(queryset, many=True)

        result['data'] = {
            'count': len(queryset),
            'array': [item.PC for item in queryset],
            'detail': serializer.data
            }

        return Response(result)


class ParkingTypeAPIView(APIView):
    allowed_methods = ['GET', 'OPTIONS']  # Include 'OPTIONS'

    def get(self, request):
        try:
            queryset = SVC_T_PARK.objects.all()
        except SVC_T_PARK.DoesNotExist:
            result['detail'] = '해당 객체를 찾을 수 없습니다.'
            result['status'] = {
                'oldcode': 404,
                'detail': status.HTTP_404_NOT_FOUND
                }
            return Response(result, status=status.HTTP_404_NOT_FOUND)

        serializer = ParkingTypeSerializer(queryset, many=True)
        result['data'] = {
            'count': len(queryset),
            'detail': serializer.data
            }
        return Response(result)

