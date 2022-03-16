"""
Definition of models.
"""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from uuid import uuid4


# Model for storing the uuid of beacon devices
class BeaconDevice(models.Model):

    class ModelName(models.TextChoices):
        DEV_MODEL = 'DEV', 'Development Model'
        IBEACON = 'IB', 'iBeacon' # For future iBeacon support

    device_name = models.TextField(max_length=64, default="Beacon Device", null=True)

    # This is the UUID the beacon broadcasts
    bc_uuid = models.UUIDField("Broadcast UUID", null=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='beacons')


# Stores data about registered sniffers
class Sniffer(models.Model):
    device_name = models.TextField(max_length=64)
    serial_code = models.SlugField(max_length=19)
    is_master = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User,
        null=True, 
        on_delete=models.SET_NULL, 
        related_name="sniffers")

# Stores User-Defined Locations
class Location(models.Model):
    label = models.CharField(max_length=64)
    description = models.TextField(default="")
    sniffer = models.OneToOneField(Sniffer, on_delete=models.SET_NULL, null=True)
    # The account this location belongs to
    account = models.ForeignKey(User, on_delete=models.CASCADE, related_name="locations")


# Stores data for pets
class Pet(models.Model):
    name = models.TextField()
    species = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')
    beacon = models.OneToOneField(
        BeaconDevice, 
        null=True,
        on_delete=models.CASCADE,
        related_name='pet')


# Model for storing and accessing location updates
class TrackingEvent(models.Model):
    time = models.DateTimeField()
    # Beacon ID - The beacon detected (1:N)
    beacon = models.ForeignKey(BeaconDevice, on_delete=models.CASCADE, related_name="events")
    # Sniffer ID - The sniffer that detected it (1:N)
    sniffer = models.ForeignKey(Sniffer, on_delete=models.CASCADE, related_name="events")

    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="+")
    
    