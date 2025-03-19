from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class QuestionnaireCategory(AbstractBaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"), null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    class Meta:
        verbose_name = _("Questionnaire Category")
        verbose_name_plural = _("Questionnaires Category")

    def __str__(self):
        return str(self.title)


class Questionnaire(AbstractBaseModel):
    category = models.ForeignKey(
        "QuestionnaireCategory",
        on_delete=models.CASCADE,
        related_name="questionnaires",
        db_index=True,
    )
    question = models.TextField(verbose_name=_("Question"), db_index=True)
    is_text_answer = models.BooleanField(
        verbose_name=_("Is text answer"), default=False, db_index=True
    )
    is_active = models.BooleanField(
        verbose_name=_("Is active"), default=True, db_index=True
    )

    class Meta:
        verbose_name = _("Questionnaire")
        verbose_name_plural = _("Questionnaires")
        ordering = ("created_at",)
        db_table = "questionnaire"

    def __str__(self):
        return self.question


class QuestionnaireAnswer(AbstractBaseModel):
    questionnaire = models.ForeignKey(
        "Questionnaire",
        on_delete=models.CASCADE,
        related_name="answers",
        db_index=True,
    )
    answer = models.TextField(verbose_name=_("Answer"), db_index=True)
    is_active = models.BooleanField(
        verbose_name=_("Is active"), default=True, db_index=True
    )

    class Meta:
        verbose_name = _("Questionnaire Answer")
        verbose_name_plural = _("Questionnaire Answers")
        ordering = ("-created_at",)
        db_table = "questionnaire_answer"

    def __str__(self):
        return self.answer


class QuestionnaireUserAnswer(AbstractBaseModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="questionnaire_answers",
        db_index=True,
    )
    category = models.ForeignKey(
        "QuestionnaireCategory",
        on_delete=models.CASCADE,
        related_name="user_answers",
        db_index=True,
    )

    class Meta:
        verbose_name = _("Questionnaire User Answer")
        verbose_name_plural = _("Questionnaire User Answers")
        ordering = ("-updated_at",)
        db_table = "questionnaire_user_answer"

    def __str__(self):
        return str(self.user.id)


class QuestionnaireUserAnswerDetail(AbstractBaseModel):
    user_answer = models.ForeignKey(
        "QuestionnaireUserAnswer",
        on_delete=models.CASCADE,
        related_name="user_answer_details",
        db_index=True,
    )
    questionnaire = models.ForeignKey(
        "Questionnaire",
        on_delete=models.CASCADE,
        related_name="user_answers",
        db_index=True,
    )
    answer = models.ForeignKey(
        "QuestionnaireAnswer",
        on_delete=models.CASCADE,
        related_name="user_answers",
        db_index=True,
        null=True,
        blank=True,
    )
    answer_text = models.TextField(
        verbose_name=_("Answer text"), db_index=True, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Questionnaire User Answer Detail")
        verbose_name_plural = _("Questionnaire User Answer Details")
        ordering = ("-updated_at",)
        db_table = "questionnaire_user_answer_detail"

    def __str__(self):
        return str(self.user_answer.id)
