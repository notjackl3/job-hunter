from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class JobPost(models.Model):
    id = models.AutoField(primary_key=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    site = models.CharField(max_length=100, default="none")
    title = models.CharField(max_length=200, default="none")
    company = models.CharField(max_length=200, default="none")
    # date_posted = models.CharField(max_length=100, default="none")
    date_posted = models.DateField(default=None, null=True, blank=True)
    description = models.TextField(default="none")
    location = models.CharField(max_length=200, default="none")
    keywords = models.CharField(default="none")
    link = models.CharField(default="none")

    def __str__(self):
        return f"{self.title} | {self.company}"
