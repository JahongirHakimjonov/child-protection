from django.conf import settings
from django.conf.urls.i18n import i18n_patterns  # noqa: F401
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from core.config.swagger import urlpatterns as swagger_patterns

urlpatterns = (
    [
        path("i18n/", include("django.conf.urls.i18n")),
    ]
    + i18n_patterns(
        path("admin/", admin.site.urls),
    )
    + [
        path("", include("apps.shared.urls")),
        path("api/v1/", include("apps.users.urls")),
        path("api/v1/", include("apps.mobile.urls")),
        path("api/v1/moderator/", include("apps.moderator.urls")),
        path("api/v1/", include("apps.chat.urls")),
        path("rosetta/", include("rosetta.urls")),
        # path("silk/", include("silk.urls", namespace="silk")),
        # Media and static files
        re_path(r"static/(?P<path>.*)", serve, {"document_root": settings.STATIC_ROOT}),
        re_path(r"media/(?P<path>.*)", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
)

urlpatterns += swagger_patterns
