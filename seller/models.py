from django.db import models
from django.conf import settings

from core.models import BaseModel

class SellerProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_profile')
    shop_name = models.CharField(max_length=10)
    is_approved = models.BooleanField(default=False)


