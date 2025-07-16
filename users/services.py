from django.contrib.auth import get_user_model

from users.models import CustomUser

def create_user(username: str, password: str, email: str) -> CustomUser:
    return get_user_model().objects.create_user(
        username=username,
        password=password,
        email=email
    )