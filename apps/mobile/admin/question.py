from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from apps.mobile.models.question import QuestionCategory, Question


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ["id", "category", "title"]
    search_fields = ["title"]
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["category"]
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
