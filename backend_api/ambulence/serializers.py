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

class AmbulanceSerializer(serializers.ModelSerializer):
    requester_ip = serializers.IPAddressField()
    assigned_location_latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    assigned_location_longitude = serializers.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        model = models.Ambulance
        fields = ['number_plate', 'current_location_latitude', 'current_location_longitude', 'requester_ip', 'assigned_location_latitude', 'assigned_location_longitude']
