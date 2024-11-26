# auth_backend.py
import hashlib
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class SHA2Backend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        # Hash the provided password using SHA2
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Compare the hashed password with the one in the database
        if hashed_password == user.password:
            return user

        return None