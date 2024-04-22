from django.contrib import admin
from django.urls import path
from apps.accounts.views import UserCreateAPIView, UserLoginAPIView

urlpatterns = [
    path('api/auth/register/', UserCreateAPIView.as_view(), name='user-create'),
    path('api/auth/login/', UserLoginAPIView.as_view(), name='user-login'),
]
