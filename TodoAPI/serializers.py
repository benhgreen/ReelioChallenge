from django.contrib.auth.models import User
from rest_framework import serializers
from TodoAPI.models import TodoList, TodoItem
from rest_framework.exceptions import PermissionDenied


class TodoItemSerializer(serializers.ModelSerializer):
    list = serializers.StringRelatedField()

    def create(self, validated_data):
        item = TodoItem(**validated_data)
        user_lists = TodoList.objects.filter(user=self.context['request'].user)
        if validated_data['list'] not in user_lists:
            raise PermissionDenied(detail="That list is not available to you!")
        item.hidden = False
        item.save()
        return item

    class Meta:
        model = TodoItem
        fields = ('id', 'text', 'list', 'created_at')


class TodoListSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        query = TodoItem.objects.filter(list=obj.id, hidden=False)
        serializer = TodoItemSerializer(query, many=True)
        return serializer.data

    def create(self, validated_data):
        list = TodoList(**validated_data)
        list.user = self.context['request'].user
        list.save()
        return list

    class Meta:
        model = TodoList
        fields = (
            'id', 'name', 'number_of_items', 'items', 'created_at'
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email'
        )


