from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Saved(AbstractBaseModel):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="saved", db_index=True
    )
    lesson = models.ForeignKey(
        "CourseLesson", on_delete=models.CASCADE, related_name="saved", db_index=True
    )

    class Meta:
        verbose_name = _("Saved")
        verbose_name_plural = _("Saved")
        ordering = ["-created_at"]
        db_table = "saved"
        unique_together = ["user", "lesson"]

    def __str__(self) -> str:
        return f"{self.user} - {self.lesson}"


class Viewed(AbstractBaseModel):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="viewed", db_index=True
    )
    lesson = models.ForeignKey(
        "CourseLesson", on_delete=models.CASCADE, related_name="viewed", db_index=True
    )

    class Meta:
        verbose_name = _("Viewed")
        verbose_name_plural = _("Viewed")
        ordering = ["-created_at"]
        db_table = "viewed"
        unique_together = ["user", "lesson"]

    def __str__(self) -> str:
        return f"{self.user} - {self.lesson}"
