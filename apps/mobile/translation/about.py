from modeltranslation.translator import TranslationOptions, register

from apps.mobile.models.about import About, AboutProject


@register(About)
class AboutTranslationOptions(TranslationOptions):
    fields = ("title", "description")


@register(AboutProject)
class AboutProjectTranslationOptions(TranslationOptions):
    fields = ("title", "description")
