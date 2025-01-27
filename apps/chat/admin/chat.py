from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.chat.models.chat import ChatRoom, Message, ChatResource


@admin.register(ChatRoom)
class ChatRoomAdmin(ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at")
    autocomplete_fields = ("participants",)
    search_fields = ("participants__phone",)


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ("id", "chat", "sender", "created_at", "updated_at")
    search_fields = ("chat__participants__username", "sender__username")
    autocomplete_fields = ("chat", "sender", "file")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("chat", "sender")


@admin.register(ChatResource)
class ChatResourceAdmin(ModelAdmin):
    list_display = ("id", "user", "file", "created_at")
    autocomplete_fields = ("user",)
    search_fields = ("file", "user__first_name")
    readonly_fields = ("name", "size", "type", "created_at")
