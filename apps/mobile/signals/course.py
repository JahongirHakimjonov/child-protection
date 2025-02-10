from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.mobile.models.course import CourseLessonResource, ResourceTypes, CourseLesson


@receiver(post_save, sender=CourseLessonResource)
def update_course_resource_count(sender, instance, created, **kwargs):
    if created:
        if instance.type == ResourceTypes.VIDEO:
            instance.lesson.video_count = CourseLessonResource.objects.filter(
                lesson=instance.lesson, type=ResourceTypes.VIDEO
            ).count()
        elif instance.type == ResourceTypes.AUDIO:
            instance.lesson.audio_count = CourseLessonResource.objects.filter(
                lesson=instance.lesson, type=ResourceTypes.AUDIO
            ).count()
        else:
            instance.lesson.document_count = CourseLessonResource.objects.filter(
                lesson=instance.lesson, type=ResourceTypes.DOCUMENT
            ).count()
        instance.lesson.save()


@receiver(post_delete, sender=CourseLessonResource)
def update_course_resource_count_on_delete(sender, instance, **kwargs):
    if instance.type == ResourceTypes.VIDEO:
        instance.lesson.video_count = (
            CourseLessonResource.objects.filter(
                lesson=instance.lesson, type=ResourceTypes.VIDEO
            ).count()
            or 0
        )
    elif instance.type == ResourceTypes.AUDIO:
        instance.lesson.audio_count = (
            CourseLessonResource.objects.filter(
                lesson=instance.lesson, type=ResourceTypes.AUDIO
            ).count()
            or 0
        )
    else:
        instance.lesson.document_count = (
            CourseLessonResource.objects.filter(
                lesson=instance.lesson, type=ResourceTypes.DOCUMENT
            ).count()
            or 0
        )
    instance.lesson.save()


@receiver(post_save, sender=CourseLesson)
def update_course_lesson_count(sender, instance, created, **kwargs):
    if created:
        instance.category.lesson_count = CourseLesson.objects.filter(
            category=instance.category
        ).count()
        instance.category.save()


@receiver(post_delete, sender=CourseLesson)
def update_course_lesson_count_on_delete(sender, instance, **kwargs):
    instance.category.lesson_count = (
        CourseLesson.objects.filter(category=instance.category).count() or 0
    )
    instance.category.save()
