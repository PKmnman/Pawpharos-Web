import django.db.models
from django.contrib import admin
from app import models


@admin.register(models.Sniffer)
class SnifferAdmin(admin.ModelAdmin):
	fields = ('location', 'serial_code', ('owner',))
	list_display = ('serial_code', 'location')
	list_display_links = ('serial_code',)


@admin.register(models.BeaconDevice)
class BeaconAdmin(admin.ModelAdmin):
	fields = ('mac_addr', 'owner')
	list_display = ('mac_addr', 'owner')
	list_display_links = ('mac_addr',)
	search_fields = ['owner__email', 'mac_addr']


@admin.register(models.TrackingEvent)
class EventAdmin(admin.ModelAdmin):
	ordering = ['event_time']
	date_hierarchy = 'event_time'
	list_display = ('event_time', 'beacon_addr', 'sniffer_serial')
	list_display_links = ('event_time',)