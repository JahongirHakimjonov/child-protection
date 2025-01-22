from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline, TabularInline

from apps.mobile.models.course import (
    CourseCategory,
    Course,
    CourseLesson,
    CourseLessonResource,
)


class LessonInline(StackedInline):
    model = CourseLesson
    extra = 0
    tab = True
    fields = ["sort_number", "title", "description"]
    show_change_link = True


class ResourceInline(TabularInline):
    model = CourseLessonResource
    extra = 0
    tab = True
    fields = ["title", "file"]
    show_change_link = True


@admin.register(CourseCategory)
class CourseCategoryAdmin(ModelAdmin):
    list_display = ["id", "name", "image"]
    search_fields = ["name"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Course)
class CourseAdmin(ModelAdmin):
    list_display = [
        "id",
        "category",
        "title",
        "lesson_count",
        "students_count",
        "is_active",
        "is_paid",
    ]
    search_fields = ["title"]
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["category"]
    inlines = [LessonInline]


@admin.register(CourseLesson)
class CourseLessonAdmin(ModelAdmin):
    list_display = ["id", "course", "title"]
    search_fields = ["title"]
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["course"]
    inlines = [ResourceInline]


@admin.register(CourseLessonResource)
class CourseLessonResourceAdmin(ModelAdmin):
    list_display = ["id", "lesson", "title"]
    search_fields = ["title"]
    readonly_fields = ["created_at", "updated_at"]
    autocomplete_fields = ["lesson"]
