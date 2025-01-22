import mimetypes

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class CourseCategory(AbstractBaseModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    image = models.ImageField(upload_to="course_categories/", null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = _("Course Category")
        verbose_name_plural = _("Course Categories")
        ordering = ["name"]
        db_table = "course_categories"

    def __str__(self) -> str:
        return str(self.name)


class Course(AbstractBaseModel):
    category = models.ForeignKey(
        CourseCategory, on_delete=models.CASCADE, related_name="courses", db_index=True
    )
    sort_number = models.PositiveIntegerField(default=0, db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(db_index=True)
    image = models.ImageField(
        upload_to="courses/", null=True, blank=True, db_index=True
    )
    lesson_count = models.PositiveIntegerField(db_index=True, default=0)
    students_count = models.PositiveIntegerField(db_index=True, default=0)
    saved_count = models.PositiveIntegerField(default=0, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    is_paid = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ["sort_number"]
        db_table = "courses"

    def __str__(self) -> str:
        return str(self.title)


class CourseLesson(AbstractBaseModel):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", db_index=True
    )
    sort_number = models.PositiveIntegerField(default=0, db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = _("Course Lesson")
        verbose_name_plural = _("Course Lessons")
        ordering = ["sort_number"]
        db_table = "course_lessons"

    def __str__(self) -> str:
        return str(self.title)


class CourseLessonResource(AbstractBaseModel):
    lesson = models.ForeignKey(
        CourseLesson, on_delete=models.CASCADE, related_name="resources", db_index=True
    )
    title = models.CharField(max_length=255, db_index=True)
    name = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    file = models.FileField(upload_to="course_lessons/", db_index=True)
    size = models.PositiveIntegerField(default=0, db_index=True)
    type = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = _("Course Lesson Resource")
        verbose_name_plural = _("Course Lesson Resources")
        db_table = "course_lesson_resources"
        ordering = ["created_at"]

    def __str__(self) -> str:
        return str(self.title)

    def get_file_size(self):
        size = self.file.size
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024 * 1024:
            return f"{round(size / 1024, 2)} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{round(size / (1024 * 1024), 2)} MB"
        else:
            return f"{round(size / (1024 * 1024 * 1024), 2)} GB"

    get_file_size.short_description = _("File Size")

    def get_file_type(self):
        if "/" in self.type:
            return self.type.split("/")[1].upper()
        return self.type.upper()

    get_file_type.short_description = _("File Type")

    def get_file_name(self):
        return self.file.name.split("/")[-1]

    get_file_name.short_description = _("File Name")

    def save(self, *args, **kwargs):
        self.size = self.file.size
        self.type, _ = mimetypes.guess_type(self.file.name)
        self.name = self.file.name
        super().save(*args, **kwargs)
