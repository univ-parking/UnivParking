from .models import SVC_I_PARK
from rest_framework import serializers

class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SVC_I_PARK
        fields = '__all__'
