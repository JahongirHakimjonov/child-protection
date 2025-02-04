from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.mobile.models.news import News


@admin.register(News)
class NewsAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "title", "is_active"]
    search_fields = ["title", "description"]
    readonly_fields = ["created_at", "updated_at"]
