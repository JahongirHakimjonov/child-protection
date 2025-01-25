from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.mobile.models.saved import Saved, Viewed


@admin.register(Saved)
class SavedAdmin(ModelAdmin):
    list_display = ["id", "user", "lesson"]
    search_fields = ["user", "lesson"]
    autocomplete_fields = ["user", "lesson"]


@admin.register(Viewed)
class ViewedAdmin(ModelAdmin):
    list_display = ["id", "user", "lesson"]
    search_fields = ["user", "lesson"]
    autocomplete_fields = ["user", "lesson"]
