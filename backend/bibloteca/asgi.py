"""
ASGI config for bibloteca project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from .consumers import NotificationConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bibloteca.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("ws/notificacion/", NotificationConsumer.as_asgi())
                    # Add WebSocket URL routes here.
                ]
            )
        ),  # Add more ASGI WebSocket routes here if needed.
    }
)
