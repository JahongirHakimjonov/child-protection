from typing import Union

from rest_framework import exceptions


class BreakException(Exception):
    """
    Break exception
    """

    def __init__(self, *args, message: Union[str, None] = None, data=None):
        if data is None:
            data = []
        self.args = args
        self.message = message
        self.data = data


class MyApiException(exceptions.APIException):
    """
    My API Exception for API exceptions status code edit
    """

    status_code = 400

    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.data = data
        self.detail = {
            "success": success,
            "message": message,
            "data": data,
        }


class ResponseException:
    def __init__(
        self,
        success: bool = False,
        message: str = "",
        data: Union[dict, list, None] = None,
        exception: Union[BreakException, None] = None,
        **kwargs,
    ):
        if isinstance(exception, BreakException):
            raise exception

        if data is None:
            data = {}
        raise MyApiException(success, message, data)
