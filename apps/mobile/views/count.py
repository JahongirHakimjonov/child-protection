from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.course import CourseLesson
from apps.mobile.models.news import News
from apps.mobile.models.victim import Victim
from apps.users.models.users import User


class CountApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user_count = User.objects.count()
        course_count = CourseLesson.objects.count()
        news_count = News.objects.count()
        victim_count = Victim.objects.count()

        return Response(
            {
                "user_count": user_count,
                "lesson_count": course_count,
                "news_count": news_count,
                "victim_count": victim_count,
            },
            status=status.HTTP_200_OK,
        )
