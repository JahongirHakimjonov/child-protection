import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models.notification import Notification, NotificationType
from apps.users.tasks import send_notification_to_all_task

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created and instance.type == NotificationType.SINGLE:
        logger.info(f"Notification {instance.title} sent.")
    elif created and instance.type == NotificationType.ALL:
        send_notification_to_all_task.delay(instance.id)
        logger.info(f"Notification {instance.title} sent to all users.")
    elif created and instance.type == NotificationType.NONE:
        logger.info(f"Notification {instance.title} sent to group.")
