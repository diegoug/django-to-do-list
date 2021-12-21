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
    
    def test_api_get_list_task(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(reverse('task-list'), {
            'user': self.task['user'],
            'title': self.task['title'],
            'description': self.task['description'],
            'status': self.task['status']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(reverse('task-list'), format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertIn('count', result)
        self.assertEqual(result['count'], 1)
    
    def test_api_get_list_search_task(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(reverse('task-list'), {
            'user': self.task['user'],
            'title': self.task['title'],
            'description': self.task['description'],
            'status': self.task['status']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(
            reverse_query('task-list', 
                query_kwargs={'search': 'Lorem Ipsum'}),
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertIn('count', result)
        self.assertEqual(result['count'], 1)
    
    def test_api_get_list_task_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(reverse('task-list'), {
            'user': self.task['user'],
            'title': self.task['title'],
            'description': self.task['description'],
            'status': self.task['status']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.post(reverse('task-list'), {
            'user': self.task_two['user'],
            'title': self.task_two['title'],
            'description': self.task_two['description'],
            'status': self.task_two['status']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(reverse('task-list'), format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertIn('count', result)
        self.assertEqual(result['count'], 1)
    
    def test_api_get_list_task_page(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        for i in range(0,5):
            response = client.post(reverse('task-list'), {
                'user': self.task['user'],
                'title': self.task['title'],
                'description': self.task['description'],
                'status': self.task['status']
            }, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(reverse('task-list'), format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result = json.loads(response.content)
        self.assertIn('count', result)
        self.assertIn('next', result)
        self.assertEqual(result['count'], 5)
    
    def test_api_put_task(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(reverse('task-list'), {
            'user': self.task['user'],
            'title': self.task['title'],
            'description': self.task['description'],
            'status': self.task['status']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        result = json.loads(response.content)
        self.assertIn('id', result)

        response = client.put(
            reverse('task-detail', kwargs={'pk': result['id']}), {
                'user': self.task['user'],
                'title': self.task_two['title'],
                'description': self.task_two['description'],
                'status': True
            }, format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_delete_user(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        response = client.post(reverse('task-list'), {
            'user': self.task['user'],
            'title': self.task['title'],
            'description': self.task['description'],
            'status': self.task['status']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        result = json.loads(response.content)
        self.assertIn('id', result)

        response = client.delete(
            reverse('task-detail', kwargs={'pk': result['id']}), 
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

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
            'description': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys',
            'status': False
        }

        self.user_two = {
            'email': 'testing@user-two-ms.com',
            'password': 'testPassword1234',
            'first_name': 'tst_name',
            'last_name': 'Testing',
            'username': 'testing2'
        }

        response = client.post(
                reverse('user-signup'), {
                'email': self.user_two['email'],
                'password': self.user_two['password'],
                'password_confirmation': self.user_two['password'],
                'first_name': self.user_two['first_name'],
                'last_name': self.user_two['last_name'],
                'username': self.user_two['username']
            },
            format='multipart'
        )

        self.user_obj = User.objects.get(email=self.user_two['email'])

        response = client.post(reverse('user-login'), {
            'email': self.user_two['email'],
            'password': self.user_two['password'],
        }, format='json')
        
        result = json.loads(response.content)
        client_two_secret = result['client_secret']
        client_two_id = result['client_id']

        response = client.post(
                reverse('oauth2_provider:token'), {
                'grant_type': 'password',
                'client_id': client_two_id,
                'client_secret': client_two_secret,
                'username': self.user_two['email'],
                'password': self.user_two['password'],
            },
            format='multipart'
        )

        result = json.loads(response.content)
        self.access_token_two = result['access_token']

        self.task_two = {
            'user': str(self.user_obj.id),
            'title': 'Title test 2',
            'description': 'standard dummy text ever since the 1500s',
            'status': False
        }
