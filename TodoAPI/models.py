from django.contrib.auth.models import User
from django.db import models

class TodoList(models.Model):
    user = models.ForeignKey(User, related_name='lists')
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now=True)

    def number_of_items(self):
        return self.items.count()

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return self.name

class TodoItem(models.Model):
    list = models.ForeignKey(TodoList, related_name='items')
    created_at = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=128)
    hidden = models.BooleanField()

    class Meta:
        unique_together = ('list', 'text')

    def __str__(self):
        return self.text
