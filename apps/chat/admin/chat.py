from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.chat.models.chat import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(ModelAdmin):
    list_display = ("user", "created_at", "updated_at")
    search_fields = ("user__username",)
    list_filter = ("user",)
    autocomplete_fields = ("user",)


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ("chat_room", "sender", "created_at", "updated_at")
    search_fields = ("chat_room__user__username", "sender__username")
    list_filter = ("chat_room", "sender")
    autocomplete_fields = ("chat_room", "sender")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("chat_room", "sender")
