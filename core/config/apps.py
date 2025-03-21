THIRD_PARTY_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "modeltranslation",
    "corsheaders",
    "rosetta",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    # "silk",
]

DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

PROJECT_APPS = [
    "apps.shared.apps.SharedConfig",
    "apps.users.apps.UsersConfig",
    "apps.mobile.apps.MobileConfig",
    "apps.moderator.apps.ModeratorConfig",
    "apps.chat.apps.ChatConfig",
]
