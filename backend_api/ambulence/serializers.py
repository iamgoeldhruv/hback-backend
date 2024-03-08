from rest_framework import serializers

from .import models

class AmbulanceLocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ambulance
        fields = ['number_plate', 'current_location_latitude', 'current_location_longitude']

class AmbulanceCurrentLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ambulance
        fields = ['current_location_latitude', 'current_location_longitude']

