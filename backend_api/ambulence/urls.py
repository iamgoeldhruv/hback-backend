from django.urls import path
from .import views

urlpatterns = [
    path('api/update-ambulance-location/', views.updateAmbulance),
    path('api/get-ambulance-location/', views.GetAmbulanceLocationAPIView.as_view(), name='get_ambulance_location'),
    path('api/assign-ambulance/', views.AssignAmbuanceView.as_view(), name='assign_ambulance'),
    path('api/Remaining-Time/', views.RemainingTimeView.as_view(), name='time_left'),
]