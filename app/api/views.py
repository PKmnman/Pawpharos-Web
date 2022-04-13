import datetime

import rest_framework.authtoken.models
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework import permissions
from app.api.serializers import SnifferSerializer, UserSerializer
import time

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

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([permissions.IsAuthenticated])
def post_tracking_event(request):
	if request.method == 'POST':
		try:
			assert isinstance(request.data['uuid'], str)
		except AssertionError:
			return Response({'data': 'Missing required parameter uuid.'}, status=status.HTTP_400_BAD_REQUEST)

		try:
			assert isinstance(request.data['sniffer'], str)
		except AssertionError:
			return Response({'data': 'Missing required parameter sniffer.'}, status=status.HTTP_400_BAD_REQUEST)

		# Retrieve the requested beacon and sniffer
		beacon = request.user.beacons.get(bc_uuid=request.data['uuid'])
		sniffer = request.user.beacons.get(serial_code=request.data['sniffer'])

		if sniffer is None:
			return Response({"details": "Sniffer does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

		if beacon is None:
			return Response({"details": "Beacon does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

		location = sniffer.location

		event = models.TrackingEvent.objects.create(beacon=beacon, sniffer=sniffer, location=location, time=time.asctime())
		event.save()

		return Response(status=status.HTTP_200_OK)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)

	pass


@api_view(['GET'],)
@renderer_classes([JSONRenderer])
@permission_classes([permissions.IsAdminUser])
def list_users(request):
	users = models.User.objects.all()
	serializer = UserSerializer(users, many= True)
	return Response(serializer.data, status=status.HTTP_200_OK)
