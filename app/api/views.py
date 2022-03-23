import rest_framework.authtoken.models
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework import permissions
from app.api.serializers import SnifferSerializer, UserSerializer

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
		device_name = request.REQUEST["device_name"]
		owner = request.user
		is_master = request.REQUEST["is_master"]
		serial_code = request.REQUEST["serial"]

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
