from modeltranslation.translator import TranslationOptions, register

from apps.mobile.models.course import CourseCategory, CourseLesson, CourseLessonResource


@register(CourseCategory)
class CourseCategoryTranslationOptions(TranslationOptions):
    fields = ("title", "sub_title", "description")


@register(CourseLesson)
class CourseLessonTranslationOptions(TranslationOptions):
    fields = ("title", "description", "text")


@register(CourseLessonResource)
class CourseLessonResourceTranslationOptions(TranslationOptions):
    fields = ("title", "description")
