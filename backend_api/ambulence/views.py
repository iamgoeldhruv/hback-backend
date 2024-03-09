from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from .import models
from .import serializers
import json


@api_view(['PUT'])
def updateAmbulance(request):
     number_plate = request.data["number_plate"]
     current_loc_lat = request.data["current_location_latitude"]
     current_loc_long = request.data["current_location_longitude"]

     amb = models.Ambulance.objects.filter(number_plate=number_plate)[0]
     amb.current_location_latitude = current_loc_lat
     amb.current_location_longitude = current_loc_long

     amb.save()

     return Response("Done!")         
        
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
               assigned_ambulance.assigned_location_latitude=end_location_latitude
               assigned_ambulance.assigned_location_longitude=end_location_longitude
               assigned_ambulance.save()
               serializer = self.get_serializer(assigned_ambulance)
               return Response(serializer.data)
          else:
               return Response({"message": "No available ."}, status=404)

               

               

     
        
        

     