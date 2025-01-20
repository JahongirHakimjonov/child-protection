from modeltranslation.translator import TranslationOptions, register

from apps.users.models import Notification


@register(Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = ("title", "message")
