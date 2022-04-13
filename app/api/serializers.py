from rest_framework import serializers
import app.models as models


class UserSerializer(serializers.ModelSerializer):
	
	sniffers = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Sniffer.objects.all(), required=False)
	locations = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Location.objects.all(), required=False)

	class Meta:
		model = models.User
		fields = ['id', 'username', 'sniffers', 'locations']
		read_only_fields = ['id']


class SnifferSerializer(serializers.ModelSerializer):

	owner = serializers.PrimaryKeyRelatedField(queryset=models.User.objects.all(), required = False)

	def create(self, validated_data):
		return models.Sniffer.objects.create(**validated_data)

	class Meta:
		model = models.Sniffer
		fields = ['id', 'serial_code', 'owner']


class TrackingEventSerializer(serializers.ModelSerializer):

	time = serializers.DateTimeField(format="%m-%d-%y %H:%M:%S.%fz")

	class Meta:
		model = models.TrackingEvent
		fields = ['sniffer', 'beacon', 'time']
