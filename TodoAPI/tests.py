from TodoAPI.models import TodoList, TodoItem
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class TodoAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_info = {'username': 'test', 'email': 'a@a.com',
                          'password': '123456'}
        self.user = User(**self.user_info)
        self.alt_user_info = {'username': 'hey', 'password': 'hi'}

        self.list_url = reverse('lists-list')
        self.register_user_url = reverse('register_user')
        self.item_url = reverse('items-list')
        self.restore_url = reverse('restore', args=[1])

    def test_create_account(self):
        """
        Ensure we can create a new user.
        """
        data = self.user_info
        response = self.client.post(self.register_user_url, data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test')

    def test_lists_unavailable_anon(self):
        """
        Test lists are not accessible to anon users
        """
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, 403)

    def test_lists_available(self):
        """
        Test lists are  accessible to logged-in users
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_operations(self):
        """
        Ensure we can create a new list, add items, delete items, restore items,
        and delete the list
        """
        self.client.post(self.register_user_url, self.user_info, format='json')
        self.client.login(**self.user_info)

        # create a list
        list_data = {'name': 'test_list'}
        response = self.client.post(self.list_url, list_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(TodoList.objects.count(), 1)

        # add item to our list
        item_data = {'text': 'hey hi', 'list': 1}
        response = self.client.post(self.item_url, item_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(TodoItem.objects.count(), 1)
        self.assertEqual(TodoList.objects.first().items.count(), 1)

        # edit the list name
        new_list_data = {'name': 'cheeseburger'}
        response = self.client.patch(self.list_url + '1/', new_list_data,
                                     format='json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.data[0].get('name'), 'cheeseburger')

        # edit the item name
        new_item_data = {'text': 'fries'}
        response = self.client.patch(self.item_url + '1/', new_item_data,
                                     format='json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.item_url, format='json')
        self.assertEqual(response.data[0].get('text'), 'fries')

        # make sure we can see the new list
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(len(response.data), 1)

        # register new user
        self.client.post(self.register_user_url, self.alt_user_info,
                         format='json')

        # login as new user and make sure new list isn't there
        self.client.logout()
        self.client.login(**self.alt_user_info)
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(len(response.data), 0)

        # log back in as OG user and 'delete' the item
        self.client.logout()
        self.client.login(**self.user_info)
        response = self.client.delete(self.item_url + '1/', format='json')
        self.assertTrue(TodoItem.objects.first().hidden)

        # make sure our item is gone from the items list
        response = self.client.get(self.item_url, format='json')
        self.assertEqual(len(response.data), 0)

        # check the list itself for good measure
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(len(response.data[0].get('items')), 0)

        # restore the item
        response = self.client.post(self.restore_url, format='json')
        self.assertEqual(response.status_code, 200)

        # make sure the restored item appears in item list...
        response = self.client.get(self.item_url, format='json')
        self.assertEqual(len(response.data), 1)

        # ...and in the list itself
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(len(response.data[0].get('items')), 1)

        # delete the list
        response = self.client.delete(self.list_url + '1/', format='json')
        self.assertEqual(response.status_code, 204)

        # make sure list was done deleted good
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(len(response.data), 0)
