from django.contrib.auth.models import User
from rest_framework import serializers
from TodoAPI.models import TodoList, TodoItem


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ('id', 'text', 'created_at')


class TodoListSerializer(serializers.HyperlinkedModelSerializer):
    items = TodoItemSerializer(many=True)

    class Meta:
        model = TodoList
        fields = (
        'id', 'name', 'user', 'number_of_items', 'items', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    lists = serializers.PrimaryKeyRelatedField(many=True,
                                               queryset=TodoList.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'lists')
