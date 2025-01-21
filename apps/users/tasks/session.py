from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from apps.users.models import ActiveSessions


@shared_task()
def in_activate_sessions():
    now = timezone.now()
    one_day_before_expiry = now + timedelta(days=1)

    # Deactivate sessions where expiry is within 1 day
    sessions_to_deactivate = ActiveSessions.objects.filter(
        expired_at__lt=one_day_before_expiry
    )
    sessions_to_deactivate.update(is_active=False)

    return "Inactivated sessions"
