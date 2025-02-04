from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline
from apps.mobile.models.test import Answer, TestQuestion, Test


class AnswerInline(TabularInline, TranslationTabularInline):
    model = Answer
    extra = 0


class TestQuestionInline(TabularInline, TranslationTabularInline):
    model = TestQuestion
    extra = 0


@admin.register(Answer)
class AnswerAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "answer", "type"]
    search_fields = ["answer", "type"]
    list_filter = ["type"]
    autocomplete_fields = ["question"]


@admin.register(TestQuestion)
class TestQuestionAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "test", "question"]
    search_fields = ["test", "question"]
    list_filter = ["test"]
    autocomplete_fields = ["test"]
    inlines = [AnswerInline]


@admin.register(Test)
class TestAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["id", "title", "description"]
    search_fields = ["title", "description"]
    list_filter = ["title"]
    autocomplete_fields = ["lesson"]
    inlines = [TestQuestionInline]
