from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.courses.models import Course

User = get_user_model()


class AnalyticsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.instructor = User.objects.create_user(
            email='instructor@test.com',
            username='instructor1',
            password='testpass123',
            is_instructor=True,
            is_student=False
        )
        self.student = User.objects.create_user(
            email='student@test.com',
            username='student1',
            password='testpass123'
        )
        Course.objects.create(
            instructor=self.instructor,
            title='Test Kurs',
            description='Tavsif',
            is_published=True
        )

    def test_dashboard_instructor(self):
        self.client.force_authenticate(user=self.instructor)
        response = self.client.get('/api/v1/analytics/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('summary', response.data)
        self.assertIn('courses', response.data)

    def test_dashboard_unauthorized(self):
        response = self.client.get('/api/v1/analytics/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dashboard_student_forbidden(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/v1/analytics/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)