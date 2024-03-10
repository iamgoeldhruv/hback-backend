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
from math import ceil



@api_view(['PUT'])
def updateAmbulance(request):
     number_plate = request.data["number_plate"]
     current_loc_lat = request.data["current_location_latitude"]
     current_loc_long = request.data["current_location_longitude"]

     amb = models.Ambulance.objects.filter(number_plate=number_plate)[0]
     amb.current_location_latitude = current_loc_lat
     amb.current_location_longitude = current_loc_long

     amb.save()
     
     print("xyz")
     print(number_plate)
     print(amb.current_location_latitude)

     

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
          co_ords = None
          for ambulance in ambulances:
               start_location = f"{ambulance.current_location_longitude},{ambulance.current_location_latitude}"
               end_location = f"{end_location_longitude},{end_location_latitude}"
               print( start_location)
               api_url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248258dee8d25fb456d9798ddc3f7741e68&start={start_location}&end={end_location}"
               response=requests.get(api_url)
               print(response.content)
               if response.status_code == 200:
                    time=response.json()["features"][0]["properties"]["segments"][0]["duration"]
                   
                    print(time)
                    time = float(time)
                    print(type(time))   
                    if(mtime>=float(time)):
                         print("Compared")
                         co_ords = response.json()["features"][0]["geometry"]
                         mtime=time
                         print("MIN YIMR" + str(time))
                         assigned_ambulance=ambulance
          if assigned_ambulance != None:
               assigned_ambulance.is_assigned = True
               assigned_ambulance.requester_ip = request.META.get('REMOTE_ADDR')  
               assigned_ambulance.assigned_location_latitude=end_location_latitude
               assigned_ambulance.assigned_location_longitude=end_location_longitude
               assigned_ambulance.save()
               serializer = self.get_serializer(assigned_ambulance)
               return Response({"data":serializer.data,"time":int(mtime/60) , "waypoints" : json.dumps(co_ords) })
          else:
               return Response({"message": "No available ."}, status=404)
          
class RemainingTimeView(generics.GenericAPIView):
     def get(self,request):
           requester_ip = request.META.get('REMOTE_ADDR')
           try:
                 ambulance = models.Ambulance.objects.get(requester_ip=requester_ip)
                 start_location=f"{ambulance.current_location_longitude},{ambulance.current_location_latitude}"
                 end_location=f"{ambulance.assigned_location_longitude},{ambulance.assigned_location_latitude}"
                 api_url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248258dee8d25fb456d9798ddc3f7741e68&start={start_location}&end={end_location}"
                 print(api_url)
                 response=requests.get(api_url)
                 if response.status_code == 200:
                    time_left = response.json()["features"][0]["properties"]["segments"][0]["duration"]
                    return Response({"time_left": ceil((time_left)/60)})
                 else:
                    print(response.content)
                    return Response({"message": "Failed to retrieve time from API"}, status=response.status_code)
                 
           except models.Ambulance.DoesNotExist:
                 return Response({"message": "so such ambulence exist"}, status=404)



                      


          
 

               

               

     
        
        

     