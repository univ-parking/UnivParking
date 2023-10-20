from django.urls import path, include
from rest_framework import urls
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('list', UserViewSet) # 유저리스트 (테스트용)


urlpatterns = [
    path("", include(router.urls)),
    ]