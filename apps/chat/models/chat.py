from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class ChatRoom(AbstractBaseModel):
    """
    Chat xonasi modeli. Har bir user va adminlar o'rtasida alohida chat xonasi bo'ladi.
    """

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="chat_rooms",
        help_text="Chat xonasi user bilan bog'langan.",
    )

    def __str__(self):
        return f"Chat Room for {self.user.username}"

    class Meta:
        verbose_name = _("Chat Room")
        verbose_name_plural = _("Chat Rooms")
        ordering = ["-created_at"]
        db_table = "chat_rooms"


class Message(AbstractBaseModel):
    """
    Xabarlar modeli. Chatda yozilgan xabarlarni saqlash uchun ishlatiladi.
    """

    chat_room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name="messages",
        help_text="Xabar tegishli bo'lgan chat xonasi.",
    )
    sender = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        help_text="Xabarni yuborgan foydalanuvchi.",
    )
    text = models.TextField(blank=True, null=True, help_text="Xabar matni.")
    file = models.FileField(
        upload_to="chat_files/",
        blank=True,
        null=True,
        help_text="Foydalanuvchi yuborgan fayl.",
    )
    is_admin = models.BooleanField(
        default=False, help_text="Xabar admin tomonidan yuborilganligini bildiradi."
    )

    def __str__(self):
        sender_type = "Admin" if self.is_admin else "User"
        return f"{sender_type} ({self.sender.username}): {self.text[:30] if self.text else 'File Message'}"

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ["-created_at"]
        db_table = "messages"
