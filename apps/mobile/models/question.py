from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class QuestionCategory(AbstractBaseModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    image = models.ImageField(upload_to="question_categories/", null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = _("Question Category")
        verbose_name_plural = _("Question Categories")
        ordering = ["name"]
        db_table = "question_categories"

    def __str__(self) -> str:
        return str(self.name)


class Question(AbstractBaseModel):
    category = models.ForeignKey(
        QuestionCategory,
        on_delete=models.CASCADE,
        related_name="questions",
        db_index=True,
    )
    sort_number = models.PositiveIntegerField(
        db_index=True, verbose_name=_("Sort number"), null=True, blank=True
    )
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ["sort_number"]
        db_table = "questions"

    def __str__(self) -> str:
        return str(self.title)
