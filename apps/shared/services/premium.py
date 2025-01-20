from django.utils import timezone

from apps.panda.models import CinemaVideo
from apps.payment.models import Subscription


class PremiumService:
    @staticmethod
    def has_access(user_id, cinema_id):
        """
        Tekshiradi, agar foydalanuvchi premium statusga ega bo'lsa va berilgan cinema_id uchun ruxsat mavjud bo'lsa.

        :param user_id: Foydalanuvchi IDsi
        :param cinema_id: Cinema IDsi
        :return: True yoki False
        """
        now = timezone.now()

        # CinemaVideo ni olish
        cinema_video = (
            CinemaVideo.objects.filter(id=cinema_id).select_related("cinema").first()
        )
        if not cinema_video:
            return False

        # Agar kino pullik bo'lmasa, ruxsat beriladi
        if not cinema_video.cinema.is_paid:
            return True

        # Foydalanuvchi IDsi asosida tekshirish
        subscriptions = (
            Subscription.objects.filter(
                user_id=user_id, start_date__lte=now, end_date__gte=now, is_active=True
            )
            .select_related("order__plan")
            .prefetch_related("order__plan__category")
        )

        for subscription in subscriptions:
            if cinema_video.cinema.category in subscription.order.plan.category.all():
                return True

        return False
