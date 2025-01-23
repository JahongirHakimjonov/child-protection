import traceback
from urllib.parse import parse_qs

import jwt
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidSignatureError,
    InvalidTokenError,
)

User = get_user_model()


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            query_string = parse_qs(scope["query_string"].decode("utf8"))
            jwt_token_list = query_string.get("token", None)
            if jwt_token_list:
                jwt_token = jwt_token_list[0]
                if not jwt_token or jwt_token.count(".") != 2:
                    print(f"Invalid JWT format: {jwt_token[:10]}...")
                    scope["user"] = AnonymousUser()
                else:
                    try:
                        jwt_payload = self.get_payload(jwt_token)
                        user_credentials = self.get_user_credentials(jwt_payload)
                        user = await self.get_logged_in_user(user_credentials)
                        scope["user"] = user
                    except (
                        InvalidSignatureError,
                        ExpiredSignatureError,
                        DecodeError,
                        InvalidTokenError,
                    ) as e:
                        print(f"JWT authentication error: {e}")
                        scope["user"] = AnonymousUser()
                    except Exception as e:
                        print(f"Unexpected error: {e}")
                        traceback.print_exc()
                        scope["user"] = AnonymousUser()
            else:
                print("No token provided in query string.")
                scope["user"] = AnonymousUser()
        except Exception as e:
            print(f"Error in middleware: {e}")
            traceback.print_exc()
            scope["user"] = AnonymousUser()
        return await self.app(scope, receive, send)

    def get_payload(self, jwt_token):
        """
        Decode the JWT token and return its payload.
        """
        if jwt_token.count(".") != 2:
            raise DecodeError(f"Invalid JWT format: {jwt_token[:10]}...")
        payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload

    def get_user_credentials(self, payload):
        """
        Extract user credentials (user ID) from the JWT payload.
        """
        user_id = payload.get("user_id")
        if not user_id:
            raise KeyError("user_id is missing in the JWT payload.")
        return user_id

    async def get_logged_in_user(self, user_id):
        """
        Retrieve the user from the database using user ID.
        """
        user = await self.get_user(user_id)
        return user

    @database_sync_to_async
    def get_user(self, user_id):
        """
        Fetch the user from the database or return AnonymousUser if not found.
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()


def JWTAuthMiddlewareStack(app):
    return JWTAuthMiddleware(AuthMiddlewareStack(app))
