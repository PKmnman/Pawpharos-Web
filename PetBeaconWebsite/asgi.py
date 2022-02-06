from email.mime import application
import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PetBeaconWebsite.settings')

application = get_asgi_application()