from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.courses.models import Course
from apps.enrollments.models import Enrollment

User = get_user_model()


class ReviewTest(TestCase):
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
        Enrollment.objects.create(user=self.student, course=self.course)

    def test_create_review(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.post('/api/v1/reviews/create/', {
            'course': self.course.id,
            'rating': 5,
            'comment': 'Ajoyib kurs!'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_course_reviews(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(f'/api/v1/reviews/course/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_unauthorized(self):
        response = self.client.post('/api/v1/reviews/create/', {
            'course': self.course.id,
            'rating': 5,
            'comment': 'Test'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)