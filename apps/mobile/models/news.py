from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class News(AbstractBaseModel):
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("content"))
    banner = models.ImageField(upload_to="news/", null=True, blank=True)
    view_count = models.PositiveBigIntegerField(
        _("view count"), default=0, db_index=True, null=True, blank=True
    )
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ["-created_at"]
        db_table = "news"

    def __str__(self) -> str:
        return str(self.title)

    def increase_view_count(self):
        self.view_count += 1
        self.save()
