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


class VictimStatus(AbstractBaseModel):
    name = models.CharField(_("name"), max_length=255, db_index=True)
    is_pending = models.BooleanField(_("is pending"), default=False, db_index=True)

    class Meta:
        verbose_name = _("victim status")
        verbose_name_plural = _("victim statuses")
        ordering = ["name"]
        db_table = "victim_statuses"

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
    answer = models.TextField(_("answer"), blank=True, null=True, db_index=True)
    status = models.ForeignKey(
        VictimStatus,
        verbose_name=_("status"),
        related_name="victims",
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("victim")
        verbose_name_plural = _("victims")
        ordering = ["-created_at"]
        db_table = "victims"

    def __str__(self):
        return str(self.user)
