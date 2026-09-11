from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class FirstNameBackend(ModelBackend):
    """Foydalanuvchini email/username o'rniga ISM orqali autentifikatsiya qiladi.
    Ism har bir foydalanuvchida noyob bo'lishi kerak (RegisterForm buni tekshiradi)."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        first_name = username
        if first_name is None or password is None:
            return None
        try:
            user = User.objects.get(first_name__iexact=first_name.strip())
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
