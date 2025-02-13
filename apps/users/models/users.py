from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from apps.shared.encoders import PrettyJSONEncoder
from apps.shared.models import AbstractBaseModel
from apps.users.managers import UserManager


class RoleChoices(models.TextChoices):
    ADMIN = "ADMIN", _("Admin")
    USER = "USER", _("Foydalanuvchi")
    SUPER_ADMIN = "SUPER_ADMIN", _("Super admin")


class RegisterTypeChoices(models.TextChoices):
    PHONE = "PHONE", _("Telefon")
    GOOGLE = "GOOGLE", _("Google")
    APPLE = "APPLE", _("Apple")


class User(AbstractUser, AbstractBaseModel):
    phone = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Telefon raqami"),
        db_index=True,
        null=True,
        blank=True,
    )
    username = models.CharField(
        max_length=100,
        verbose_name=_("Foydalanuvchi nomi"),
        db_index=True,
    )
    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True, verbose_name=_("Avatar")
    )
    role = models.CharField(
        choices=RoleChoices,
        max_length=20,
        default=RoleChoices.USER,
        verbose_name=_("Role"),
    )
    register_type = models.CharField(
        choices=RegisterTypeChoices,
        max_length=20,
        verbose_name=_("Ro'yxatdan o'tish turi"),
        db_index=True,
        default=RegisterTypeChoices.PHONE,
    )
    sos_count = models.PositiveBigIntegerField(
        default=0, verbose_name=_("SOS count"), db_index=True, null=True, blank=True
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username"]
    objects = UserManager()

    def __str__(self):
        user_data = self.phone if self.phone else self.email
        return (
            f"{self.first_name} {self.last_name} - {user_data}"
            if self.phone
            else str(_("Foydalanuvchi"))
        )

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.phone
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Foydalanuvchi")
        verbose_name_plural = _("Foydalanuvchilar")
        ordering = ["-created_at"]
        db_table = "users"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": self.id,
        }


class ActiveSessions(AbstractBaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sessions", verbose_name=_("User")
    )
    ip = models.GenericIPAddressField(db_index=True, verbose_name=_("IP address"))
    user_agent = models.TextField(verbose_name=_("User agent"), db_index=True)
    location = models.JSONField(
        verbose_name=_("Location"), null=True, blank=True, encoder=PrettyJSONEncoder
    )
    last_activity = models.DateTimeField(
        auto_now=True, verbose_name=_("Last activity"), db_index=True
    )
    fcm_token = models.CharField(
        max_length=255,
        verbose_name=_("FCM token"),
        null=True,
        blank=True,
        db_index=True,
    )
    refresh_token = models.TextField(verbose_name=_("Refresh token"), db_index=True)
    access_token = models.TextField(verbose_name=_("Access token"), db_index=True)
    expired_at = models.DateTimeField(
        verbose_name=_("Expired at"), db_index=True, null=True, blank=True
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))
    data = models.JSONField(
        verbose_name=_("Data"), null=True, blank=True, encoder=PrettyJSONEncoder
    )

    class Meta:
        verbose_name = _("Active session")
        verbose_name_plural = _("Active sessions")
        db_table = "active_sessions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} {self.ip}" if self.user else str(_("Session"))


class UserData(AbstractBaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="data",
        verbose_name=_("User"),
        db_index=True,
    )
    provider = models.CharField(
        choices=RegisterTypeChoices,
        max_length=20,
        verbose_name=_("Provider"),
        db_index=True,
    )
    uid = models.CharField(max_length=100, verbose_name=_("Provider ID"), db_index=True)
    extra_data = models.JSONField(
        verbose_name=_("Extra data"), null=True, blank=True, db_index=True, encoder=PrettyJSONEncoder
    )

    class Meta:
        verbose_name = _("User data")
        verbose_name_plural = _("User data")
        db_table = "user_data"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.user.username} {self.user.email}"
            if self.user.email
            else str(_("User"))
        )
