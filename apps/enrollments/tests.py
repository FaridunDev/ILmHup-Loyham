from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.courses.models import Course
from .models import Enrollment

User = get_user_model()


class EnrollmentTest(TestCase):
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
        self.course = Course.objects.create(
            instructor=self.instructor,
            title='Test Kurs',
            description='Tavsif',
            is_published=True
        )

    def test_enroll_success(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.post('/api/v1/enrollments/enroll/', {'course': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 1)

    def test_enroll_duplicate(self):
        self.client.force_authenticate(user=self.student)
        self.client.post('/api/v1/enrollments/enroll/', {'course': self.course.id})
        response = self.client.post('/api/v1/enrollments/enroll/', {'course': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_my_enrollments(self):
        Enrollment.objects.create(user=self.student, course=self.course)
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/v1/enrollments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
