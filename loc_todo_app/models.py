from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    latitude  = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    country = models.CharField(max_length=50)


class TodoItem(models.Model):                           
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="todo_item")
    def __str__(self):
        return self.name