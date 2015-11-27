from TodoAPI.models import TodoList, TodoItem
from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view their items,
    and to restrict anonymous users from using the views entirely.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, TodoList):
            return obj.user == request.user
        elif isinstance(obj, TodoItem):
            return obj.list.user == request.user

    def has_permission(self, request, view):
        return not isinstance(request.user, AnonymousUser)
