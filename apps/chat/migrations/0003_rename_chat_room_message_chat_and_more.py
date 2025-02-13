# Generated by Django 5.0.8 on 2025-01-23 11:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0002_alter_chatroom_options_alter_message_options_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name="message",
            old_name="chat_room",
            new_name="chat",
        ),
        migrations.RenameField(
            model_name="message",
            old_name="text",
            new_name="message",
        ),
        migrations.RemoveField(
            model_name="chatroom",
            name="user",
        ),
        migrations.AddField(
            model_name="chatroom",
            name="participants",
            field=models.ManyToManyField(
                related_name="chats", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="sender",
            field=models.ForeignKey(
                help_text="Xabarni yuborgan foydalanuvchi.",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sent_messages",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
