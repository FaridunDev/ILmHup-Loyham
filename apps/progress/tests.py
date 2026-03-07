from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.courses.models import Course, Module, Lesson
from apps.enrollments.models import Enrollment

User = get_user_model()


class ProgressTest(TestCase):
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
        self.module = Module.objects.create(
            course=self.course,
            title='1-modul',
            order=1
        )
        self.lesson = Lesson.objects.create(
            module=self.module,
            title='1-dars',
            content='Kontent',
            order=1,
            duration=10
        )
        Enrollment.objects.create(user=self.student, course=self.course)

    def test_complete_lesson(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.post(f'/api/v1/progress/lesson/{self.lesson.id}/complete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('progress', response.data)

    def test_get_progress(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/v1/progress/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_course_progress(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(f'/api/v1/progress/course/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_progress_unauthorized(self):
        response = self.client.get('/api/v1/progress/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)