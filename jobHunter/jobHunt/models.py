from django.db import models
from django.utils import timezone


class JobPost(models.Model):
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
