import base64
import binascii
import re

import jwt
from django.http import JsonResponse

from apps.shared.services import PremiumService


class CinemaVideoAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        pattern = r"^/media/hls_videos/cinema/(?P<dynamic_part>[^/]+)/"

        match = re.match(pattern, request.path)
        if match:
            dynamic_part = match.group("dynamic_part")
            x_panda_id = request.headers.get("X-Panda-Id")
            x_panda_object_id = request.headers.get("X-Panda-Object-Id")
            x_panda_api_key = request.headers.get("X-Panda-Api-Key")

            if not x_panda_id or not x_panda_object_id or not x_panda_api_key:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Missing required headers: X-Panda-Id, X-Panda-Object-Id, and X-Panda-Api-Key.",
                        "data": {
                            "url": request.build_absolute_uri(),
                        },
                    },
                    status=403,
                )

            try:
                decoded_dynamic_part = base64.b64decode(dynamic_part).decode("utf-8")
            except (binascii.Error, UnicodeDecodeError):
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Invalid dynamic_part encoding.",
                        "data": {
                            "url": request.build_absolute_uri(),
                        },
                    },
                    status=403,
                )

            try:
                decoded_token = jwt.decode(
                    x_panda_api_key, options={"verify_signature": False}
                )
                user_id = decoded_token.get("user_id")
            except jwt.DecodeError:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Invalid Api Key token.",
                        "data": {
                            "url": request.build_absolute_uri(),
                        },
                    },
                    status=403,
                )

            if decoded_dynamic_part != x_panda_object_id and user_id != int(x_panda_id):
                return JsonResponse(
                    {
                        "success": False,
                        "message": "You do not have access to this video. Invalid X-Panda-Id or X-Panda-Object-Id.",
                        "data": {
                            "url": request.build_absolute_uri(),
                        },
                    },
                    status=403,
                )

            if not PremiumService.has_access(x_panda_id, x_panda_object_id):
                return JsonResponse(
                    {
                        "success": False,
                        "message": "You do not have access to this video. Please subscribe to our premium plan",
                        "data": {
                            "url": request.build_absolute_uri(),
                        },
                    },
                    status=403,
                )

        return self.get_response(request)
