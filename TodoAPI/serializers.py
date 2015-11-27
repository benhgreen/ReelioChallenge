from rest_framework import serializers

from rest_framework.relations import StringRelatedField

from TodoAPI.models import TodoList, TodoItem


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ('text', 'created_at')

class TodoListSerializer(serializers.HyperlinkedModelSerializer):
    items = TodoItemSerializer(many=True)

    class Meta:
        model = TodoList
        fields = ('name', 'user', 'number_of_items', 'items', 'created_at')