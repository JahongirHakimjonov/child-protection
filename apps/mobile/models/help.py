from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class HelpStatus(models.TextChoices):
    SAFE = "SAFE", _("Safe")
    DANGER = "DANGER", _("Danger")


class Help(AbstractBaseModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="help",
        verbose_name=_("user"),
    )
    longitude = models.FloatField(_("longitude"), null=True, blank=True)
    latitude = models.FloatField(_("latitude"), null=True, blank=True)
    status = models.CharField(
        _("status"), max_length=6, choices=HelpStatus, default=HelpStatus.SAFE
    )
    is_send = models.BooleanField(_("is send"), default=False)

    class Meta:
        verbose_name = _("help")
        verbose_name_plural = _("helps")
        db_table = "helps"
