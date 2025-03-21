import asyncio
import json
import logging

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.users.models.notification import Notification

logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                f"user_{self.user.id}", self.channel_name
            )
            logger.info(f"User {self.user.id} connected to notification channel.")
            await self.accept()

            self.periodic_task = asyncio.create_task(
                self.check_notifications_periodically()
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"user_{self.user.id}", self.channel_name
        )
        if hasattr(self, "periodic_task") and self.periodic_task:
            self.periodic_task.cancel()

    async def check_notifications_periodically(self):
        try:
            while True:
                await self.check_and_send_notifications()
                await asyncio.sleep(5)
        except asyncio.CancelledError:
            pass

    async def check_and_send_notifications(self):
        """
        Send new notifications to the client if `is_send=False` and update `is_send` to `True` after sending.
        """
        notifications = await sync_to_async(list)(
            Notification.objects.filter(user=self.user, is_send=False)
        )

        for notification in notifications:
            notification_data = {
                "type": "send_notification",
                "id": notification.id,
                "user": self.user.id,
                "banner": notification.banner.url if notification.banner else None,
                "title": notification.title_uz,
                "message": notification.message_uz,
                "created_at": notification.created_at.isoformat(),
                "is_read": notification.is_read,
            }
            try:
                await self.send(text_data=json.dumps(notification_data))
                # Update the is_send flag after sending the notification.
                notification.is_send = True
                await sync_to_async(notification.save)()
            except Exception as e:
                logger.error(f"Failed to send notification to user {self.user.id}: {e}")

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event))
