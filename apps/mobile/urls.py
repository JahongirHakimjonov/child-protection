from django.urls import path

from apps.mobile.views.banner import BannerListAPIView
from apps.mobile.views.course import (
    CourseCategoryListAPIView,
    LessonListAPIView,
    LessonDetailAPIView,
    LessonResourceListAPIView,
    LessonResourceDetailAPIView,
    CourseCategoryDetailAPIView,
)
from apps.mobile.views.help import HelpView
from apps.mobile.views.question import (
    QuestionDetailAPIView,
    QuestionListAPIView,
    QuestionCategoryListAPIView,
)
from apps.mobile.views.saved import SavedApiView
from apps.mobile.views.test import QuestionList, TestResult

urlpatterns = [
    path(
        "course/category/", CourseCategoryListAPIView.as_view(), name="course-category"
    ),
    path(
        "course/category/<int:pk>/",
        CourseCategoryDetailAPIView.as_view(),
        name="course-category-detail",
    ),
    path("course/lesson/", LessonListAPIView.as_view(), name="course-lesson"),
    path(
        "course/lesson/<int:pk>/",
        LessonDetailAPIView.as_view(),
        name="course-lesson-detail",
    ),
    path(
        "course/resource/",
        LessonResourceListAPIView.as_view(),
        name="course-resource",
    ),
    path(
        "course/resource/<int:pk>/",
        LessonResourceDetailAPIView.as_view(),
        name="course-resource-detail",
    ),
    path("question/", QuestionListAPIView.as_view(), name="question"),
    path("question/<int:pk>/", QuestionDetailAPIView.as_view(), name="question-detail"),
    path(
        "question/category/",
        QuestionCategoryListAPIView.as_view(),
        name="question-category",
    ),
    path("saved/", SavedApiView.as_view(), name="saved"),
    path("test/<int:lesson_id>/", SavedApiView.as_view(), name="test"),
    path("question/<int:test_id>/", QuestionList.as_view(), name="question"),
    path("result/", TestResult.as_view(), name="result"),
    path("banner/", BannerListAPIView.as_view(), name="banner"),
    path("help/", HelpView.as_view(), name="help"),
]
