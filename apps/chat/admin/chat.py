from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.chat.models.chat import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(ModelAdmin):
    list_display = ("id", "created_at", "updated_at")
    autocomplete_fields = ("participants",)
    search_fields = ("participants__phone",)  # Add this line


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ("id", "chat", "sender", "created_at", "updated_at")
    search_fields = ("chat__participants__username", "sender__username")
    autocomplete_fields = ("chat", "sender")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("chat", "sender")
