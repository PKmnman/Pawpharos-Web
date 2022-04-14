import datetime

import rest_framework.authentication
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework import permissions
from app.api.serializers import SnifferSerializer, UserSerializer, TrackingEventSerializer
import logging
from django.views.decorators.csrf import csrf_exempt
import app.models as models


class SnifferApiView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	renderer_classes = [JSONRenderer]

	def get(self, request, *args, **kwargs):
		sniffers = models.Sniffer.objects.filter(owner = request.user.profile)
		serializer = SnifferSerializer(sniffers, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def get_object(self, sniffer_id, user_id):
		try:
			return models.Sniffer.objects.get(id=sniffer_id, owner = models.User.objects.get(id=user_id).id)
		except models.Sniffer.DoesNotExist:
			return None


class TrackingEventAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	renderer_classes = [JSONRenderer]
	authentication_classes = [rest_framework.authentication.TokenAuthentication]

	def post(self, request: HttpRequest):
		try:
			assert isinstance(request.data['sniffer_serial'], str)
		except AssertionError:
			return Response({'error': 'Missing required parameter uuid.'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			assert isinstance(request.data['beacon_addr'], str)
		except AssertionError:
			return Response({'error': 'Missing required parameter sniffer.'}, status=status.HTTP_400_BAD_REQUEST)

		# Retrieve the requested beacon and sniffer
		beacon = request.user.beacons.get(mac_addr=request.data['beacon_addr'])
		sniffer = request.user.sniffers.get(serial_code=request.data['sniffer_serial'])

		event_time = datetime.datetime.fromisoformat(request.data['event_time'])

		prev_event = models.TrackingEvent.objects.filter(beacon_addr=beacon, sniffer_serial=sniffer).order_by('-event_time')[0]

		event = models.TrackingEvent(beacon_addr=beacon,
									 sniffer_serial=sniffer,
									 event_time=event_time,
									 rssi=request.data['rssi'])

		if prev_event is not None and (event_time - prev_event.event_time) < datetime.timedelta(minutes=5):
			return Response(status=status.HTTP_208_ALREADY_REPORTED)

		event.save()
		return Response(status=status.HTTP_201_CREATED)


@api_view(['PUT', 'POST'])
@renderer_classes([JSONRenderer])
@permission_classes([permissions.IsAuthenticated])
def create_sniffer(request):

	if request.method == 'PUT':
		device_name = request.data["device_name"]
		owner = request.user
		is_master = request.data["is_master"]
		serial_code = request.data["serial"]

		sniffer = models.Sniffer.objects.create(device_name=device_name, serial_code=serial_code, is_master=is_master,
												owner=owner)
		sniffer.save()

		serializer = SnifferSerializer(sniffer)

		return Response(serializer.data, status=status.HTTP_200_OK)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'],)
@renderer_classes([JSONRenderer])
@permission_classes([permissions.IsAdminUser])
def list_users(request):
	users = models.User.objects.all()
	serializer = UserSerializer(users, many= True)
	return Response(serializer.data, status=status.HTTP_200_OK)
