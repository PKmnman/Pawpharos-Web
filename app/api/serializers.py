from rest_framework import serializers
import app.models as models


class UserSerializer(serializers.ModelSerializer):
	
	sniffers = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Sniffer.objects.all(), required=False)

	class Meta:
		model = models.User
		fields = ['id', 'username', 'sniffers']
		read_only_fields = ['id']


class SnifferSerializer(serializers.ModelSerializer):

	owner = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all(), required = False)

	def create(self, validated_data):
		return models.Sniffer.objects.create(**validated_data)

	class Meta:
		model = models.Sniffer
		fields = ['id', 'serial_code', 'owner']


class TrackingEventSerializer(serializers.ModelSerializer):

	event_time = serializers.DateTimeField(format="%m-%d-%y %H:%M:%S.%fz", required=True)

	class Meta:
		models = models.TrackingEvent
		fields = ['event_time', 'beacon_addr', 'sniffer_serial', 'rssi']