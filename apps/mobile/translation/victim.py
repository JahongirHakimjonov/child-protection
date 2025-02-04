from modeltranslation.translator import TranslationOptions, register

from apps.mobile.models.victim import VictimType


@register(VictimType)
class VictimTypeTranslationOptions(TranslationOptions):
    fields = ("name",)
