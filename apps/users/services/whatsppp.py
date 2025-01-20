import os
import urllib.parse

import requests

from apps.users.models import RegisterTypeChoices, User, UserData
from apps.users.services.register import RegisterService


class WhatsApp:
    @staticmethod
    def authenticate(code):
        try:
            token_data = WhatsApp._fetch_token(code)
            user_info = WhatsApp._fetch_user_info(token_data["access_token"])
            user = WhatsApp._get_or_create_user(user_info)
            WhatsApp._update_user_data(user, token_data, user_info)
            return user.tokens()
        except (ValueError, requests.RequestException) as e:
            raise ValueError(f"Authentication failed: {str(e)}")

    @staticmethod
    def _fetch_token(code):
        response = requests.post(
            "https://graph.facebook.com/v21.0/oauth/access_token",
            params={
                "client_id": os.getenv("WHATSAPP_CLIENT_ID"),
                "client_secret": os.getenv("WHATSAPP_CLIENT_SECRET"),
                "redirect_uri": os.getenv("WHATSAPP_REDIRECT_URI"),
                "code": code,
            },
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _fetch_user_info(access_token):
        response = requests.get(
            "https://graph.facebook.com/me",
            params={
                "access_token": access_token,
                "fields": "id,name,email",
            },
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _get_or_create_user(user_info):
        user, created = User.objects.get_or_create(
            email=user_info["email"],
            defaults={
                "username": RegisterService.check_unique_username(
                    user_info["email"].split("@")[0]
                ),
                "first_name": user_info.get("name", "").split()[0],
                "last_name": " ".join(user_info.get("name", "").split()[1:]),
                "is_active": True,
                "register_type": RegisterTypeChoices.WHATSAPP,
            },
        )
        return user

    @staticmethod
    def _update_user_data(user, token_data, user_info):
        UserData.objects.update_or_create(
            user=user,
            defaults={
                "provider": RegisterTypeChoices.WHATSAPP,
                "uid": user_info["id"],
                "extra_data": {
                    "access_token": token_data["access_token"],
                    "user_info": user_info,
                },
            },
        )

    @staticmethod
    def get_auth_url():
        redirect_uri = os.getenv("WHATSAPP_REDIRECT_URI")
        client_id = os.getenv("WHATSAPP_CLIENT_ID")
        api_version = os.getenv("FACEBOOK_API_VERSION", "v21.0")
        scopes = [
            # "whatsapp_business_management",
            # "whatsapp_business_messaging",
            "email",
            "public_profile",
        ]
        scope = urllib.parse.quote(" ".join(scopes))
        url = (
            f"https://www.facebook.com/{api_version}/dialog/oauth?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code&"
            f"scope={scope}"
        )
        return url
