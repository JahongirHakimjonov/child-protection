from modeltranslation.translator import TranslationOptions, register

from apps.mobile.models.test import Test, TestQuestion, Answer


@register(Test)
class TestTranslationOptions(TranslationOptions):
    fields = ("title", "description")


@register(TestQuestion)
class TestQuestionTranslationOptions(TranslationOptions):
    fields = ("question",)


@register(Answer)
class AnswerTranslationOptions(TranslationOptions):
    fields = ("answer",)