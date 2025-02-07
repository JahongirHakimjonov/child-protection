import asyncio
import json
import logging

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.mobile.models.help import Help

logger = logging.getLogger(__name__)


class HelpConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.user = await self.get_user()
        if not self.user:
            await self.close()
        else:
            await self.channel_layer.group_add(
                f"user_{self.user_id}", self.channel_name
            )
            logger.info(f"User {self.user_id} connected to help channel.")
            await self.accept()

            self.periodic_task = asyncio.create_task(
                self.check_help_periodically()
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            f"user_{self.user_id}", self.channel_name
        )
        if hasattr(self, "periodic_task") and self.periodic_task:
            self.periodic_task.cancel()

    async def check_help_periodically(self):
        try:
            while True:
                await self.check_and_send_help()
                await asyncio.sleep(5)
        except asyncio.CancelledError:
            pass

    async def check_and_send_help(self):
        """
        Send new help to the client if `is_send=False` and update `is_send` to `True` after sending.
        """
        helps = await sync_to_async(list)(
            Help.objects.filter(user=self.user, is_send=False)
        )

        for help in helps:
            help_data = {
                "type": "send_help",
                "id": help.id,
                "user": self.user_id,
                "longitude": help.longitude,
                "latitude": help.latitude,
                "status": help.status,
                "created_at": help.created_at.isoformat(),
            }
            await self.send(text_data=json.dumps(help_data))
            help.is_send = True
            await sync_to_async(help.save)()

    async def get_user(self):
        return await sync_to_async(Help.objects.get)(user_id=self.user_id)
