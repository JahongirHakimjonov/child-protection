from django.urls import path

from apps.moderator.views.banner import ModeratorBannerView, ModeratorBannerDetailView

urlpatterns = [
    path("banner/", ModeratorBannerView.as_view(), name="moderator_banner"),
    path(
        "banner/<int:pk>/",
        ModeratorBannerDetailView.as_view(),
        name="moderator_banner_detail",
    ),
]
