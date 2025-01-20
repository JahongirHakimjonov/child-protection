# from django.db import models
#
# from apps.shared.models import AbstractBaseModel
#
# from django.utils.translation import gettext_lazy as _
#
#
# class Support(AbstractBaseModel):
#     name = models.CharField(max_length=255, verbose_name=_("Ism"))
#     email = models.EmailField(max_length=255, verbose_name=_("Email"))
#     message = models.TextField(verbose_name=_("Xabar"))
#
#     class Meta:
#         verbose_name = _("Qo'llab-quvvat")
#         verbose_name_plural = _("Qo'llab-quvvatlar")
#         ordering = ("-created_at",)
#         db_table = "support"
#
#     def __str__(self):
#         return self.name
