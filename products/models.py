from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericRelation


from core.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )
    is_active = models.BooleanField(default=True)


class Brand(BaseModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='brands/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='products'
    )
    tags = models.ManyToManyField(
        'ProductTag',
        blank=True,
        related_name='products'
    )
    comments = GenericRelation('comments.Comment')

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    base_price = models.PositiveIntegerField()
    is_active = models. BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        from django.db.models import Avg
        return self.ratings.aggregate(avg=Avg('rating'))['avg'] or 0


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_main = models.BooleanField(default=False)


class ProductAttribute(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    attribute = models.ForeignKey(
        ProductAttribute,
        on_delete=models.CASCADE,
        related_name='values'
    )
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.attribute.name} - {self.value}"


class CategoryAttribute(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('category', 'attribute')

    def __str__(self):
        return f"{self.category.name} - {self.attribute.name}"


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )
    attribute_values = models.ManyToManyField(ProductAttributeValue)

    sku = models.CharField(max_length=100, unique=True)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Variant of {self.product.name} - SKU: {self.sku}"


class ProductRating(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])  # 1 to 5
    comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-updated_at']


class DynamicPrice(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='dynamic_prices'
    )
    price = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def is_active(self):
        now = timezone.now()

        return self.start_time <= now <= self.end_time


class ProductTag(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
