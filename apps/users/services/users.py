from apps.shared import exceptions
from apps.shared.exceptions import ResponseException
from apps.users.models import User
from apps.users.services import SmsService


class UserService(SmsService):
    @staticmethod
    def send_confirmation(self, phone) -> bool:
        try:
            self.send_confirm(phone)
            return True
        except exceptions.SmsException as e:
            raise ResponseException(  # noqa
                success=False,
                message=str(e),
                data={"expired": str(e.kwargs.get("expired"))},
            )
        except Exception as e:
            raise ResponseException(  # noqa
                success=False, message=str(e), data={"expired": False}
            )

    @staticmethod
    def change_password(phone, password):
        """
        Change password
        """
        user = User.objects.filter(phone=phone).first()
        user.set_password(password)
        user.save()
