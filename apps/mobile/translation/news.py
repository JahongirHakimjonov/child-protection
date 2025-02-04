from modeltranslation.translator import TranslationOptions, register

from apps.mobile.models.news import News


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ("title", "description")
