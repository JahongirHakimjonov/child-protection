import mimetypes

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class ResourceTypes(models.TextChoices):
    VIDEO = "VIDEO", _("Video")
    AUDIO = "AUDIO", _("Audio")
    DOCUMENT = "DOCUMENT", _("Document")


class CourseCategory(AbstractBaseModel):
    title = models.CharField(max_length=255, unique=True, db_index=True)
    sub_title = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    description = models.TextField(db_index=True, null=True, blank=True)
    image = models.ImageField(upload_to="course_categories/", null=True, blank=True)
    lesson_count = models.PositiveIntegerField(db_index=True, default=0)
    first_color = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    second_color = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = _("Course Category")
        verbose_name_plural = _("Course Categories")
        ordering = ["-created_at"]
        db_table = "course_categories"

    def __str__(self) -> str:
        return str(self.title)


class CourseLesson(AbstractBaseModel):
    category = models.ForeignKey(
        CourseCategory, on_delete=models.CASCADE, related_name="courses", db_index=True
    )
    sort_number = models.PositiveIntegerField(default=0, db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(db_index=True)
    text = models.TextField(db_index=True, null=True, blank=True)
    image = models.ImageField(
        upload_to="lessons/", null=True, blank=True, db_index=True
    )
    likes_count = models.PositiveIntegerField(db_index=True, default=0)
    students_count = models.PositiveIntegerField(db_index=True, default=0)
    audio_count = models.PositiveIntegerField(db_index=True, default=0)
    video_count = models.PositiveIntegerField(db_index=True, default=0)
    document_count = models.PositiveIntegerField(db_index=True, default=0)
    test_count = models.PositiveIntegerField(db_index=True, default=0)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = _("Course Lesson")
        verbose_name_plural = _("Courses Lessons")
        ordering = ["sort_number"]
        db_table = "courses_lessons"

    def __str__(self) -> str:
        return str(self.title)


class CourseLessonResource(AbstractBaseModel):
    lesson = models.ForeignKey(
        CourseLesson, on_delete=models.CASCADE, related_name="resources", db_index=True
    )
    title = models.CharField(max_length=255, db_index=True)
    name = models.CharField(max_length=255, db_index=True, null=True, blank=True)
    file = models.FileField(upload_to="lesson_resource/", db_index=True)
    size = models.CharField(db_index=True, max_length=255, null=True, blank=True)
    type = models.CharField(
        max_length=255, db_index=True, null=True, blank=True, choices=ResourceTypes
    )
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = _("Course Lesson Resource")
        verbose_name_plural = _("Course Lesson Resources")
        db_table = "course_lesson_resources"
        ordering = ["created_at"]

    def __str__(self) -> str:
        return str(self.title)

    def get_file_size(self, size=None):
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024 * 1024:
            return f"{round(size / 1024, 2)} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{round(size / (1024 * 1024), 2)} MB"
        else:
            return f"{round(size / (1024 * 1024 * 1024), 2)} GB"

    get_file_size.short_description = _("File Size")

    def get_file_type(self, file=None):
        if file:
            mime_type = mimetypes.guess_type(file)[0]
            if mime_type:
                if mime_type.startswith("video"):
                    return ResourceTypes.VIDEO
                elif mime_type.startswith("audio"):
                    return ResourceTypes.AUDIO
                elif mime_type.startswith("application") or mime_type.startswith(
                    "text"
                ):
                    return ResourceTypes.DOCUMENT
        return ResourceTypes.DOCUMENT

    get_file_type.short_description = _("File Type")

    def get_file_name(self, file=None):
        if file:
            return file.split("/")[-1]

    get_file_name.short_description = _("File Name")

    def save(self, *args, **kwargs):
        self.size = self.get_file_size(self.file.size)
        self.type = self.get_file_type(self.file.name)
        self.name = self.get_file_name(self.file.name)
        super().save(*args, **kwargs)
