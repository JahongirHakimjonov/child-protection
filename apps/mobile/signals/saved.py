from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.mobile.models.saved import Saved


@receiver(post_save, sender=Saved)
def update_course_saved_count(sender, instance, created, **kwargs):
    if created:
        instance.course.saved_count += 1
        instance.course.save()


@receiver(post_delete, sender=Saved)
def update_course_saved_count(sender, instance, **kwargs):
    instance.course.saved_count -= 1
    instance.course.save()
