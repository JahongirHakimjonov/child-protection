from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.users.models import SmsConfirm


@admin.register(SmsConfirm)
class SmsConfirmAdmin(ModelAdmin):
    list_display = ["id", "phone", "code", "created_at"]
    search_fields = ["phone"]
    list_filter = ["created_at"]
    ordering = ["-created_at"]
    readonly_fields = ["phone", "code", "created_at"]
    fieldsets = ((None, {"fields": ("phone", "code", "created_at")}),)
    add_fieldsets = ((None, {"fields": ("phone", "code")}),)
