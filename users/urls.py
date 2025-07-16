from django.urls import path 

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='user-login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='user-login-refresh'),
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
]