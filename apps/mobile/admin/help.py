from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.mobile.models.help import Help


@admin.register(Help)
class HelpAdmin(ModelAdmin):
    list_display = ("id", "user", "longitude", "latitude", "message")
    search_fields = ("user__email",)
    list_filter = ("created_at",)
    autocomplete_fields = ("user",)
