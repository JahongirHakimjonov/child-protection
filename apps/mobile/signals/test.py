from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.mobile.models.test import Test


@receiver(post_save, sender=Test)
def update_course_saved_count(sender, instance, created, **kwargs):
    if created:
        instance.lesson.test_count = Test.objects.filter(lesson=instance.lesson).count()
        instance.lesson.save()


@receiver(post_delete, sender=Test)
def update_course_saved_count(sender, instance, **kwargs):
    instance.lesson.test_count = Test.objects.filter(lesson=instance.lesson).count()
    instance.lesson.save()
