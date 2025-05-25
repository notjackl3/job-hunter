from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm
from . import views

urlpatterns = [
    path("login-user/", views.login_user, name="login_user"),
    path("signup-user/", views.signup_user, name="signup_user"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
            form_class=CustomPasswordResetForm,
            template_name='registration/password-reset.html',
            email_template_name='registration/password_reset_email.txt',
            subject_template_name='registration/password_reset_subject.txt'),
        name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(            template_name='registration/password-reset-done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password-reset-confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(), 
         name='password_reset_complete'),
]
