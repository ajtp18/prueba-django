from django.urls import path
from apps.accounts.views import CreateUser, UserLogin, UserLogout

urlpatterns = [
    path('register/', CreateUser.as_view(), name='user-create'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', UserLogout.as_view(), name='user-logout'),
]