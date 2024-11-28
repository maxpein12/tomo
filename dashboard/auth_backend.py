from django.contrib.auth.hashers import BasePasswordHasher
from hashlib import sha256

class SHA2PasswordHasher(BasePasswordHasher):
    algorithm = "sha2"

    def encode(self, password, salt):
        hash = sha256((password + salt).encode()).hexdigest()
        return f"sha2${salt}${hash}"

    def verify(self, password, encoded):
        algorithm, salt, hash = encoded.split("$")
        encoded_2 = self.encode(password, salt)
        return encoded == encoded_2