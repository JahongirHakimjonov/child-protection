from django.urls import path

from apps.mobile.views.course import (
    CourseCategoryListAPIView,
    CourseListAPIView,
    CourseDetailAPIView,
    CourseLessonListAPIView,
    CourseLessonDetailAPIView,
    CourseLessonResourceListAPIView,
    CourseLessonResourceDetailAPIView,
)
from apps.mobile.views.question import (
    QuestionDetailAPIView,
    QuestionListAPIView,
    QuestionCategoryListAPIView,
)
from apps.mobile.views.saved import SavedApiView

urlpatterns = [
    path(
        "course/category/", CourseCategoryListAPIView.as_view(), name="course-category"
    ),
    path("course/lesson/", CourseLessonListAPIView.as_view(), name="course-lesson"),
    path(
        "course/lesson/<int:pk>",
        CourseLessonDetailAPIView.as_view(),
        name="course-lesson-detail",
    ),
    path(
        "course/resource/",
        CourseLessonResourceListAPIView.as_view(),
        name="course-resource",
    ),
    path(
        "course/resource/<int:pk>/",
        CourseLessonResourceDetailAPIView.as_view(),
        name="course-resource-detail",
    ),
    path("course/", CourseListAPIView.as_view(), name="course"),
    path("course/<int:pk>/", CourseDetailAPIView.as_view(), name="course-detail"),
    path("question/", QuestionListAPIView.as_view(), name="question"),
    path("question/<int:pk>/", QuestionDetailAPIView.as_view(), name="question-detail"),
    path(
        "question/category/",
        QuestionCategoryListAPIView.as_view(),
        name="question-category",
    ),
    path("saved/", SavedApiView.as_view(), name="saved"),
]
