import asyncio
import json
import logging

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import UntypedToken

from apps.mobile.models.help import Help, HelpStatus
from apps.users.models.users import User

logger = logging.getLogger(__name__)


class HelpConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        # Foydalanuvchini autentifikatsiya qilamiz
        self.user = await self.authenticate_user()
        if isinstance(self.user, AnonymousUser) or not self.user:
            await self.close()
            return

        # Websocketga bog‘lanish vaqtini belgilab olamiz
        self.connected_at = timezone.now()

        await self.channel_layer.group_add(f"user_{self.user_id}", self.channel_name)
        logger.info(f"User {self.user_id} connected to help channel.")
        await self.accept()

        self.periodic_task = asyncio.create_task(self.check_help_periodically())

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
        Faqat foydalanuvchi bog‘lanish vaqtidan keyin yaratilgan help yozuvlarini mijozga yuboradi.
        """
        helps = await sync_to_async(list)(
            Help.objects.filter(
                user=self.user_id,
                is_send=False,
                status=HelpStatus.DANGER,
                created_at__gte=self.connected_at,  # Faqat bog‘lanishdan keyingi yozuvlar
            )
        )

        for help_obj in helps:
            help_data = {
                "type": "send_help",
                "id": help_obj.id,
                "user": int(self.user_id),
                "longitude": help_obj.longitude,
                "latitude": help_obj.latitude,
                "status": help_obj.status,
                "created_at": help_obj.created_at.isoformat(),
                "updated_at": help_obj.updated_at.isoformat(),
            }
            await self.send(text_data=json.dumps(help_data))
            # Xabar yuborilganligini belgilaymiz
            await self.mark_help_as_sent(help_obj)

    @database_sync_to_async
    def mark_help_as_sent(self, help_obj):
        help_obj.is_send = True
        help_obj.save()

    @database_sync_to_async
    def authenticate_user(self):
        """
        Query parametridagi JWT token yordamida foydalanuvchini autentifikatsiya qilish.
        """
        try:
            token = self.scope["query_string"].decode().split("=")[1]
            validated_token = UntypedToken(token)
            user_id = validated_token["user_id"]
            return User.objects.get(id=user_id)
        except (InvalidToken, TokenError, User.DoesNotExist):
            return AnonymousUser()
