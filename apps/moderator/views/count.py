from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.course import CourseLesson
from apps.mobile.models.course import CourseLessonResource
from apps.mobile.models.help import Help, HelpStatus
from apps.mobile.models.news import News
from apps.mobile.models.question import Question
from apps.mobile.models.saved import Saved
from apps.mobile.models.test import TestQuestion
from apps.mobile.models.victim import Victim
from apps.users.models.users import User


class ModeratorCount(APIView):
    def get(self, request):
        user_count = User.objects.count()
        course_count = CourseLesson.objects.count()
        question_count = Question.objects.count()
        news_count = News.objects.count()
        help_count = (
            Help.objects.filter(status=HelpStatus.DANGER).distinct("user").count()
        )
        victim_count = Victim.objects.count()
        test_count = TestQuestion.objects.count()
        resource_count = CourseLessonResource.objects.count()
        saved_count = Saved.objects.count()

        return Response(
            {
                "user_count": user_count,
                "lesson_count": course_count,
                "question_count": question_count,
                "news_count": news_count,
                "help_count": help_count,
                "victim_count": victim_count,
                "test_count": test_count,
                "resource_count": resource_count,
                "student_count": saved_count,
            },
            status=status.HTTP_200_OK,
        )
