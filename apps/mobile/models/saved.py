from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Saved(AbstractBaseModel):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="saved", db_index=True
    )
    course = models.ForeignKey(
        "Course", on_delete=models.CASCADE, related_name="saved", db_index=True
    )

    class Meta:
        verbose_name = _("Saved")
        verbose_name_plural = _("Saved")
        ordering = ["-created_at"]
        db_table = "saved"

    def __str__(self) -> str:
        return f"{self.user} - {self.course}"
