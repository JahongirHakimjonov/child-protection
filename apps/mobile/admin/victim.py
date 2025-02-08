from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.mobile.models.victim import Victim, VictimType, VictimStatus


@admin.register(VictimType)
class VictimTypeAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]
    list_per_page = 50


@admin.register(VictimStatus)
class VictimStatusAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]
    list_per_page = 50


@admin.register(Victim)
class VictimAdmin(ModelAdmin):
    list_display = ["id", "type", "message"]
    search_fields = ["type__name", "message"]
    list_filter = ["type"]
    autocomplete_fields = ("type", "user", "status")
    list_per_page = 50
