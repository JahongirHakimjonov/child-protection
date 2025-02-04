from modeltranslation.translator import TranslationOptions, register

from apps.mobile.models.question import Question, QuestionCategory


@register(QuestionCategory)
class QuestionCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ("title", "description")
