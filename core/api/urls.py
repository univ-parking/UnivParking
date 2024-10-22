from django.urls import path, include
from .views import ParkingAPIView, ParkingDetailAPIView, ParkingTypeAPIView
from .file import ParkingDataSaveAPIView

urlpatterns = [
	# Update, List
	path('parking/', ParkingAPIView.as_view(), name='parking-api'),

	# Parking Detail
	path('parking/<int:type_id>/<int:AN>/', ParkingDetailAPIView.as_view()),
	path('parking/<int:type_id>/', ParkingDetailAPIView.as_view()),

	# Parking Data
	# Parking Data Save
	path('parking/data/save', ParkingDataSaveAPIView.as_view()),

	# Parking Type List
	path('parking/type', ParkingTypeAPIView.as_view()),

	]
