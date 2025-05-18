from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.add_job),
    path("write-cover-letter/", views.write_cover_letter),
    path("show-statistics/", views.show_statistics),
    path("delete/<int:id>/", views.delete_job, name="delete_job")
]
