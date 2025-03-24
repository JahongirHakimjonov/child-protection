from django.urls import path

from apps.mobile.views.questionnaire import QuestionnaireUserAnswerDetailView
from apps.moderator.views.about import (
    ModeratorAboutProjectDetailView,
    ModeratorAboutProjectView,
    ModeratorAboutDetailView,
    ModeratorAboutView,
)
from apps.moderator.views.banner import ModeratorBannerView, ModeratorBannerDetailView
from apps.moderator.views.chat import (
    ModeratorChatRoomList,
    ModeratorMessageList,
    ModeratorChatResourceView,
    ModeratorMessageUpdate,
)
from apps.moderator.views.count import ModeratorCount
from apps.moderator.views.course import (
    ModeratorCourseCategoryView,
    ModeratorCourseCategoryDetailView,
    ModeratorCourseLessonResourceView,
    ModeratorCourseLessonResourceDetailView,
    ModeratorCourseLessonView,
    ModeratorCourseLessonDetailView,
)
from apps.moderator.views.faq import ModeratorFAQView, ModeratorFAQDetailView
from apps.moderator.views.help import ModeratorHelpView, ModeratorHelpDetailView
from apps.moderator.views.news import ModeratorNewsList, ModeratorNewsDetail
from apps.moderator.views.notification import (
    ModeratorNotificationView,
    ModeratorNotificationDetailView,
)
from apps.moderator.views.places import ModeratorPlaceList, ModeratorPlaceDetail
from apps.moderator.views.question import (
    ModeratorQuestionCategoryView,
    ModeratorQuestionCategoryDetailView,
    ModeratorQuestionView,
    ModeratorQuestionDetailView,
)
from apps.moderator.views.questionnaire import (
    ModeratorQuestionareCategoryView,
    ModeratorQuestionareCategoryDetailView,
    ModeratorQuestionareView,
    ModeratorQuestionareDetailView,
    ModeratorQuestionareUserAnswerView,
    ModeratorQuestionareUserDetailAnswerView,
)
from apps.moderator.views.test import (
    ModeratorTestView,
    ModeratorTestDetailView,
    ModeratorTestQuestionView,
    ModeratorTestQuestionDetailView,
    ModeratorAnswerView,
    ModeratorAnswerDetailView,
)
from apps.moderator.views.user import ModeratorUserView, ModeratorUserDetailView
from apps.moderator.views.victim import (
    VictimList,
    VictimDetail,
    VictimTypeList,
    VictimTypeDetail,
    VictimStatusList,
    VictimStatusDetail,
)
from apps.moderator.views.victim_count import VictimCount

