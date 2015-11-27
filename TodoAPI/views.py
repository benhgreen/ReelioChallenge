from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics

# Create your views here.
from rest_framework import viewsets

from TodoAPI.serializers import TodoItemSerializer, TodoListSerializer, \
    UserSerializer
from rest_framework.permissions import IsAuthenticated


class TodoListViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TodoListSerializer

    def get_queryset(self):
        return self.request.user.lists.all()


class TodoItemViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TodoItemSerializer

    def get_queryset(self):
        items = set()
        for list in self.request.user.lists.all():
            items.add(list.items)
        return items

class UserViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer