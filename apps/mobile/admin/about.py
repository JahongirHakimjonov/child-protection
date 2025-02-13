from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin

from apps.mobile.models.about import About, AboutProject


@admin.register(About)
class AboutAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "title", "full_name", "created_at"]
    search_fields = ["title", "full_name"]
    list_filter = ["created_at"]


@admin.register(AboutProject)
class AboutProjectAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "title", "created_at"]
    search_fields = ["title"]
    list_filter = ["created_at"]
