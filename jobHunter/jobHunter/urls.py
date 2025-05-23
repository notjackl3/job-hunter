from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path('', auth_views.LoginView.as_view(), name="login"),
    path("users/", include("django.contrib.auth.urls")),
    path("users/", include("users.urls")),
    path("admin/", admin.site.urls),
    path("", include("jobHunt.urls")),
    path("logout/", auth_views.LogoutView.as_view(), name='logout'),
]
