"""
Definition of models.
"""

from django.db import models

# Create your models here.

class UserAccount(models.Model):
    userID = models.TextField()
    first_name = models.TextField(max_length=64)
    last_name = models.TextField(max_length=64)
    email = models.EmailField()

    # devices = BeaconManager()


class BeaconDevice(models.Model):
    uuid = models.UUIDField(primary_key=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='beacons')


class Pet(models.Model):
    name = models.TextField()
    species = models.TextField()
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='pets')

    beacon = models.OneToOneField(BeaconDevice, on_delete=models.CASCADE)