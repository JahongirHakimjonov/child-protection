from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Banner(AbstractBaseModel):
    image = models.ImageField(upload_to="banners/", null=True, blank=True)
    link = models.URLField(max_length=255, db_index=True, null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = _("Banner")
        verbose_name_plural = _("Banners")
        ordering = ["-created_at"]
        db_table = "banners"

    def __str__(self) -> str:
        return str(self.image)
