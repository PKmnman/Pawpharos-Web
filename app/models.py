"""
Definition of models.
"""

from django.db import models
from django.conf import settings

from uuid import uuid4

# Create your models here.

# Model for storing user-related data
class UserProfile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4)
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        name='account', 
        related_name='profile',
        null=True)

# Model for storing the uuid of beacon devices
class BeaconDevice(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='beacons')

# Stores data for pets
class Pet(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.TextField()
    species = models.TextField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='pets')
    beacon = models.OneToOneField(
        BeaconDevice, null=True, 
        on_delete=models.CASCADE,
        related_name='beacon')

# Stores data about registered sniffers
class Sniffer(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.TextField(max_length=64)
    reg_code = models.Func()
    is_master = models.BooleanField()
    owner = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name="owner")

# Model for storing and accessing location updates
class BeaconPing(models.Model):
    id = models.AutoField(primary_key=True)
    beacon = models.ForeignKey(
        BeaconDevice,
        on_delete=models.CASCADE,
        related_name='beacon')
    sniffer = models.ForeignKey(
        Sniffer,
        on_delete=models.CASCADE,
        related_name='source')
    time = models.DateTimeField()
    