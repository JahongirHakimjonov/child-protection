from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def user_has_group_or_permission(user, permission):
    if user.is_superuser:
        return True

    group_names = user.groups.values_list("name", flat=True)
    if not group_names:
        return True

    return user.groups.filter(permissions__codename=permission).exists()


PAGES = [
    {
        "seperator": True,
        "items": [
            {
                "title": _("Bosh sahifa"),
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Foydalanuvchilar"),
        "items": [
            {
                "title": _("Guruhlar"),
                "icon": "person_add",
                "link": reverse_lazy("admin:auth_group_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_group"
                ),
            },
            {
                "title": _("Foydalanuvchilar"),
                "icon": "person_add",
                "link": reverse_lazy("admin:users_user_changelist"),
                "permission": lambda request: user_has_group_or_permission(
                    request.user, "view_user"
                ),
            },
            {
                "title": _("SMS Kodlar"),
                "icon": "sms",
                "link": reverse_lazy("admin:users_smsconfirm_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_smsconfirm"
                ),
            },
            {
                "title": _("Site"),
                "icon": "captive_portal",
                "link": reverse_lazy("admin:sites_site_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_smsconfirm"
                ),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Foydalanuvchi ma'lumotlari"),
        "items": [
            {
                "title": _("Aktiv sessiyalar"),
                "icon": "mobile_friendly",
                "link": reverse_lazy("admin:users_activesessions_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_activesessions"
                ),
            },
            {
                "title": _("User Social data"),
                "icon": "database",
                "link": reverse_lazy("admin:users_userdata_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_userdata"
                ),
            },
            {
                "title": _("Bildirishnomalar"),
                "icon": "mark_email_unread",
                "link": reverse_lazy("admin:users_notification_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_notification"
                ),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Kurslar"),
        "items": [
            {
                "title": _("Darslar"),
                "icon": "play_lesson",
                "link": reverse_lazy("admin:mobile_courselesson_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_courselesson"
                ),
            },
            {
                "title": _("Resurslar"),
                "icon": "cloud_upload",
                "link": reverse_lazy("admin:mobile_courselessonresource_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_courselessonresource"
                ),
            },
            {
                "title": _("Ketegoriyalar"),
                "icon": "list",
                "link": reverse_lazy("admin:mobile_coursecategory_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_coursecategory"
                ),
            },
            {
                "title": _("Saqlanganlar"),
                "icon": "bookmark",
                "link": reverse_lazy("admin:mobile_saved_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_saved"
                ),
            },
            {
                "title": _("Ko'rganlar"),
                "icon": "visibility",
                "link": reverse_lazy("admin:mobile_viewed_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_viewed"
                ),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Testlar"),
        "items": [
            {
                "title": _("Testlar"),
                "icon": "quiz",
                "link": reverse_lazy("admin:mobile_test_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_test"
                ),
            },
            {
                "title": _("Savollar"),
                "icon": "unknown_document",
                "link": reverse_lazy("admin:mobile_testquestion_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_testquestion"
                ),
            },
            {
                "title": _("Javoblar"),
                "icon": "person_raised_hand",
                "link": reverse_lazy("admin:mobile_answer_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_answer"
                ),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Savollar"),
        "items": [
            {
                "title": _("Savollar"),
                "icon": "question_mark",
                "link": reverse_lazy("admin:mobile_question_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_question"
                ),
            },
            {
                "title": _("Kategoriyalar"),
                "icon": "checklist_rtl",
                "link": reverse_lazy("admin:mobile_questioncategory_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_questioncategory"
                ),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Chat"),
        "items": [
            {
                "title": _("Chat"),
                "icon": "forum",
                "link": reverse_lazy("admin:chat_chatroom_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_chatroom"
                ),
            },
            {
                "title": _("Xabarlar"),
                "icon": "mark_chat_read",
                "link": reverse_lazy("admin:chat_message_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_message"
                ),
            },
            {
                "title": _("Chat resurslar"),
                "icon": "cloud_download",
                "link": reverse_lazy("admin:chat_chatresource_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_chatresource"
                ),
            },
        ],
    },
    {
        "seperator": True,
        "title": _("Qo'shimcha"),
        "items": [
            {
                "title": _("FAQ"),
                "icon": "quiz",
                "link": reverse_lazy("admin:mobile_faq_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_faq"
                ),
            },
            {
                "title": _("Banner"),
                "icon": "perm_media",
                "link": reverse_lazy("admin:mobile_banner_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_banner"
                ),
            },
            {
                "title": _("Yordam xizmati"),
                "icon": "privacy_tip",
                "link": reverse_lazy("admin:mobile_help_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_help"
                ),
            },
            {
                "title": _("Victimlik"),
                "icon": "warning",
                "link": reverse_lazy("admin:mobile_victim_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_victim"
                ),
            },
            {
                "title": _("Yangiliklar"),
                "icon": "news",
                "link": reverse_lazy("admin:mobile_news_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_news"
                ),
            },
            {
                "title": _("Joylashuvlar"),
                "icon": "where_to_vote",
                "link": reverse_lazy("admin:mobile_place_changelist"),
                "permissions": lambda request: user_has_group_or_permission(
                    request.user, "view_place"
                ),
            },
        ],
    },
]

TABS = [
    {
        "models": [
            "mobile.victim",
            "mobile.victimtype",
            "mobile.victimstatus",
        ],
        "items": [
            {
                "title": _("Victimlar"),
                "link": reverse_lazy("admin:mobile_victim_changelist"),
            },
            {
                "title": _("Victim turlari"),
                "link": reverse_lazy("admin:mobile_victimtype_changelist"),
            },
            {
                "title": _("Victim statuslari"),
                "link": reverse_lazy("admin:mobile_victimstatus_changelist"),
            },
        ],
    },
]
