from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from apps.mobile.models.faq import FAQ


@admin.register(FAQ)
class FAQAdmin(ModelAdmin):
    list_display = ["question", "is_active"]
    search_fields = ["question", "answer"]
    list_filter = ["is_active"]
    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
    }
