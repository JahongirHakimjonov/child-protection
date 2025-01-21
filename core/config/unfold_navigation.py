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
]

# TABS = [
#     {
#         "models": [
#             "auth.user",
#             "auth.group",
#         ],
#         "items": [
#             {
#                 "title": _("Foydalanuvchilar"),
#                 "link": reverse_lazy("admin:users_user_changelist"),
#             },
#             {
#                 "title": _("Guruhlar"),
#                 "link": reverse_lazy("admin:auth_group_changelist"),
#             },
#         ],
#     },
# ]
