from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # You can add additional fields here if needed
    phone_number = models.CharField(max_length=11, blank=True, null=True)

    def __str__(self):
        return self.username