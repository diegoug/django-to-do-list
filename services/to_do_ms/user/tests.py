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
    
    def test_oauth_token(self):
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertIn('access_token', result)
        self.assertIn('refresh_token', result)
    
    def test_oauth_introspect(self):
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        access_token = result['access_token']

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

        response = client.post(
                reverse('oauth2_provider:introspect'), {
                'token': access_token,
                'client_id': client_id
            },
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertIn('active', result)
        self.assertEqual(result['active'], True)

class UserAPICase(TestCase):
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

        response = client.post(
                reverse('user-login'), {
                'email': self.user['email'],
                'password': self.user['password'],
            },
            format='json'
        )
        
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
        access_token = result['access_token']

        self.access_token = access_token
    
    def test_api_get_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.get(
            reverse('user-detail', 
                kwargs={'email': self.user['email']}), 
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertIn('email', result)
        self.assertEqual(result['email'], self.user['email'])

    def test_api_get_list_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.get(reverse('user-list'), format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertIn('count', result)
        self.assertEqual(result['count'], 1)
    
    def test_api_get_list_search_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.get(
            reverse_query('user-list', 
                query_kwargs={'search': self.user['first_name']}),
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertIn('count', result)
        self.assertEqual(result['count'], 1)
    
    def test_api_put_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.get(
            reverse_query('user-list', 
                query_kwargs={'search': self.user['first_name']}),
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertIn('count', result)
        self.assertEqual(result['count'], 1)

        response = client.put(
            reverse('user-detail', kwargs={'email': self.user['email']}), {
                'first_name': 'dago',
                'last_name': 'berto',
                'username': 'dagob'
            }, format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get(
            reverse_query('user-list', 
                query_kwargs={'search': self.user['first_name']}),
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertIn('count', result)
        self.assertEqual(result['count'], 0)

        response = client.get(
            reverse_query('user-list', 
                query_kwargs={'search': 'dago'}),
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertIn('count', result)
        self.assertEqual(result['count'], 1)

    def test_api_delete_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.delete(
            reverse('user-detail', kwargs={'email': self.user['email']}), 
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
