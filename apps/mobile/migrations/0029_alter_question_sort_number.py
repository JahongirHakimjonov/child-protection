# Generated by Django 5.1.5 on 2025-02-07 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mobile", "0028_news_place"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="sort_number",
            field=models.PositiveIntegerField(
                blank=True, db_index=True, null=True, verbose_name="Sort number"
            ),
        ),
    ]
