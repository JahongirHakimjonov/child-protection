from django.urls import re_path, path

from apps.chat.consumers.chat import ChatConsumer
from apps.chat.consumers.notification import NotificationConsumer
from apps.chat.views.chat import ChatRoomList, MessageList, ChatResourceView

urlpatterns = [
    path("chat/", ChatRoomList.as_view(), name="chat"),
    path("chat/resource/", ChatResourceView.as_view(), name="chat-resource"),
    path("message/<int:chat_id>/", MessageList.as_view(), name="message"),
]

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<chat_room_id>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/notification/$", NotificationConsumer.as_asgi()),
]
