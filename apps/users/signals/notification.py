import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import Notification, NotificationType
from apps.users.tasks import send_notification_task, send_notification_to_all_task

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):  # noqa
    if created and instance.type == NotificationType.SINGLE:
        send_notification_task.apply_async(args=(instance.id,), queue="notifications")
        logger.info(f"Notification {instance.title} sent.")
    elif created and instance.type == NotificationType.ALL:
        send_notification_to_all_task.apply_async(
            args=(instance.id,), queue="notifications_all"
        )
        logger.info(f"Notification {instance.title} sent to all users.")
    elif created and instance.type == NotificationType.NONE:
        logger.info(f"Notification {instance.title} sent to group.")