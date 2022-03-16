from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework import permissions
from app.api.serializers import SnifferSerializer, UserSerializer

import app.models as models


class SnifferApiView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request, *args, **kwargs):
		sniffers = models.Sniffer.objects.filter(owner = request.user.profile)
		serializer = SnifferSerializer(sniffers, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def get_object(self, sniffer_id, user_id):
		try:
			return models.Sniffer.objects.get(id=sniffer_id, owner = models.UserProfile.objects.get(id=user_id).id)
		except models.Sniffer.DoesNotExist:
			return None

@api_view(['GET'])
#@permission_classes([permissions.IsAdminUser])
def list_users(request):
	users = models.User.objects.all()
	serializer = UserSerializer(users, many= True)
	return Response(serializer.data, status=status.HTTP_200_OK)
