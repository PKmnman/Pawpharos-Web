from django.contrib import admin
from app import models

@admin.register(models.Sniffer)
class SnifferAdmin(admin.ModelAdmin):
	pass

@admin.register(models.BeaconDevice)
class BeaconAdmin(admin.ModelAdmin):
	pass


@admin.register(models.TrackingEvent)
class EventAdmin(admin.ModelAdmin):
	ordering = ['time']