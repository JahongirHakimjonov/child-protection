# Generated by Django 5.1.5 on 2025-01-22 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mobile", "0002_remove_course_price_course_saved_count_saved"),
    ]

    operations = [
        migrations.AddField(
            model_name="coursecategory",
            name="is_active",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AddField(
            model_name="courselesson",
            name="is_active",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AddField(
            model_name="courselessonresource",
            name="is_active",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AddField(
            model_name="question",
            name="is_active",
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AddField(
            model_name="questioncategory",
            name="is_active",
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
