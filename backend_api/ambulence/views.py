from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
import requests
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
        
class AssignAmbuanceView(generics.GenericAPIView):
     serializer_class =serializers.AmbulanceSerializer
     def get(self,request):
          ambulances = models.Ambulance.objects.filter(is_active=True, is_assigned=False)
          end_location_latitude = request.query_params.get('assigned_location_latitude')
          end_location_longitude = request.query_params.get('assigned_location_longitude')
          mtime=float('inf')
          assigned_ambulance=None
          for ambulance in ambulances:
               start_location = f"xyz;{ambulance.current_location_latitude},{ambulance.current_location_longitude}"
               end_location = f"uvw;{end_location_latitude},{end_location_longitude}"
               print( start_location)
               api_url = f"https://wps.hereapi.com/v8/findsequence2?apiKey=dFfyuh7vgDXD4w4FCqyHp7A7HVJyAGebVkUYQzt34gw&start={start_location}&end={end_location}&mode=truck"
               response=requests.get(api_url)
               if response.status_code == 200:
                    time=response.json()["results"][0]["time"]
                    
                    print(time)
                    time = float(time)
                    print(type(time))
                    if(mtime>=float(time)):
                         print("Compared")
                         mtime=time
                         assigned_ambulance=ambulance
          if assigned_ambulance != None:
               assigned_ambulance.is_assigned = True
               assigned_ambulance.requester_ip = request.META.get('REMOTE_ADDR')  
               assigned_ambulance.save()
               serializer = self.get_serializer(assigned_ambulance)
               return Response(serializer.data)
          else:
               return Response({"message": "No available ."}, status=404)

               

               

     
        
        

     