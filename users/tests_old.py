from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status


class UserTest(APITestCase):
    def test_user_register(self):
        url = reverse('user-register')

        data = {
            'username': 'user',
            'password': 'hg@123456',
            'password2': 'hg@123456',
            'email': 'a@b.com'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.first().username, "user")
        self.assertEqual(get_user_model().objects.first().email, "a@b.com")

    def test_password_do_not_match(self):
        url = reverse('user-register')

        data = {
            'username': 'user',
            'password': 'hg@123456',
            'password2': 'hg123456',
            'email': 'a@b.com'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("passwords do not match", str(
            response.data.get('non_field_errors')[0]))
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_email_exists(self):
        get_user_model().objects.create_user(
            username='test',
            email='a@b.com',
            password='hg@123456',
        )

        url = reverse('user-register')

        data = {
            'username': 'user',
            'password': 'hg@123456',
            'password2': 'hg@123456',
            'email': 'a@b.com'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("User with this email already exists",
                         str(response.data.get('email')[0]))
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_username_exists(self):
        get_user_model().objects.create_user(
            username='test',
            email='a@b.com',
            password='hg@123456',
        )

        url = reverse('user-register')

        data = {
            'username': 'test',
            'password': 'hg@123456',
            'password2': 'hg@123456',
            'email': 'ab@b.com'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("User with this username already exists",
                         str(response.data.get('username')[0]))
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_user_login(self):
        get_user_model().objects.create_user(
            username='test',
            email='a@b.com',
            password='hg@123456',
        )

        url = reverse('user-login')
        data = {
            'username': 'test',
            'password': 'hg@123456'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_wrong_password(self):
        get_user_model().objects.create_user(
            username='test',
            email='a@b.com',
            password='hg@123456',
        )

        url = reverse('user-login')
        data = {
            'username': 'test',
            'password': 'wrong-password'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 401)
        self.assertNotIn('access', response.data)
