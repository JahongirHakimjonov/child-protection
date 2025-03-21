# Generated by Django 5.1.5 on 2025-02-21 06:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

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
        migrations.CreateModel(
            name="Answer",
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
                ("answer", models.TextField(db_index=True)),
                ("answer_uz", models.TextField(db_index=True, null=True)),
                ("answer_ru", models.TextField(db_index=True, null=True)),
                ("answer_en", models.TextField(db_index=True, null=True)),
                (
                    "type",
                    models.CharField(
                        choices=[("RADIO", "Radio"), ("CHECKBOX", "Checkbox")],
                        db_index=True,
                        default="RADIO",
                        max_length=10,
                        verbose_name="Type",
                    ),
                ),
                (
                    "ball",
                    models.IntegerField(db_index=True, default=0, verbose_name="Ball"),
                ),
                (
                    "is_correct",
                    models.BooleanField(
                        db_index=True, default=False, verbose_name="Is correct"
                    ),
                ),
            ],
            options={
                "verbose_name": "Answer",
                "verbose_name_plural": "Answers",
                "db_table": "answer",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="Banner",
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
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="banners/"),
                ),
                (
                    "link",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="link"
                    ),
                ),
                ("is_active", models.BooleanField(db_index=True, default=True)),
            ],
            options={
                "verbose_name": "Banner",
                "verbose_name_plural": "Banners",
                "db_table": "banners",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="CourseCategory",
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
                ("title", models.TextField(db_index=True)),
                ("title_uz", models.TextField(db_index=True, null=True)),
                ("title_ru", models.TextField(db_index=True, null=True)),
                ("title_en", models.TextField(db_index=True, null=True)),
                ("sub_title", models.TextField(blank=True, db_index=True, null=True)),
                (
                    "sub_title_uz",
                    models.TextField(blank=True, db_index=True, null=True),
                ),
                (
                    "sub_title_ru",
                    models.TextField(blank=True, db_index=True, null=True),
                ),
                (
                    "sub_title_en",
                    models.TextField(blank=True, db_index=True, null=True),
                ),
                ("description", models.TextField(blank=True, db_index=True, null=True)),
                (
                    "description_uz",
                    models.TextField(blank=True, db_index=True, null=True),
                ),
                (
                    "description_ru",
                    models.TextField(blank=True, db_index=True, null=True),
                ),
                (
                    "description_en",
                    models.TextField(blank=True, db_index=True, null=True),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="course_categories/"
                    ),
                ),
                ("lesson_count", models.PositiveIntegerField(db_index=True, default=0)),
                (
                    "first_color",
                    models.CharField(
                        blank=True, db_index=True, max_length=255, null=True
                    ),
                ),
                (
                    "second_color",
                    models.CharField(
                        blank=True, db_index=True, max_length=255, null=True
                    ),
                ),
                ("is_active", models.BooleanField(db_index=True, default=True)),
            ],
            options={
                "verbose_name": "Course Category",
                "verbose_name_plural": "Course Categories",
                "db_table": "course_categories",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="FAQ",
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
                ("question", models.TextField(verbose_name="Question")),
                ("question_uz", models.TextField(null=True, verbose_name="Question")),
                ("question_ru", models.TextField(null=True, verbose_name="Question")),
                ("question_en", models.TextField(null=True, verbose_name="Question")),
                ("answer", models.TextField(verbose_name="Answer")),
                ("answer_uz", models.TextField(null=True, verbose_name="Answer")),
                ("answer_ru", models.TextField(null=True, verbose_name="Answer")),
                ("answer_en", models.TextField(null=True, verbose_name="Answer")),
                (
                    "is_active",
                    models.BooleanField(default=True, verbose_name="Is Active"),
                ),
            ],
            options={
                "verbose_name": "FAQ",
                "verbose_name_plural": "FAQs",
                "db_table": "faq",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Help",
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
                (
                    "longitude",
                    models.FloatField(blank=True, null=True, verbose_name="longitude"),
                ),
                (
                    "latitude",
                    models.FloatField(blank=True, null=True, verbose_name="latitude"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("SAFE", "Safe"), ("DANGER", "Danger")],
                        default="SAFE",
                        max_length=6,
                        verbose_name="status",
                    ),
                ),
                ("is_send", models.BooleanField(default=False, verbose_name="is send")),
            ],
            options={
                "verbose_name": "help",
                "verbose_name_plural": "helps",
                "db_table": "helps",
            },
        ),
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
                (
                    "view_count",
                    models.PositiveBigIntegerField(
                        blank=True,
                        db_index=True,
                        default=0,
                        null=True,
                        verbose_name="view count",
                    ),
                ),
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
        migrations.CreateModel(
            name="Question",
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
                (
                    "sort_number",
                    models.PositiveIntegerField(
                        blank=True, db_index=True, null=True, verbose_name="Sort number"
                    ),
                ),
                ("title", models.CharField(db_index=True, max_length=255)),
                (
                    "title_uz",
                    models.CharField(db_index=True, max_length=255, null=True),
                ),
                (
                    "title_ru",
                    models.CharField(db_index=True, max_length=255, null=True),
                ),
                (
                    "title_en",
                    models.CharField(db_index=True, max_length=255, null=True),
                ),
                ("description", models.TextField(db_index=True)),
                ("description_uz", models.TextField(db_index=True, null=True)),
                ("description_ru", models.TextField(db_index=True, null=True)),
                ("description_en", models.TextField(db_index=True, null=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
            ],
            options={
                "verbose_name": "Question",
                "verbose_name_plural": "Questions",
                "db_table": "questions",
                "ordering": ["sort_number"],
            },
        ),
        migrations.CreateModel(
            name="QuestionCategory",
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
                ("name", models.CharField(db_index=True, max_length=255, unique=True)),
                (
                    "name_uz",
                    models.CharField(
                        db_index=True, max_length=255, null=True, unique=True
                    ),
                ),
                (
                    "name_ru",
                    models.CharField(
                        db_index=True, max_length=255, null=True, unique=True
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        db_index=True, max_length=255, null=True, unique=True
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="question_categories/"
                    ),
                ),
                ("is_active", models.BooleanField(db_index=True, default=True)),
            ],
            options={
                "verbose_name": "Question Category",
                "verbose_name_plural": "Question Categories",
                "db_table": "question_categories",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Saved",
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
            ],
            options={
                "verbose_name": "Saved",
                "verbose_name_plural": "Saved",
                "db_table": "saved",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Test",
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
                ("title", models.CharField(db_index=True, max_length=255)),
                (
                    "title_uz",
                    models.CharField(db_index=True, max_length=255, null=True),
                ),
                (
                    "title_ru",
                    models.CharField(db_index=True, max_length=255, null=True),
                ),
                (
                    "title_en",
                    models.CharField(db_index=True, max_length=255, null=True),
                ),
                ("description", models.TextField(db_index=True)),
                ("description_uz", models.TextField(db_index=True, null=True)),
                ("description_ru", models.TextField(db_index=True, null=True)),
                ("description_en", models.TextField(db_index=True, null=True)),
                (
                    "banner",
                    models.ImageField(
                        blank=True, db_index=True, null=True, upload_to="test"
                    ),
                ),
                (
                    "question_count",
                    models.PositiveBigIntegerField(db_index=True, default=0),
                ),
                ("is_active", models.BooleanField(db_index=True, default=True)),
            ],
            options={
                "verbose_name": "Test",
                "verbose_name_plural": "Tests",
                "db_table": "test",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="TestQuestion",
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
                ("question", models.TextField(db_index=True, verbose_name="Question")),
                (
                    "question_uz",
                    models.TextField(db_index=True, null=True, verbose_name="Question"),
                ),
                (
                    "question_ru",
                    models.TextField(db_index=True, null=True, verbose_name="Question"),
                ),
                (
                    "question_en",
                    models.TextField(db_index=True, null=True, verbose_name="Question"),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        db_index=True, default=True, verbose_name="Is active"
                    ),
                ),
            ],
            options={
                "verbose_name": "Question",
                "verbose_name_plural": "Questions",
                "db_table": "question",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="Victim",
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
                ("message", models.TextField(db_index=True, verbose_name="message")),
                (
                    "answer",
                    models.TextField(
                        blank=True, db_index=True, null=True, verbose_name="answer"
                    ),
                ),
            ],
            options={
                "verbose_name": "victim",
                "verbose_name_plural": "victims",
                "db_table": "victims",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="VictimStatus",
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
                (
                    "name",
                    models.CharField(
                        db_index=True, max_length=255, verbose_name="name"
                    ),
                ),
                (
                    "name_uz",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "name_ru",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        db_index=True, max_length=255, null=True, verbose_name="name"
                    ),
                ),
                (
                    "is_pending",
                    models.BooleanField(
                        db_index=True, default=False, verbose_name="is pending"
                    ),
                ),
            ],
            options={
                "verbose_name": "victim status",
                "verbose_name_plural": "victim statuses",
                "db_table": "victim_statuses",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="VictimType",
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
                (
                    "name",
                    models.CharField(
                        db_index=True, max_length=255, unique=True, verbose_name="name"
                    ),
                ),
                (
                    "name_uz",
                    models.CharField(
                        db_index=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="name",
                    ),
                ),
                (
                    "name_ru",
                    models.CharField(
                        db_index=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="name",
                    ),
                ),
                (
                    "name_en",
                    models.CharField(
                        db_index=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="name",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        db_index=True, default=True, verbose_name="is active"
                    ),
                ),
            ],
            options={
                "verbose_name": "victim type",
                "verbose_name_plural": "victim types",
                "db_table": "victim_types",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Viewed",
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
            ],
            options={
                "verbose_name": "Viewed",
                "verbose_name_plural": "Viewed",
                "db_table": "viewed",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="CourseLesson",
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
                ("sort_number", models.PositiveIntegerField(db_index=True, default=0)),
                ("title", models.CharField(db_index=True, max_length=255)),
                (
                    "title_uz",
                    models.CharField(db_index=True, max_length=255, null=True),
                ),
                (
                    "title_ru",
                    models.CharField(db_index=True, max_length=255, null=True),
                ),
                (
                    "title_en",
                    models.CharField(db_index=True, max_length=255, null=True),
                ),
                ("description", models.TextField(db_index=True)),
                ("description_uz", models.TextField(db_index=True, null=True)),
                ("description_ru", models.TextField(db_index=True, null=True)),
                ("description_en", models.TextField(db_index=True, null=True)),
                ("text", models.TextField(blank=True, db_index=True, null=True)),
                ("text_uz", models.TextField(blank=True, db_index=True, null=True)),
                ("text_ru", models.TextField(blank=True, db_index=True, null=True)),
                ("text_en", models.TextField(blank=True, db_index=True, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, db_index=True, null=True, upload_to="lessons/"
                    ),
                ),
                ("likes_count", models.PositiveIntegerField(db_index=True, default=0)),
                (
                    "students_count",
                    models.PositiveIntegerField(db_index=True, default=0),
                ),
                ("audio_count", models.PositiveIntegerField(db_index=True, default=0)),
                ("video_count", models.PositiveIntegerField(db_index=True, default=0)),
                (
                    "document_count",
                    models.PositiveIntegerField(db_index=True, default=0),
                ),
                ("test_count", models.PositiveIntegerField(db_index=True, default=0)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="courses",
                        to="mobile.coursecategory",
                    ),
                ),
            ],
            options={
                "verbose_name": "Course Lesson",
                "verbose_name_plural": "Courses Lessons",
                "db_table": "courses_lessons",
                "ordering": ["sort_number"],
            },
        ),
        migrations.CreateModel(
            name="CourseLessonResource",
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
                ("title", models.CharField(db_index=True, max_length=255)),
                (
                    "title_uz",
                    models.CharField(db_index=True, max_length=255, null=True),
                ),
                (
                    "title_ru",
                    models.CharField(db_index=True, max_length=255, null=True),
                ),
                (
                    "title_en",
                    models.CharField(db_index=True, max_length=255, null=True),
                ),
                ("description", models.TextField(blank=True, db_index=True, null=True)),
                (
                    "description_uz",
                    models.TextField(blank=True, db_index=True, null=True),
                ),
                (
                    "description_ru",
                    models.TextField(blank=True, db_index=True, null=True),
                ),
                (
                    "description_en",
                    models.TextField(blank=True, db_index=True, null=True),
                ),
                (
                    "banner",
                    models.ImageField(
                        blank=True,
                        db_index=True,
                        null=True,
                        upload_to="lesson_resource/banner/",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, db_index=True, max_length=255, null=True
                    ),
                ),
                ("file", models.FileField(db_index=True, upload_to="lesson_resource/")),
                (
                    "size",
                    models.CharField(
                        blank=True, db_index=True, max_length=255, null=True
                    ),
                ),
                (
                    "type",
                    models.CharField(
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
                ("is_active", models.BooleanField(db_index=True, default=True)),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="resources",
                        to="mobile.courselesson",
                    ),
                ),
            ],
            options={
                "verbose_name": "Course Lesson Resource",
                "verbose_name_plural": "Course Lesson Resources",
                "db_table": "course_lesson_resources",
                "ordering": ["created_at"],
            },
        ),
    ]
