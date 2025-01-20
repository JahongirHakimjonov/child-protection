from datetime import timedelta

import requests
from celery import shared_task
from django.utils import timezone

from apps.users.models import ActiveSessions


@shared_task(name="apps.users.tasks.session.in_activate_sessions", queue="cron")
def in_activate_sessions():
    now = timezone.now()
    one_day_before_expiry = now + timedelta(days=1)

    # Deactivate sessions where expiry is within 1 day
    sessions_to_deactivate = ActiveSessions.objects.filter(
        expired_at__lt=one_day_before_expiry
    )
    sessions_to_deactivate.update(is_active=False)

    url = "https://api.telegram.org/bot1165698137:AAE3cRK3DlSXkwgKRUzaXbDrDJpvhV-X7jo/sendMessage"
    params = {"chat_id": "483578239", "text": "Inactivated sessions"}
    requests.get(url, params=params)
    return "Inactivated sessions"
