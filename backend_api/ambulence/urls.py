from django.urls import path
from .import views

urlpatterns = [
    path('api/update-ambulance-location/', views.AmbulanceLocationUpdateAPIView.as_view(), name='update_ambulance_location'),
    path('api/get-ambulance-location/', views.GetAmbulanceLocationAPIView.as_view(), name='get_ambulance_location'),
]