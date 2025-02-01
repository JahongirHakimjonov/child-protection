from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class VictimType(AbstractBaseModel):
    name = models.CharField(_("name"), max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(_("is active"), default=True, db_index=True)

    class Meta:
        verbose_name = _("victim type")
        verbose_name_plural = _("victim types")
        ordering = ["name"]
        db_table = "victim_types"

    def __str__(self):
        return str(self.name)


class Victim(AbstractBaseModel):
    user = models.ForeignKey(
        "users.User",
        verbose_name=_("user"),
        related_name="victims",
        on_delete=models.CASCADE,
        db_index=True,
    )
    type = models.ForeignKey(
        VictimType,
        verbose_name=_("type"),
        related_name="victims",
        on_delete=models.CASCADE,
        db_index=True,
    )
    message = models.TextField(_("message"), db_index=True)
