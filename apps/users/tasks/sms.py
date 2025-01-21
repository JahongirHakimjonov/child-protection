from celery import shared_task
from django.utils.translation import gettext_lazy as _

from apps.users.services import SendService
from apps.shared.utils import console


@shared_task()
def send_confirm(phone, code):
    try:
        service: SendService = SendService()
        service.send_sms(
            phone,
            _("Ro'yxatdan o'tishingiz uchun tasdiqlash kodi: %(code)s")
            % {"code": code},
        )
        console.Console().success(f"Success: {phone}-{code}")
    except Exception as e:
        console.Console().error(
            "Error: {phone}-{code}\n\n{error}".format(phone=phone, code=code, error=e)
        )  # noqa
