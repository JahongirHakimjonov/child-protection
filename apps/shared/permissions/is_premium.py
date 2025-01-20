from django.utils import timezone
from rest_framework.permissions import BasePermission

from apps.panda.models import CinemaVideo
from apps.payment.models import Subscription


class IsPremium(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        now = timezone.now()

        cinema_id = request.query_params.get("cinema_id")
        if not cinema_id:
            return False

        cinema_video = (
            CinemaVideo.objects.filter(cinema__id=cinema_id)
            .select_related("cinema")
            .first()
        )
        if not cinema_video:
            return False

        if not cinema_video.cinema.is_paid:
            return True

        if not user.is_authenticated or not user.is_premium:
            return False

        subscriptions = (
            Subscription.objects.filter(
                user=user, start_date__lte=now, end_date__gte=now, is_active=True
            )
            .select_related("order__plan")
            .prefetch_related("order__plan__category")
        )

        for subscription in subscriptions:
            if cinema_video.cinema.category in subscription.order.plan.category.all():
                return True

        return False
