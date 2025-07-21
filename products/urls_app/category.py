from django.urls import path

from products.views_app import category

urlpatterns = [
    path('categories/', category.CategoryListView.as_view(), name='category-list'),
    path('categories/create/', category.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update/', category.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/', category.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/delete/', category.CategoryDeleteView.as_view(), name='category-delete'),
]
