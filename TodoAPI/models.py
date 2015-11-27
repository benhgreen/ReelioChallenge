from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

class TodoList(models.Model):
    user = models.OneToOneField(User)

class TodoItem(models.Model):
    list = models.ForeignKey(TodoList)
    created_at = models.DateTimeField(default=datetime.now())
    text = models.CharField(max_length=128)
    hidden = models.BooleanField()
