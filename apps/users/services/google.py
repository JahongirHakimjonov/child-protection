import os
import urllib.parse

import requests
from django.core.files.base import ContentFile
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from apps.users.models.users import RegisterTypeChoices, UserData, User
from apps.users.services.register import RegisterService


class Google:
    @staticmethod
    def authenticate(id_token):
        try:
            # token_data = Google._fetch_token(code)
            idinfo = Google._verify_token(id_token)
            user = Google._get_or_create_user(idinfo)
            if idinfo.get("picture"):
                Google._save_user_avatar(user, idinfo["picture"])
            Google._update_user_data(user, idinfo)
            return user.tokens()
        except (ValueError, requests.RequestException) as e:
            raise ValueError(f"Authentication failed: {str(e)}")

    # @staticmethod
    # def _fetch_token(code):
    #     response = requests.post(
    #         "https://oauth2.googleapis.com/token",
    #         data={
    #             "code": code,
    #             "client_id": os.getenv("GOOGLE_CLIENT_ID"),
    #             "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
    #             "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
    #             "grant_type": "authorization_code",
    #         },
    #     )
    #     response.raise_for_status()
    #     return response.json()

    @staticmethod
    def _verify_token(token):
        return id_token.verify_oauth2_token(
            token, google_requests.Request(), os.getenv("GOOGLE_CLIENT_ID")
        )

    @staticmethod
    def _get_or_create_user(idinfo):
        user, created = User.objects.get_or_create(
            email=idinfo["email"],
            defaults={
                "username": RegisterService.check_unique_username(
                    idinfo["email"].split("@")[0]
                ),
                "first_name": idinfo.get("given_name", ""),
                "last_name": idinfo.get("family_name", ""),
                "is_active": True,
                "register_type": RegisterTypeChoices.GOOGLE,
            },
        )
        return user

    @staticmethod
    def _save_user_avatar(user, picture_url):
        try:
            response = requests.get(picture_url)
            response.raise_for_status()

            parsed_url = urllib.parse.urlparse(picture_url)
            filename = os.path.basename(parsed_url.path)
            sanitized_filename = f"{user.username}_avatar_{filename}"

            user.avatar.save(
                sanitized_filename,
                ContentFile(response.content),
                save=False,
            )
            user.save()
        except requests.RequestException as e:
            print(f"Failed to save avatar: {str(e)}")

    @staticmethod
    def _update_user_data(user, idinfo):
        UserData.objects.update_or_create(
            user=user,
            defaults={
                "provider": RegisterTypeChoices.GOOGLE,
                "uid": idinfo["sub"],
                "extra_data": idinfo,
            },
        )

    @staticmethod
    def get_auth_url():
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
        client_id = os.getenv("GOOGLE_CLIENT_ID")

        if not redirect_uri or not client_id:
            raise ValueError("GOOGLE_REDIRECT_URI yoki GOOGLE_CLIENT_ID aniqlanmagan.")

        scopes = [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid",
        ]

        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": " ".join(scopes),
            "access_type": "offline",  # Ushbu parametrni "refresh token" olish uchun qo'shishingiz mumkin
            "prompt": "consent",  # Foydalanuvchi har doim ruxsatni tasdiqlashi uchun
        }

        url = f"https://accounts.google.com/o/oauth2/auth?{urllib.parse.urlencode(params)}"
        return url
