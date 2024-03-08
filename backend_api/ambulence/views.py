from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .import models
from .import serializers


# Create your views here.
class AmbulanceLocationUpdateAPIView(APIView):
    def post(self,request):
        serializer = serializers.AmbulanceLocationUpdateSerializer(data=request.data)
        number_plate = serializer.validated_data['number_plate']
        current_location_latitude = serializer.validated_data['current_location_latitude']
        current_location_longitude = serializer.validated_data['current_location_longitude']
        try:
            ambulance = models.Ambulance.objects.get(number_plate=number_plate)
            ambulance.current_location_latitude = current_location_latitude
            ambulance.current_location_longitude = current_location_longitude

            ambulance.save()
            return Response({'message': 'Ambulance location updated successfully.'}, status=status.HTTP_200_OK)
        except models.Ambulance.DoesNotExist:
                return Response({'error': 'no such ambulence.'}, status=status.HTTP_404_NOT_FOUND)

        
        
class GetAmbulanceLocationAPIView(APIView):
    def get(self, request):
        requester_ip = request.META.get('REMOTE_ADDR')  
        try:
            ambulance = models.Ambulance.objects.get(requester_ip=requester_ip)
            serializer = serializers.AmbulanceCurrentLocationSerializer(ambulance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Ambulance.DoesNotExist:
            return Response({'error': 'No ambulance assigned for the requester IP address.'}, status=status.HTTP_404_NOT_FOUND)
