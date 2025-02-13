# Generated by Django 5.1.5 on 2025-01-24 11:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0005_chatroom_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ChatResource",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(help_text="Fayl nomi.", max_length=255)),
                (
                    "file",
                    models.FileField(
                        help_text="Foydalanuvchi yuborgan fayl.",
                        upload_to="chat_resources/",
                    ),
                ),
                (
                    "size",
                    models.PositiveIntegerField(
                        blank=True, help_text="Fayl hajmi (byte).", null=True
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        blank=True, help_text="Fayl turi.", max_length=255, null=True
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="Foydalanuvchi.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chat_resources",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AlterField(
            model_name="message",
            name="file",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="chat.chatresource",
            ),
        ),
    ]
