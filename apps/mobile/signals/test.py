from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.mobile.models.test import Test, TestQuestion


@receiver(post_save, sender=Test)
def update_course_saved_count(sender, instance, created, **kwargs):
    if created:
        instance.lesson.test_count = (
            Test.objects.filter(lesson=instance.lesson).count() or 0
        )
        instance.lesson.save()


@receiver(post_delete, sender=Test)
def update_course_saved_count(sender, instance, **kwargs):
    instance.lesson.test_count = (
        Test.objects.filter(lesson=instance.lesson).count() or 0
    )
    instance.lesson.save()


@receiver(post_save, sender=TestQuestion)
def update_question_count(sender, instance, created, **kwargs):
    if created:
        instance.test.question_count = (
            TestQuestion.objects.filter(test=instance.test).count() or 0
        )
        instance.test.save()


@receiver(post_delete, sender=TestQuestion)
def update_question_count(sender, instance, **kwargs):
    instance.test.question_count = (
        TestQuestion.objects.filter(test=instance.test).count() or 0
    )
    instance.test.save()
