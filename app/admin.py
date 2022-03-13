from django.contrib import admin
from app import models

@admin.register(models.Sniffer)
class SnifferAdmin(admin.ModelAdmin):
	pass