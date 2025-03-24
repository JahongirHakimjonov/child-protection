from django.urls import path

from apps.mobile.views.about import (
    AboutView,
    AboutDetailView,
    AboutProjectView,
    AboutProjectDetailView,
)
from apps.mobile.views.banner import BannerListAPIView
from apps.mobile.views.count import CountApiView
from apps.mobile.views.course import (
    CourseCategoryListAPIView,
    LessonListAPIView,
    LessonDetailAPIView,
    LessonResourceListAPIView,
    LessonResourceDetailAPIView,
    CourseCategoryDetailAPIView,
)
from apps.mobile.views.faq import FAQList
from apps.mobile.views.help import HelpView
from apps.mobile.views.news import NewsView, NewsDetailView
from apps.mobile.views.places import PlacesView
from apps.mobile.views.question import (
    QuestionDetailAPIView,
    QuestionListAPIView,
    QuestionCategoryListAPIView,
)
from apps.mobile.views.questionnaire import (
    QuestionnaireUserAnswerView,
    QuestionnaireDetailView,
    QuestionnaireCategoryView,
    QuestionnaireView,
    QuestionnaireUserAnswerDetailView,
)
from apps.mobile.views.saved import SavedApiView
from apps.mobile.views.test import TestResult, TestList, TestQuestionList
from apps.mobile.views.victim import VictimTypeList, VictimList
from apps.mobile.views.victim_stat import VictimStat

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
    path("test/<int:lesson_id>/", TestList.as_view(), name="test"),
    path("test/question/<int:test_id>/", TestQuestionList.as_view(), name="question"),
    path("result/", TestResult.as_view(), name="result"),
    path("banner/", BannerListAPIView.as_view(), name="banner"),
    path("help/", HelpView.as_view(), name="help"),
    path("faq/", FAQList.as_view(), name="faq"),
    path("victim/type/", VictimTypeList.as_view(), name="victim-type"),
    path("victim/", VictimList.as_view(), name="victim"),
    path("victim/statistics/", VictimStat.as_view(), name="victim"),
    path("news/", NewsView.as_view(), name="news"),
    path("news/<int:pk>/", NewsDetailView.as_view(), name="news_detail"),
    path("place/", PlacesView.as_view(), name="place"),
    path("count/", CountApiView.as_view(), name="count"),
    path("about/", AboutView.as_view(), name="about"),
    path("about/<int:pk>/", AboutDetailView.as_view(), name="about-detail"),
    path("about/project/", AboutProjectView.as_view(), name="about-project"),
    path(
        "about/project/<int:pk>/",
        AboutProjectDetailView.as_view(),
        name="about-project-detail",
    ),
    path(
        "questionnaire/category/",
        QuestionnaireCategoryView.as_view(),
        name="questionnaire-category",
    ),
    path("questionnaire/", QuestionnaireView.as_view(), name="questionnaire"),
    path(
        "questionnaire/<int:pk>/",
        QuestionnaireDetailView.as_view(),
        name="questionnaire-detail",
    ),
    path(
        "questionnaire/answer/",
        QuestionnaireUserAnswerView.as_view(),
        name="questionnaire-answer",
    ),
    path(
        "questionare/answer/user/",
        QuestionnaireUserAnswerDetailView.as_view(),
        name="questionare-user-answer",
    ),
]
