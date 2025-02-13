from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class About(AbstractBaseModel):
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    full_name = models.CharField(_("Full Name"), max_length=255)
    image = models.ImageField(_("Image"), upload_to="about/")

    class Meta:
        verbose_name = _("About")
        verbose_name_plural = _("Abouts")
        ordering = ["-created_at"]
        db_table = "about"

    def __str__(self):
        return self.title


class AboutProject(AbstractBaseModel):
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    image = models.ImageField(_("Image"), upload_to="about/")

    class Meta:
        verbose_name = _("About Project")
        verbose_name_plural = _("About Projects")
        ordering = ["-created_at"]
        db_table = "about_project"

    def __str__(self):
        return self.title
