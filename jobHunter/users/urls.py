from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("login-user/", views.login_user, name="login_user"),
    path("signup-user/", views.signup_user, name="signup_user"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
