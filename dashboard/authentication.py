from django.contrib.auth.backends import ModelBackend
from .models import Users

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = Users.objects.get(email=email)
            if user.check_password(password) and user.type == 0:
                return user
        except Users.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None