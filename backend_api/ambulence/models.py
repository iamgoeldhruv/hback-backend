from django.db import models

from django.db import models

class Ambulance(models.Model):
   
    number_plate = models.CharField(primary_key=True, max_length=20)
    current_location_latitude = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    current_location_longitude = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_assigned = models.BooleanField(default=False)
    assigned_location_latitude = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    assigned_location_longitude = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    requester_ip = models.GenericIPAddressField(blank=True, null=True)
   
    def __str__(self):
        return self.number_plate

