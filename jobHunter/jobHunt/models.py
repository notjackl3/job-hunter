from django.db import models


class JobPost(models.Model):
    site = models.CharField(max_length=100, default="none")
    title = models.CharField(max_length=200, default="none")
    company = models.CharField(max_length=200, default="none")
    date_posted = models.CharField(max_length=100, default="none")
    description = models.TextField(default="none")
    location = models.CharField(max_length=200, default="none")

    def __str__(self):
        return f"{self.title} | {self.company}"
