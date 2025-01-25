from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.mobile.models.test import Answer, TestQuestion, Test


@admin.register(Answer)
class AnswerAdmin(ModelAdmin):
    list_display = ["id", "answer", "type"]
    search_fields = ["answer", "type"]
    list_filter = ["type"]
    autocomplete_fields = ["question"]


@admin.register(TestQuestion)
class TestQuestionAdmin(ModelAdmin):
    list_display = ["id", "test", "question"]
    search_fields = ["test", "question"]
    list_filter = ["test"]
    autocomplete_fields = ["test"]


@admin.register(Test)
class TestAdmin(ModelAdmin):
    list_display = ["id", "title", "description"]
    search_fields = ["title", "description"]
    list_filter = ["title"]
    autocomplete_fields = ["lesson"]
