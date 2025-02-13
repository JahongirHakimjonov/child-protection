import json
import os
import time
import urllib.parse

import jwt
import requests
from django.core.files.base import ContentFile

from apps.users.models.users import RegisterTypeChoices, UserData, User
from apps.users.services.register import RegisterService


class Apple:
    @staticmethod
    def authenticate(code, id_token):
        try:
            token_data = Apple._fetch_token(code)
            idinfo = Apple._verify_token(id_token)
            user = Apple._get_or_create_user(idinfo)
            if idinfo.get("picture"):
                Apple._save_user_avatar(user, idinfo["picture"])
            Apple._update_user_data(user, idinfo)
            return user.tokens()
        except (ValueError, requests.RequestException) as e:
            raise ValueError(f"Authentication failed: {str(e)}")

    @staticmethod
    def _fetch_token(code):
        response = requests.post(
            "https://appleid.apple.com/auth/token",
            data={
                "code": code,
                "client_id": os.getenv("APPLE_CLIENT_ID"),
                "client_secret": Apple._generate_client_secret(),
                "redirect_uri": os.getenv("APPLE_REDIRECT_URI"),
                "grant_type": "authorization_code",
            },
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _generate_client_secret():
        headers = {"kid": os.getenv("APPLE_KEY_ID")}
        payload = {
            "iss": os.getenv("APPLE_TEAM_ID"),
            "iat": int(time.time()),
            "exp": int(time.time()) + 86400 * 180,  # 180 days expiration
            "aud": "https://appleid.apple.com",
            "sub": os.getenv("APPLE_CLIENT_ID"),
        }

        client_secret = jwt.encode(
            payload,
            os.getenv("APPLE_PRIVATE_KEY").replace("\\n", "\n"),
            algorithm="ES256",
            headers=headers,
        )
        return client_secret

    @staticmethod
    def _verify_token(id_token):
        headers = jwt.get_unverified_header(id_token)
        kid = headers["kid"]
        public_key = Apple._get_public_key(kid)
        return jwt.decode(
            id_token,
            public_key,
            algorithms=["RS256"],
            audience=os.getenv("APPLE_CLIENT_ID"),
        )

    @staticmethod
    def _get_public_key(kid):
        response = requests.get("https://appleid.apple.com/auth/keys")
        response.raise_for_status()
        keys = response.json()["keys"]
        for key in keys:
            if key["kid"] == kid:
                return jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
        raise ValueError("Public key not found")

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
                "register_type": RegisterTypeChoices.APPLE,
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
                "provider": RegisterTypeChoices.APPLE,
                "uid": idinfo["sub"],
                "extra_data": idinfo,
            },
        )

    @staticmethod
    def get_auth_url():
        redirect_uri = os.getenv("APPLE_REDIRECT_URI")
        client_id = os.getenv("APPLE_CLIENT_ID")

        if not redirect_uri or not client_id:
            raise ValueError("APPLE_REDIRECT_URI or APPLE_CLIENT_ID not defined.")

        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code id_token",
            "scope": "name email",
            "response_mode": "form_post",
            "state": "random_state_string",
            "nonce": "random_nonce_string",
        }

        url = (
            f"https://appleid.apple.com/auth/authorize?{urllib.parse.urlencode(params)}"
        )
        return url
