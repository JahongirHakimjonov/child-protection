from django.urls import path

from apps.shared.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
