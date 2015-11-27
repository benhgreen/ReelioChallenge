from TodoAPI.models import TodoItem
from TodoAPI.permissions import IsOwner
from TodoAPI.serializers import TodoItemSerializer, TodoListSerializer, \
    UserSerializer
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response


class TodoListViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwner,)
    serializer_class = TodoListSerializer

    def get_queryset(self):
        return self.request.user.lists.all()


class TodoItemViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwner,)
    serializer_class = TodoItemSerializer

    def get_queryset(self):
        return TodoItem.objects.filter(list__user=self.request.user,
                                       hidden=False)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def create_user(request):
    """
    Creates a new user from the register/ endpoint
    :param request: POST with username, password, [email] fields
    :return: New user, in JSON
    """
    VALID_USER_FIELDS = [f.name for f in User._meta.fields]
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        user_data = {field: data for (field, data) in request.data.items()
                     if field in VALID_USER_FIELDS}
        user = User.objects.create_user(
            **user_data
        )
        return Response(UserSerializer(instance=user).data, status=201)
    else:
        return Response(serialized._errors, status=400)


@api_view(['POST'])
def restore_item(request, item_id):
    """
    Restore previously deleted item, making it viewable in item and list lists.
    :param request: Empty POST to recover/<id>, where <id> is an item owned by
                    the user.
    :param item_id: ID of item to restore.
    :return: Item in JSON format.
    """
    try:
        item = TodoItem.objects.get(pk=item_id)
    except ObjectDoesNotExist:
        return Response(status=404)
    else:
        if item.list.user == request.user:
            item.hidden = False
            item.save()
            return Response(TodoItemSerializer(item).data, 200)
        else:
            return Response(status=403)
