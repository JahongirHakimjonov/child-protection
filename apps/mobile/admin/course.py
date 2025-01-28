from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.admin import TabularInline
from unfold.widgets import UnfoldAdminColorInputWidget

from apps.mobile.models.course import (
    CourseCategory,
    CourseLesson,
    CourseLessonResource,
)


class ResourceInline(TabularInline):
    model = CourseLessonResource
    extra = 0
    tab = True
    fields = ["title", "file"]
    show_change_link = True


@admin.register(CourseCategory)
class CourseCategoryAdmin(ModelAdmin):
    list_display = ["id", "title", "image"]
    search_fields = ["name"]
    readonly_fields = ["created_at", "updated_at", "lesson_count"]

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields["first_color"].widget = UnfoldAdminColorInputWidget()
        form.base_fields["second_color"].widget = UnfoldAdminColorInputWidget()
        return form


@admin.register(CourseLesson)
class LessonAdmin(ModelAdmin):
    list_display = [
        "id",
        "category",
        "title",
        "is_active",
    ]
    search_fields = ["title"]
    readonly_fields = [
        "likes_count",
        "students_count",
        "audio_count",
        "video_count",
        "document_count",
        "test_count",
        "created_at",
        "updated_at",
    ]
    autocomplete_fields = ["category"]
    inlines = [ResourceInline]
    # formfield_overrides = {
    #     models.TextField: {
    #         "widget": WysiwygWidget,
    #     }
    # }
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "category",
                    "sort_number",
                    "title",
                    "description",
                    "text",
                    "image",
                    "is_active",
                ]
            },
        ),
        (
            "Counts",
            {
                "classes": ["tab"],
                "fields": [
                    "likes_count",
                    "students_count",
                    "audio_count",
                    "video_count",
                    "document_count",
                    "test_count",
                ],
            },
        ),
    ]


@admin.register(CourseLessonResource)
class LessonResourceAdmin(ModelAdmin):
    list_display = ["id", "lesson", "title"]
    search_fields = ["title"]
    readonly_fields = ["created_at", "updated_at", "size", "type", "name"]
    autocomplete_fields = ["lesson"]
