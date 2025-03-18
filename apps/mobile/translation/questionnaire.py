from modeltranslation.translator import TranslationOptions, register

from apps.mobile.models.questionnaire import (
    Questionnaire,
    QuestionnaireCategory,
    QuestionnaireAnswer,
)


@register(QuestionnaireCategory)
class QuestionnaireCategoryTranslationOptions(TranslationOptions):
    fields = ("title", "description")


@register(Questionnaire)
class QuestionnaireTranslationOptions(TranslationOptions):
    fields = ("question",)


@register(QuestionnaireAnswer)
class QuestionnaireAnswerTranslationOptions(TranslationOptions):
    fields = ("answer",)
