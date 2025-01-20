from django.urls import path
from rest_framework_simplejwt.views import (
    TokenVerifyView,
)

from apps.users.views import (
    RegisterView,
    CheckPhoneView,
    MeView,
    UpdateAvatarView,
    UpdateUserView,
    ChangePasswordView,
    ConfirmView,
    SendPasswordResetView,
    ResetConfirmationCodeView,
    ResetSetPasswordView,
    DeleteAccountView,
    ResendView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    BlockSessionView,
    ListSessionView,
    SocialAuthView,
    LogoutView,
)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/check/phone/", CheckPhoneView.as_view(), name="check_phone"),
    path("auth/me/", MeView.as_view(), name="me"),
    path("auth/update/avatar/", UpdateAvatarView.as_view(), name="update_avatar"),
    path("auth/update/user/", UpdateUserView.as_view(), name="update"),
    path("auth/confirm/", ConfirmView.as_view(), name="confirm"),
    path("auth/resend/", ResendView.as_view(), name="resend"),
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/password/change/", ChangePasswordView.as_view(), name="change_password"),
    path("auth/user/delete/", DeleteAccountView.as_view(), name="delete-account"),
    path("auth/session/block/", BlockSessionView.as_view(), name="block_session"),
    path("auth/session/list/", ListSessionView.as_view(), name="list_session"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path(
        "auth/password/reset/", SendPasswordResetView.as_view(), name="reset-password"
    ),
    path(
        "auth/password/reset/confirm/",
        ResetConfirmationCodeView.as_view(),
        name="reset-confirmation-code",
    ),
    path(
        "auth/password/reset/set/", ResetSetPasswordView.as_view(), name="set-password"
    ),
    path(
        "auth/<str:provider_name>/callback/",
        SocialAuthView.as_view(),
        name="social_auth",
    ),
]
