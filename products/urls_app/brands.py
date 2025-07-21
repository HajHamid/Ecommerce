from django.urls import path

from products.views_app import brand

urlpatterns = [
    path('brands/', brand.BrandListView.as_view(), name='brand-list'),
]