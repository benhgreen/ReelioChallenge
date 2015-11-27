from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


    def has_permission(self, request, view):
        return not isinstance(request.user, AnonymousUser)

