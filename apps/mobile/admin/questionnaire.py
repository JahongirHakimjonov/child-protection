from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline
from unfold.admin import ModelAdmin, TabularInline

from apps.mobile.models.questionnaire import (
    Questionnaire,
    QuestionnaireAnswer,
    QuestionnaireCategory,
    QuestionnaireUserAnswer,
)


class QuestionnaireAnswerInline(TabularInline, TranslationTabularInline):
    model = QuestionnaireAnswer
    extra = 0


@admin.register(QuestionnaireCategory)
class QuestionnaireCategoryAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ["id", "title", "is_active"]
    search_fields = ["title"]
    list_filter = ["is_active"]
    list_editable = ["is_active"]


@admin.register(Questionnaire)
class QuestionnaireAdmin(TabbedTranslationAdmin, ModelAdmin):
    inlines = [QuestionnaireAnswerInline]
    list_display = ["id", "category", "question", "is_active"]
    search_fields = ["question"]
    list_filter = ["category", "is_active"]
    list_editable = ["is_active"]
    autocomplete_fields = ["category"]


@admin.register(QuestionnaireAnswer)
class QuestionnaireAnswerAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ["id", "questionnaire", "answer", "is_active"]
    search_fields = ["questionnaire__question", "answer"]
    list_filter = ["questionnaire", "is_active"]
    list_editable = ["is_active"]
    autocomplete_fields = ["questionnaire"]


@admin.register(QuestionnaireUserAnswer)
class QuestionnaireUserAnswerAdmin(ModelAdmin):
    list_display = ["id", "user", "questionnaire", "created_at"]
    search_fields = ["user__phone", "questionnaire__question"]
    list_filter = ["questionnaire", "created_at"]
    date_hierarchy = "created_at"
    autocomplete_fields = ["questionnaire", "user", "answer"]
