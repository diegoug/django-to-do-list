import json

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from profiles.models import User

from django.utils.http import urlencode

def reverse_query(viewname, kwargs=None, query_kwargs=None):
    """
    Custom reverse to add a query string after the url
    Example usage:
    url = my_reverse('my_test_url', kwargs={'pk': object.id}, query_kwargs={'next': reverse('home')})
    """
    url = reverse(viewname, kwargs=kwargs)

    if query_kwargs:
        return f'{url}?{urlencode(query_kwargs)}'

    return url

class UserAuthenticationCase(TestCase):
    def setUp(self):
        self.user = {
            'email': 'testing@user-ms.com',
            'password': 'testPassword1234',
            'first_name': 'tst_name',
            'last_name': 'Testing',
            'username': 'testing1'
        }

        client = APIClient()

        response = client.post(
                reverse('user-signup'), {
                'email': self.user['email'],
                'password': self.user['password'],
                'password_confirmation': self.user['password'],
                'first_name': self.user['first_name'],
                'last_name': self.user['last_name'],
                'username': self.user['username']
            },
            format='multipart'
        )

        self.user_obj = User.objects.get(email=self.user['email'])

        response = client.post(reverse('user-login'), {
            'email': self.user['email'],
            'password': self.user['password'],
        }, format='json')
        
        result = json.loads(response.content)
        client_secret = result['client_secret']
        client_id = result['client_id']

        response = client.post(
                reverse('oauth2_provider:token'), {
                'grant_type': 'password',
                'client_id': client_id,
                'client_secret': client_secret,
                'username': self.user['email'],
                'password': self.user['password'],
            },
            format='multipart'
        )

        result = json.loads(response.content)
        self.access_token = result['access_token']

        self.task = {
            'user': str(self.user_obj.id),
            'title': 'Title test',
            'description': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard dummy text ever since the 1500s',
            'status': False
        }
    
    def test_api_post_task(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(reverse('task-list'), {
            'user': self.task['user'],
            'title': self.task['title'],
            'description': self.task['description'],
            'status': self.task['status']
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
