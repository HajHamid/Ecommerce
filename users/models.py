import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from core.models import BaseModel


class Role(BaseModel):
    class RoleChoice(models.TextChoices):
        CUSTOMER = 'customer', 'Customer'
        VIP = 'vip', 'VIP'
        SELLER = 'seller', 'Seller'

    name = models.CharField(
        max_length=20, choices=RoleChoice.choices, unique=True)

    def __str__(self):
        return self.get_name_display()


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=11, unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    def is_vip(self):
        return self.role and self.role.name == Role.RoleChoice.VIP
    
    def is_seller(self):
        return self.role and self.role.name == Role.RoleChoice.SELLER
        
    def save(self, *args, **kwargs):
        if not self.role:
            self.role = Role.objects.get_or_create(name=Role.RoleChoice.CUSTOMER)[0]
        super().save(*args, **kwargs)



class OTP(models.Model):
    phone_number = models.CharField(max_length=11, db_index=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    otp_session_token = models.CharField(max_length=64, null=True, blank=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=2)

    @staticmethod
    def generate_code():
        return f"{random.randint(100000, 999999)}"
    
    @staticmethod
    def can_send_code(phone_number):
        one_minute_ago = timezone.now() - timezone.timedelta(minutes=1)
        return not OTP.objects.filter(phone_number=phone_number, created_at__gte=one_minute_ago).exists()
