# Generated by Django 5.1.5 on 2025-02-04 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mobile", "0026_faq"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="answer_en",
            field=models.TextField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="answer",
            name="answer_ru",
            field=models.TextField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="answer",
            name="answer_uz",
            field=models.TextField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="coursecategory",
            name="description_en",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="coursecategory",
            name="description_ru",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="coursecategory",
            name="description_uz",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="coursecategory",
            name="sub_title_en",
            field=models.CharField(
                blank=True, db_index=True, max_length=255, null=True
            ),
        ),
        migrations.AddField(
            model_name="coursecategory",
            name="sub_title_ru",
            field=models.CharField(
                blank=True, db_index=True, max_length=255, null=True
            ),
        ),
        migrations.AddField(
            model_name="coursecategory",
            name="sub_title_uz",
            field=models.CharField(
                blank=True, db_index=True, max_length=255, null=True
            ),
        ),
        migrations.AddField(
            model_name="coursecategory",
            name="title_en",
            field=models.CharField(
                db_index=True, max_length=255, null=True, unique=True
            ),
        ),
        migrations.AddField(
            model_name="coursecategory",
            name="title_ru",
            field=models.CharField(
                db_index=True, max_length=255, null=True, unique=True
            ),
        ),
        migrations.AddField(
            model_name="coursecategory",
            name="title_uz",
            field=models.CharField(
                db_index=True, max_length=255, null=True, unique=True
            ),
        ),
        migrations.AddField(
            model_name="courselesson",
            name="description_en",
            field=models.TextField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="courselesson",
            name="description_ru",
            field=models.TextField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="courselesson",
            name="description_uz",
            field=models.TextField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="courselesson",
            name="text_en",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="courselesson",
            name="text_ru",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="courselesson",
            name="text_uz",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="courselesson",
            name="title_en",
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="courselesson",
            name="title_ru",
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="courselesson",
            name="title_uz",
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="courselessonresource",
            name="description_en",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="courselessonresource",
            name="description_ru",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="courselessonresource",
            name="description_uz",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="courselessonresource",
            name="title_en",
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="courselessonresource",
            name="title_ru",
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="courselessonresource",
            name="title_uz",
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="faq",
            name="answer_en",
            field=models.TextField(null=True, verbose_name="Answer"),
        ),
        migrations.AddField(
            model_name="faq",
            name="answer_ru",
            field=models.TextField(null=True, verbose_name="Answer"),
        ),
        migrations.AddField(
            model_name="faq",
            name="answer_uz",
            field=models.TextField(null=True, verbose_name="Answer"),
        ),
        migrations.AddField(
            model_name="faq",
            name="question_en",
            field=models.TextField(null=True, verbose_name="Question"),
        ),
        migrations.AddField(
            model_name="faq",
            name="question_ru",
            field=models.TextField(null=True, verbose_name="Question"),
        ),
        migrations.AddField(
            model_name="faq",
            name="question_uz",
            field=models.TextField(null=True, verbose_name="Question"),
        ),
        migrations.AddField(
            model_name="question",
            name="description_en",
            field=models.TextField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="question",
            name="description_ru",
            field=models.TextField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="question",
            name="description_uz",
            field=models.TextField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="question",
            name="title_en",
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="question",
            name="title_ru",
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="question",
            name="title_uz",
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="questioncategory",
            name="name_en",
            field=models.CharField(
                db_index=True, max_length=255, null=True, unique=True
            ),
        ),
        migrations.AddField(
            model_name="questioncategory",
            name="name_ru",
            field=models.CharField(
                db_index=True, max_length=255, null=True, unique=True
            ),
        ),
        migrations.AddField(
            model_name="questioncategory",
            name="name_uz",
            field=models.CharField(
                db_index=True, max_length=255, null=True, unique=True
            ),
        ),
        migrations.AddField(
            model_name="test",
            name="description_en",
            field=models.TextField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="test",
            name="description_ru",
            field=models.TextField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="test",
            name="description_uz",
            field=models.TextField(db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="test",
            name="title_en",
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="test",
            name="title_ru",
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="test",
            name="title_uz",
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="testquestion",
            name="question_en",
            field=models.TextField(db_index=True, null=True, verbose_name="Question"),
        ),
        migrations.AddField(
            model_name="testquestion",
            name="question_ru",
            field=models.TextField(db_index=True, null=True, verbose_name="Question"),
        ),
        migrations.AddField(
            model_name="testquestion",
            name="question_uz",
            field=models.TextField(db_index=True, null=True, verbose_name="Question"),
        ),
        migrations.AddField(
            model_name="victimtype",
            name="name_en",
            field=models.CharField(
                db_index=True,
                max_length=255,
                null=True,
                unique=True,
                verbose_name="name",
            ),
        ),
        migrations.AddField(
            model_name="victimtype",
            name="name_ru",
            field=models.CharField(
                db_index=True,
                max_length=255,
                null=True,
                unique=True,
                verbose_name="name",
            ),
        ),
        migrations.AddField(
            model_name="victimtype",
            name="name_uz",
            field=models.CharField(
                db_index=True,
                max_length=255,
                null=True,
                unique=True,
                verbose_name="name",
            ),
        ),
    ]
