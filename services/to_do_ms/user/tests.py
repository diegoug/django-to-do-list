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
            'first_name': 'Testing',
            'last_name': 'Testing',
            'username': 'testing1'
        }

    def test_signup_user(self):
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(json.loads(response.content), {
            "username":self.user['username'],
            "first_name":self.user['first_name'],
            "last_name":self.user['last_name'],
            "email":self.user['email']
        })
    
    def test_login_user(self):
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.post(
                reverse('user-login'), {
                'email': self.user['email'],
                'password': self.user['password'],
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        result = json.loads(response.content)
        self.assertIn('client_secret', result)
        self.assertIn('client_id', result)
