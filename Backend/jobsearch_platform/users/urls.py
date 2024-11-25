from django.urls import path
from .views import register, login_user, user_profile

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('profile/', user_profile, name='user_profile'),
]