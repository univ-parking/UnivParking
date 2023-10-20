from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ParkingSerializer

from .models import SVC_I_PARK, SVC_T_PARK

from django.utils.decorators import decorator_from_middleware, method_decorator
from .middleware import AutoTokenRefreshMiddleware
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class ParkingAPIView(APIView):
    allowed_methods = ['PATCH']

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

        for item in data:
            try:
                # "AN" 값을 기반으로 데이터베이스에서 해당 항목을 찾음
                park_instance = SVC_I_PARK.objects.get(AN=item['AN'])
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
    def get(self, request, type_id, AN=None):
        try:
            if AN == None:
                queryset = SVC_I_PARK.objects.filter(type=SVC_T_PARK.objects.get(pk=type_id))
            else:
                queryset = SVC_I_PARK.objects.filter(id=AN, type=SVC_T_PARK.objects.get(pk=type_id))
        except SVC_I_PARK.DoesNotExist:
            return Response({'detail': '해당 객체를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ParkingSerializer(queryset, many=True)

        return Response(serializer.data)


