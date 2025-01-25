from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.mobile.models.saved import Saved, Viewed


@receiver(post_save, sender=Saved)
def update_course_saved_count(sender, instance, created, **kwargs):
    if created:
        instance.lesson.likes_count += 1
        instance.lesson.save()


@receiver(post_delete, sender=Saved)
def update_course_saved_count(sender, instance, **kwargs):
    instance.lesson.likes_count -= 1
    instance.lesson.save()


@receiver(post_save, sender=Viewed)
def update_course_viewed_count(sender, instance, created, **kwargs):
    if created:
        instance.lesson.students_count += 1
        instance.lesson.save()


@receiver(post_delete, sender=Viewed)
def update_course_viewed_count(sender, instance, **kwargs):
    instance.lesson.students_count -= 1
    instance.lesson.save()
