from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Place(AbstractBaseModel):
    name = models.CharField(_("Name"), max_length=255)
    latitude = models.FloatField(_("Latitude"))
    longitude = models.FloatField(_("Longitude"))
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name = _("Place")
        verbose_name_plural = _("Places")
        ordering = ["-created_at"]
        db_table = "places"

    def __str__(self):
        return str(self.name)
