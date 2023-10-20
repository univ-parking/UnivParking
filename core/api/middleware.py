# middleware.py

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response

class AutoTokenRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the response has a 401 Unauthorized status
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            # Try to get the refresh token from the request headers
            refresh_token = request.META.get('HTTP_AUTHORIZATION')
            print(refresh_token)
            if refresh_token:
                # Extract the token value from the Authorization header
                refresh_token = refresh_token.replace('Bearer ', '')  # Remove 'Bearer ' prefix
                print(refresh_token)
                try:
                    refresh = RefreshToken(refresh_token)
                    print(refresh)
                    access_token = str(refresh.access_token)
                    response.data = {'access_token': access_token}
                    response.status_code = status.HTTP_200_OK
                except Exception as e:
                    # Handle token refresh failure
                    response.data = {'detail': '유효한 Refresh token이 아닙니다.'}
                    response.status_code = status.HTTP_400_BAD_REQUEST

        return response
