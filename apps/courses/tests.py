from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Course, Module, Lesson

User = get_user_model()


class CourseTest(TestCase):
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
            password='testpass123',
            is_student=True
        )
        self.course = Course.objects.create(
            instructor=self.instructor,
            title='Test Kurs',
            description='Test tavsif',
            is_published=True
        )

    def test_course_list_public(self):
        response = self.client.get('/api/v1/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_create_instructor(self):
        self.client.force_authenticate(user=self.instructor)
        data = {
            'title': 'Yangi Kurs',
            'description': 'Tavsif',
            'level': 'beginner',
            'language': 'Uzbek'
        }
        response = self.client.post('/api/v1/courses/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_course_create_student_forbidden(self):
        self.client.force_authenticate(user=self.student)
        data = {
            'title': 'Yangi Kurs',
            'description': 'Tavsif',
        }
        response = self.client.post('/api/v1/courses/create/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_detail(self):
        response = self.client.get(f'/api/v1/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Kurs')
