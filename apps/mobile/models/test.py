from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class AnswerType(models.TextChoices):
    RADIO = "RADIO", _("Radio")
    CHECKBOX = "CHECKBOX", _("Checkbox")


class Test(AbstractBaseModel):
    lesson = models.ForeignKey(
        "CourseLesson",
        on_delete=models.CASCADE,
        related_name="questions",
        db_index=True,
    )
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(db_index=True)
    banner = models.ImageField(upload_to="test", null=True, blank=True, db_index=True)
    question_count = models.PositiveBigIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = _("Test")
        verbose_name_plural = _("Tests")
        ordering = ("-created_at",)
        db_table = "test"

    def __str__(self):
        return self.title


class TestQuestion(AbstractBaseModel):
    test = models.ForeignKey(
        "Test", on_delete=models.CASCADE, related_name="questions", db_index=True
    )
    question = models.TextField(verbose_name=_("Question"), db_index=True)
    is_active = models.BooleanField(
        verbose_name=_("Is active"), default=True, db_index=True
    )

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ("-created_at",)
        db_table = "question"

    def __str__(self):
        return self.question


class Answer(AbstractBaseModel):
    question = models.ForeignKey(
        TestQuestion, on_delete=models.CASCADE, related_name="answers", db_index=True
    )
    answer = models.TextField(db_index=True)
    type = models.CharField(
        verbose_name=_("Type"),
        max_length=10,
        choices=AnswerType,
        default=AnswerType.RADIO,
        db_index=True,
    )
    ball = models.IntegerField(verbose_name=_("Ball"), default=0, db_index=True)
    is_correct = models.BooleanField(
        verbose_name=_("Is correct"), default=False, db_index=True
    )

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        ordering = ("-created_at",)
        db_table = "answer"

    def __str__(self):
        return self.answer
