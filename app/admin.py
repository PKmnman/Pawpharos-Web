import django.db.models
from django.contrib import admin
from app import models


@admin.register(models.Sniffer)
class SnifferAdmin(admin.ModelAdmin):
	fields = ('device_name', 'serial_code', ('owner', 'is_master'))
	list_display = ('device_name', 'serial_code')
	list_display_links = ('device_name',)


@admin.register(models.BeaconDevice)
class BeaconAdmin(admin.ModelAdmin):
	pass


@admin.register(models.TrackingEvent)
class EventAdmin(admin.ModelAdmin):
	ordering = ['event_time']
	list_display_links = ('event_time',)