import hashlib
import hmac
import time
from urllib.parse import urlparse, parse_qs

from django.http import HttpResponseForbidden

from core import settings

SECRET_KEY = settings.SECRET_KEY


class SignedURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        parsed_url = urlparse(request.get_full_path())
        path = parsed_url.path

        # Check if the path starts with /media/hls_videos/
        if not path.startswith("/media/hls_videos/<int:video_id>/"):
            return self.get_response(request)

        query_params = parse_qs(parsed_url.query)
        expires = query_params.get("expires")
        signature = query_params.get("signature")

        # If `expires` or `signature` is missing, deny access
        if not expires or not signature:
            return HttpResponseForbidden("Access Denied")

        expires = int(expires[0])

        # If the URL has expired, deny access
        if expires < time.time():
            return HttpResponseForbidden("URL Expired")

        # Validate the signature
        expected_signature = hmac.new(
            SECRET_KEY.encode(), f"{path}{expires}".encode(), hashlib.sha256
        ).hexdigest()
        if signature[0] != expected_signature:
            return HttpResponseForbidden("Invalid Signature")

        return self.get_response(request)
