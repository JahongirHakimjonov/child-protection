# Generated by Django 5.1.5 on 2025-02-08 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mobile", "0034_alter_victim_options_alter_victimstatus_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="victimstatus",
            name="is_active",
        ),
        migrations.AddField(
            model_name="victimstatus",
            name="is_pending",
            field=models.BooleanField(
                db_index=True, default=False, verbose_name="is active"
            ),
        ),
    ]
