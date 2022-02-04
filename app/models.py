"""
Definition of models.
"""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

import uuid

# Create your models here.

class UserProfile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        name='account', 
        related_name='profile',
        null=True)


class BeaconDevice(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='beacons')


class Pet(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    species = models.TextField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='pets')
    beacon = models.OneToOneField(
        BeaconDevice, null=True, 
        on_delete=models.CASCADE,
        related_name='pet')