urlpatterns = [
    path("banner/", ModeratorBannerView.as_view(), name="moderator_banner"),
    path(
        "banner/<int:pk>/",
        ModeratorBannerDetailView.as_view(),
        name="moderator_banner_detail",
    ),
    path(
        "course/category/",
        ModeratorCourseCategoryView.as_view(),
        name="moderator_course_category",
    ),
    path(
        "course/category/<int:pk>/",
        ModeratorCourseCategoryDetailView.as_view(),
        name="moderator_course_detail",
    ),
    path(
        "course/lesson/resource/",
        ModeratorCourseLessonResourceView.as_view(),
        name="moderator_category_lesson_resource",
    ),
    path(
        "course/lesson/resource/<int:pk>/",
        ModeratorCourseLessonResourceDetailView.as_view(),
        name="moderator_category_lesson_resource_detail",
    ),
    path(
        "course/lesson/",
        ModeratorCourseLessonView.as_view(),
        name="moderator_category_lesson",
    ),
    path(
        "course/lesson/<int:pk>/",
        ModeratorCourseLessonDetailView.as_view(),
        name="moderator_category_lesson_detail",
    ),
    path(
        "question/category/",
        ModeratorQuestionCategoryView.as_view(),
        name="moderator_question_category",
    ),
    path(
        "question/category/<int:pk>/",
        ModeratorQuestionCategoryDetailView.as_view(),
        name="moderator_question_category_detail",
    ),
    path(
        "question/",
        ModeratorQuestionView.as_view(),
        name="moderator_question",
    ),
    path(
        "question/<int:pk>/",
        ModeratorQuestionDetailView.as_view(),
        name="moderator_question_detail",
    ),
    path(
        "test/",
        ModeratorTestView.as_view(),
        name="moderator_test",
    ),
    path(
        "test/<int:pk>/",
        ModeratorTestDetailView.as_view(),
        name="moderator_test_detail",
    ),
    path(
        "test/question/",
        ModeratorTestQuestionView.as_view(),
        name="moderator_test_question",
    ),
    path(
        "test/question/<int:pk>/",
        ModeratorTestQuestionDetailView.as_view(),
        name="moderator_test_question_detail",
    ),
    path(
        "test/answer/",
        ModeratorAnswerView.as_view(),
        name="moderator_answer",
    ),
    path(
        "test/answer/<int:pk>/",
        ModeratorAnswerDetailView.as_view(),
        name="moderator_answer_detail",
    ),
    path(
        "help/",
        ModeratorHelpView.as_view(),
        name="moderator_help",
    ),
    path(
        "help/<int:pk>/",
        ModeratorHelpDetailView.as_view(),
        name="moderator_help_detail",
    ),
    path(
        "notification/",
        ModeratorNotificationView.as_view(),
        name="moderator_notification",
    ),
    path(
        "notification/<int:pk>/",
        ModeratorNotificationDetailView.as_view(),
        name="moderator_notification_detail",
    ),
    path(
        "user/",
        ModeratorUserView.as_view(),
        name="moderator_user",
    ),
    path(
        "user/<int:pk>/",
        ModeratorUserDetailView.as_view(),
        name="moderator_user_detail",
    ),
    path("chat/", ModeratorChatRoomList.as_view(), name="chat"),
    path("chat/resource/", ModeratorChatResourceView.as_view(), name="chat-resource"),
    path("message/", ModeratorMessageList.as_view(), name="message"),
    path("message/<int:pk>/", ModeratorMessageUpdate.as_view(), name="message"),
    path(
        "faq/",
        ModeratorFAQView.as_view(),
        name="moderator_faq",
    ),
    path(
        "faq/<int:pk>/",
        ModeratorFAQDetailView.as_view(),
        name="moderator_faq",
    ),
    path(
        "place/",
        ModeratorPlaceList.as_view(),
        name="moderator_place",
    ),
    path(
        "place/<int:pk>/",
        ModeratorPlaceDetail.as_view(),
        name="moderator_place_detail",
    ),
    path(
        "victim/",
        VictimList.as_view(),
        name="moderator_victim",
    ),
    path(
        "victim/<int:pk>/",
        VictimDetail.as_view(),
        name="moderator_victim_detail",
    ),
    path(
        "victim/type/",
        VictimTypeList.as_view(),
        name="moderator_victim_type",
    ),
    path(
        "victim/type/<int:pk>/",
        VictimTypeDetail.as_view(),
        name="moderator_victim_type_detail",
    ),
    path(
        "victim/status/",
        VictimStatusList.as_view(),
        name="moderator_victim_status",
    ),
    path(
        "victim/status/<int:pk>/",
        VictimStatusDetail.as_view(),
        name="moderator_victim_status_detail",
    ),
    path(
        "victim/count/",
        VictimCount.as_view(),
        name="moderator_victim_count",
    ),
    path(
        "news/",
        ModeratorNewsList.as_view(),
        name="moderator_news",
    ),
    path(
        "news/<int:pk>/",
        ModeratorNewsDetail.as_view(),
        name="moderator_news_detail",
    ),
    path(
        "count/",
        ModeratorCount.as_view(),
        name="moderator_count",
    ),
    path("about/", ModeratorAboutView.as_view(), name="about"),
    path("about/<int:pk>/", ModeratorAboutDetailView.as_view(), name="about-detail"),
    path("about/project/", ModeratorAboutProjectView.as_view(), name="about-project"),
    path(
        "about/project/<int:pk>/",
        ModeratorAboutProjectDetailView.as_view(),
        name="about-project-detail",
    ),
    path("questionare/", ModeratorQuestionareView.as_view(), name="questionare-list"),
    path(
        "questionare/<int:pk>/",
        ModeratorQuestionareDetailView.as_view(),
        name="questionare-detail",
    ),
    path(
        "questionare/category/",
        ModeratorQuestionareCategoryView.as_view(),
        name="questionare-category",
    ),
    path(
        "questionare/category/<int:pk>/",
        ModeratorQuestionareCategoryDetailView.as_view(),
        name="questionare-category-detail",
    ),
    path(
        "questionare/answer/",
        ModeratorQuestionareUserAnswerView.as_view(),
        name="questionare-answer",
    ),
    path(
        "questionare/answer/<int:pk>/",
        ModeratorQuestionareUserDetailAnswerView.as_view(),
        name="questionare-answer-detail",
    ),
]
