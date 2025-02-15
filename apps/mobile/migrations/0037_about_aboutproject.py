# Generated by Django 5.1.5 on 2025-02-13 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mobile", "0036_alter_victimstatus_is_pending"),
    ]

    operations = [
        migrations.CreateModel(
            name="About",
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
                ("title", models.CharField(max_length=255, verbose_name="Title")),
                (
                    "title_uz",
                    models.CharField(max_length=255, null=True, verbose_name="Title"),
                ),
                (
                    "title_ru",
                    models.CharField(max_length=255, null=True, verbose_name="Title"),
                ),
                (
                    "title_en",
                    models.CharField(max_length=255, null=True, verbose_name="Title"),
                ),
                ("description", models.TextField(verbose_name="Description")),
                (
                    "description_uz",
                    models.TextField(null=True, verbose_name="Description"),
                ),
                (
                    "description_ru",
                    models.TextField(null=True, verbose_name="Description"),
                ),
                (
                    "description_en",
                    models.TextField(null=True, verbose_name="Description"),
                ),
                (
                    "full_name",
                    models.CharField(max_length=255, verbose_name="Full Name"),
                ),
                ("image", models.ImageField(upload_to="about/", verbose_name="Image")),
            ],
            options={
                "verbose_name": "About",
                "verbose_name_plural": "Abouts",
                "db_table": "about",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="AboutProject",
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
                ("title", models.CharField(max_length=255, verbose_name="Title")),
                (
                    "title_uz",
                    models.CharField(max_length=255, null=True, verbose_name="Title"),
                ),
                (
                    "title_ru",
                    models.CharField(max_length=255, null=True, verbose_name="Title"),
                ),
                (
                    "title_en",
                    models.CharField(max_length=255, null=True, verbose_name="Title"),
                ),
                ("description", models.TextField(verbose_name="Description")),
                (
                    "description_uz",
                    models.TextField(null=True, verbose_name="Description"),
                ),
                (
                    "description_ru",
                    models.TextField(null=True, verbose_name="Description"),
                ),
                (
                    "description_en",
                    models.TextField(null=True, verbose_name="Description"),
                ),
                ("image", models.ImageField(upload_to="about/", verbose_name="Image")),
            ],
            options={
                "verbose_name": "About Project",
                "verbose_name_plural": "About Projects",
                "db_table": "about_project",
                "ordering": ["-created_at"],
            },
        ),
    ]
