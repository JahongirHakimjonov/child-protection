from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusChoice(models.TextChoices):
    ACTIVE = "ACTIVE", _("Active")
    PENDING = "PENDING", _("Pending")
    REJECTED = "REJECTED", _("Rejected")
