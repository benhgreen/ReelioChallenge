from django.contrib.auth.models import User
from rest_framework import serializers
from TodoAPI.models import TodoList, TodoItem


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = ('id', 'text', 'list', 'created_at')


class TodoListSerializer(serializers.ModelSerializer):
    items = TodoItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()

    def create(self, validated_data):
        list = TodoList(**validated_data)
        list.user = self.context['request'].user
        list.save()
        return list

    class Meta:
        model = TodoList
        fields = (
            'id', 'name', 'user', 'number_of_items', 'items', 'created_at'
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email'
        )


