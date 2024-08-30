from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import json
import logging

logger = logging.getLogger(__name__)




class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Log adicional para verificar el proceso de autenticación
        logger.info(f"Attempting to connect: {self.scope['user']}")

        # Verificar si el usuario está autenticado
        if self.scope["user"].is_authenticated:
            logger.info(f"User authenticated: {self.scope['user']}")
            self.user = self.scope["user"]

            # Unirse al grupo de notificaciones del usuario
            await self.channel_layer.group_add(
                f"user_{self.user.id}", 
                self.channel_name
            )
            await self.accept()
        else:
            logger.warning("User not authenticated")
            await self.close()

    async def disconnect(self, close_code):
        # Log de desconexión
        logger.info(f"Disconnecting: {self.scope['user']}")
        
        # Salir del grupo de notificaciones del usuario
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_discard(
                f"user_{self.user.id}", 
                self.channel_name
            )

    async def receive(self, text_data):
        # Recibir datos del WebSocket
        data = json.loads(text_data)
        
        # Enviar la notificación recibida de vuelta al cliente
        await self.send(text_data=json.dumps({
            "type": "notification", 
            "message": data.get("message", "")
        }))

    async def send_notification(self, event):
        # Enviar notificación al cliente
        notification = event["notification"]
        await self.send(text_data=json.dumps({
            'notification': notification
        }))

