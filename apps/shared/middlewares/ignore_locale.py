from core.settings import IGNORE_PATHS


class IgnoreStaticLocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if any(request.path.startswith(path) for path in IGNORE_PATHS):
            request.path_info = request.path
        return self.get_response(request)
