# Generated by Django 5.1.5 on 2025-01-25 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mobile", "0012_viewed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courselessonresource",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("VIDEO", "Video"),
                    ("AUDIO", "Audio"),
                    ("DOCUMENT", "Document"),
                ],
                db_index=True,
                max_length=255,
                null=True,
            ),
        ),
    ]
