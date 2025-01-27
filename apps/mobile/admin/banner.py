from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.mobile.models.banner import Banner


@admin.register(Banner)
class BannerAdmin(ModelAdmin):
    list_display = ["image", "link", "is_active"]
    list_filter = ["is_active"]
