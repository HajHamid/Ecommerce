from django.urls import path 

from users import views


urlpatterns = [
    # path('login/', TokenObtainPairView.as_view(), name='user-login'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='user-login-refresh'),
    # path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('request-otp/', views.SendOTPView.as_view(), name='send-request-otp'),
    path('verify-otp/', views.VerfiyOTPView.as_view(), name='verify-otp')
]