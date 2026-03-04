from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/v1/users/register/'
        self.login_url = '/api/v1/users/login/'
        self.profile_url = '/api/v1/users/profile/'

    def test_register_student(self):
        data = {
            'email': 'student@test.com',
            'username': 'student1',
            'password': 'testpass123',
            'password2': 'testpass123',
            'is_instructor': False
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_register_instructor(self):
        data = {
            'email': 'instructor@test.com',
            'username': 'instructor1',
            'password': 'testpass123',
            'password2': 'testpass123',
            'is_instructor': True
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.get(email='instructor@test.com').is_instructor)

    def test_register_password_mismatch(self):
        data = {
            'email': 'test@test.com',
            'username': 'test1',
            'password': 'testpass123',
            'password2': 'wrongpass123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        User.objects.create_user(
            email='test@test.com',
            username='test1',
            password='testpass123'
        )
        response = self.client.post(self.login_url, {
            'email': 'test@test.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_profile_unauthorized(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_authorized(self):
        user = User.objects.create_user(
            email='test@test.com',
            username='test1',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@test.com')
