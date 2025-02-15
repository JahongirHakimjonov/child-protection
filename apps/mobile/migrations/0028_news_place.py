# Generated by Django 5.1.5 on 2025-02-04 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mobile", "0027_answer_answer_en_answer_answer_ru_answer_answer_uz_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="News",
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
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "title_uz",
                    models.CharField(max_length=255, null=True, verbose_name="title"),
                ),
                (
                    "title_ru",
                    models.CharField(max_length=255, null=True, verbose_name="title"),
                ),
                (
                    "title_en",
                    models.CharField(max_length=255, null=True, verbose_name="title"),
                ),
                ("description", models.TextField(verbose_name="content")),
                ("description_uz", models.TextField(null=True, verbose_name="content")),
                ("description_ru", models.TextField(null=True, verbose_name="content")),
                ("description_en", models.TextField(null=True, verbose_name="content")),
                ("banner", models.ImageField(blank=True, null=True, upload_to="news/")),
                ("is_active", models.BooleanField(db_index=True, default=True)),
            ],
            options={
                "verbose_name": "News",
                "verbose_name_plural": "News",
                "db_table": "news",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Place",
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
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                (
                    "name_uz",
                    models.CharField(max_length=255, null=True, verbose_name="Name"),
                ),
                (
                    "name_ru",
                    models.CharField(max_length=255, null=True, verbose_name="Name"),
                ),
                (
                    "name_en",
                    models.CharField(max_length=255, null=True, verbose_name="Name"),
                ),
                ("latitude", models.FloatField(verbose_name="Latitude")),
                ("longitude", models.FloatField(verbose_name="Longitude")),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is Active"),
                ),
            ],
            options={
                "verbose_name": "Place",
                "verbose_name_plural": "Places",
                "db_table": "places",
                "ordering": ["-created_at"],
            },
        ),
    ]
