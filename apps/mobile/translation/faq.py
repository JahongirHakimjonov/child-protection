from modeltranslation.translator import TranslationOptions, register

from apps.mobile.models.faq import FAQ


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ("question", "answer")
