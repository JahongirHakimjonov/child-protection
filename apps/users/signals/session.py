from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import Notification, NotificationType
from apps.users.models import ActiveSessions


@receiver(post_save, sender=ActiveSessions)
def increment_active_sessions(sender, instance, created, **kwargs):  # noqa
    if created:
        address = f"{instance.location.get('country', '')}, {instance.location.get('city', '')}"
        latitude = instance.location.get("lat", "")
        longitude = instance.location.get("lon", "")
        coordinates = f"{latitude}, {longitude}"
        ip = instance.ip
        device = instance.user_agent
        isp = instance.location.get("isp", "")
        timezone = instance.location.get("timezone", "")
        created_at = instance.created_at.strftime("%Y-%m-%d  %H:%M:%S")

        messages = {
            "uz": f"Akkauntizga soat {created_at} da {address} dan kirildi, Kordinatalar: {coordinates}, IP: {ip}, Qurilma: {device}, ISP: {isp}, Timezone: {timezone}",
            "ru": f"Ваш аккаунт был вошел в {created_at} из {address}, Координаты: {coordinates}, IP: {ip}, Устройство: {device}, ISP: {isp}, Timezone: {timezone}",
        }

        Notification.objects.create(
            user_id=instance.user_id,
            title_uz="Yangi kirish",
            title_ru="Новый вход",
            message_uz=messages["uz"],
            message_ru=messages["ru"],
            type=NotificationType.SINGLE,
        )
