from modeltranslation.translator import TranslationOptions, register

from apps.mobile.models.victim import VictimType, VictimStatus


@register(VictimType)
class VictimTypeTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(VictimStatus)
class VictimStatusTranslationOptions(TranslationOptions):
    fields = ("name",)
