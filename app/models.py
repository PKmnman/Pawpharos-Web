"""
Definition of models.
"""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Model for storing the uuid of beacon devices
class BeaconDevice(models.Model):
    mac_addr = models.CharField(max_length=24, primary_key=True, unique=True)
    # Whether or not the beacon is being actively tracked
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='beacons')

    class Meta:
        verbose_name = "Beacon Device"


# Stores data about registered sniffers
class Sniffer(models.Model):
    serial_code = models.SlugField(max_length=24, primary_key=True, unique=True)
    location = models.CharField(max_length=128)
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
    name = models.CharField(max_length=125)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')
    beacon = models.OneToOneField(
        BeaconDevice,
        null=True,
        on_delete=models.CASCADE,
        to_field='mac_addr',
        related_name='pet')


# Model for storing and accessing location updates
class TrackingEvent(models.Model):
    event_time = models.DateTimeField(verbose_name="Event Time")
    # Beacon ID - The beacon detected (1:N)
    beacon = models.ForeignKey(BeaconDevice, on_delete=models.CASCADE, related_name="events")
    # Sniffer ID - The sniffer that detected it (1:N)
    sniffer = models.ForeignKey(Sniffer, on_delete=models.CASCADE, related_name="events")

    class Meta:
        verbose_name = "Tracking Event"
    
    