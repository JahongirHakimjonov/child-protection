from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Help(AbstractBaseModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="help",
        verbose_name=_("user"),
    )
    longitude = models.FloatField(_("longitude"), null=True, blank=True)
    latitude = models.FloatField(_("latitude"), null=True, blank=True)
    message = models.TextField(_("message"), null=True, blank=True)
