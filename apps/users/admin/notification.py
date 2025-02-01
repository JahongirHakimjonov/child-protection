from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.users.models.notification import Notification


@admin.register(Notification)
class NotificationAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ("id", "user", "message", "created_at")
    search_fields = ("user__phone", "message")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at", "updated_at")
    radio_fields = {"type": admin.VERTICAL}
