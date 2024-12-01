from django.urls import path
# from .views import register, login_user, user_profile
from .views import SignupView, SigninView

urlpatterns = [
    # path('register/', register, name='register'),
    # path('login/', login_user, name='login'),
    # path('profile/', user_profile, name='user_profile'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
]