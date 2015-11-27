from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from rest_framework import viewsets
from TodoAPI.serializers import TodoItemSerializer, TodoListSerializer, \
    UserSerializer
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def create_user(request):
    VALID_USER_FIELDS = [f.name for f in User._meta.fields]
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        user_data = {field: data for (field, data) in request.data.items()
                     if field in VALID_USER_FIELDS}
        user = User.objects.create_user(
            **user_data
        )
        return Response(UserSerializer(instance=user).data, status=200)
    else:
        return Response(serialized._errors, status=400)
