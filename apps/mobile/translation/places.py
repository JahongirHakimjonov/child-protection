from modeltranslation.translator import TranslationOptions, register

from apps.mobile.models.places import Place


@register(Place)
class PlaceTranslationOptions(TranslationOptions):
    fields = ["name"]
