from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from . import consumers
from django.core.asgi import get_asgi_application

websocket_urlpatterns = [
    path('ws/appointments/<int:patient_id>/', consumers.AppointmentConsumer.as_asgi()),
]
