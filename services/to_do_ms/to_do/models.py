from django.db import models


class Task(models.Model):
    user = models.ForeignKey(
        'profiles.user', related_name='user', on_delete=models.CASCADE)
    title = models.CharField(
        "title", max_length=100)
    description = models.TextField(
        "description", blank=False)
    status = models.BooleanField(
        'staff status', default=False)
