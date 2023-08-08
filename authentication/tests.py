from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from authentication.models import User
from authentication.utils import get_user_tokens


class SignupAPITestCase(APITestCase):
    url = reverse('signup')

    def test_valid_data(self):
        """ Test to sign up with valid data """

        data = {
            'username': 'Shahryar',
            'email': 'shahryar@gmail.com',
            'password': 'shahryar12345',
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_missing_required_fields(self):
        """ Test with data having not given the input for required fields """

        data = {
            'email': 'shahryar@gmail.com',
            'password': 'shahryar12345',
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_weak_password(self):
        """ Test signing up a user with weak password """

        data = {
            'username': 'Shahryar',
            'email': 'shahryar@gmail.com',
            'password': '12345678',
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_existing_username(self):
        """ Test signing up a user with already used username """

        User.objects.create_user(
            username='Shahryar',
            email='shahryar@gmail.com',
            password='shahryar12345',
        )

        data = {
            'username': 'Shahryar',
            'email': 'shahryar@gmail.com',
            'password': 'shahryar12345',
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)


class LoginLogoutAPITestCase(APITestCase):

    def setUp(self):
        """ Creates sample user objects for testing """

        self.user = User.objects.create_user(
            username='Shahryar',
            email='shharyar@gmail.com',
            password='shahryar12345',
        )
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_valid_credentials(self):
        """ Test for logging-in with valid credentials """

        data = {
            'username': 'Shahryar',
            'password': 'shahryar12345',
        }

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_credentials(self):
        """ Test for logging-in with invalid credentials """

        data = {
            'username': 'Shahryar',
            'password': '12345678',
        }

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        """ Test for blacklisting the refresh token of authorized user """

        user_tokens = get_user_tokens(self.user)
        token = user_tokens['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.post(self.logout_url, {'refresh': user_tokens['refresh']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_logout(self):
        """ Test for blacklisting the refresh token of unauthorized user """

        response = self.client.post(self.logout_url, {'refresh': 'unauthorized token'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
