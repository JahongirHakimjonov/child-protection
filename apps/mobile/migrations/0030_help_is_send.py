# Generated by Django 5.1.5 on 2025-02-07 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mobile", "0029_alter_question_sort_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="help",
            name="is_send",
            field=models.BooleanField(default=False, verbose_name="is send"),
        ),
    ]
