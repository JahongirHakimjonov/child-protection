# Generated by Django 5.1.5 on 2025-01-22 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mobile", "0005_alter_question_sort_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="lesson_count",
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name="course",
            name="students_count",
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]