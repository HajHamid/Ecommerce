from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import Group

from core.models import BaseModel
from products.models import Product, Category, Brand


class Discount(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True, blank=True, null=True)

    percentage = models.PositiveSmallIntegerField(blank=True, null=True)
    amount = models.PositiveIntegerField(blank=True, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    max_usage_per_user = models.PositiveIntegerField(default=1)
    max_total_usage = models.PositiveIntegerField(blank=True, null=True)

    products = models.ManyToManyField(
        Product,
        blank=True,
        related_name='discounts'
    )
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='discounts'
    )
    brands = models.ManyToManyField(
        Brand,
        blank=True,
        related_name='discounts'
    )
    sellers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='seller_discounts'
    )
    user_groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='group_discounts'
    )
    allowed_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='user_specific_discounts'
    )

    def is_valid_for_user(self, user):
        now = timezone.now()
        if not self.is_active or not (self.start_datetime <= now <= self.end_datetime):
            return False

        if self.allowed_users.exists() and user not in self.allowed_users.all():
            return False

        # Check max usage per user
        usage_count = DiscountUsage.objects.filter(user=user, discount=self).count()
        if self.max_usage_per_user and usage_count >= self.max_usage_per_user:
            return False
        
        total_usage = DiscountUsage.objects.filter(discount=self).count()
        if self.max_total_usage and total_usage >= self.max_total_usage:
            return False

        return True


class DiscountUsage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} used {self.discount} at {self.used_at}"