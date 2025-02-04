from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.mobile.models.places import Place


@admin.register(Place)
class PlaceAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ["id", "name", "latitude", "longitude"]
    search_fields = ["name"]
    list_filter = ["created_at", "updated_at"]
