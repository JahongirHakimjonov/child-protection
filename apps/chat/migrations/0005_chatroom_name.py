# Generated by Django 5.1.5 on 2025-01-24 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0004_message_is_sent"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatroom",
            name="name",
            field=models.CharField(
                blank=True, help_text="Chat nomi.", max_length=255, null=True
            ),
        ),
    ]