"""
Definition of models.
"""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

class BeaconDevice(models.Model):
    uuid = models.UUIDField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='beacons')


class Pet(models.Model):
    name = models.TextField()
    species = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pets')

    beacon = models.OneToOneField(BeaconDevice, on_delete=models.CASCADE)