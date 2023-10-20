from django.urls import path, include
from .views import ParkingAPIView, ParkingDetailAPIView
from .file import ParkingDataAPIView

app_name = "api"

urlpatterns = [
	# Update, List
	path('parking/', ParkingAPIView.as_view(), name='parking-api'),

	# Parking Detail
	path('parking/<int:type_id>/<int:AN>/', ParkingDetailAPIView.as_view()),
	path('parking/<int:type_id>/', ParkingDetailAPIView.as_view()),

	# Parking Data
	path('parking/data/', ParkingDataAPIView.as_view()),

	]
