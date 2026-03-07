from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.courses.models import Course, Module, Lesson
from apps.enrollments.models import Enrollment
from .models import Quiz, Question, Answer

User = get_user_model()


class AssessmentTest(TestCase):
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
        self.quiz = Quiz.objects.create(
            lesson=self.lesson,
            title='Test Quiz',
            pass_percentage=70
        )
        self.question = Question.objects.create(
            quiz=self.quiz,
            text='Savol?',
            order=1
        )
        self.correct_answer = Answer.objects.create(
            question=self.question,
            text='Togri javob',
            is_correct=True
        )
        self.wrong_answer = Answer.objects.create(
            question=self.question,
            text='Notogri javob',
            is_correct=False
        )
        Enrollment.objects.create(user=self.student, course=self.course)

    def test_quiz_create(self):
        lesson2 = Lesson.objects.create(
            module=self.module,
            title='2-dars',
            content='Kontent',
            order=2,
            duration=10
        )
        self.client.force_authenticate(user=self.instructor)
        response = self.client.post(
            f'/api/v1/assessments/lessons/{lesson2.id}/quiz/create/',
            {'title': 'Yangi Quiz', 'pass_percentage': 60}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_quiz_detail(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(f'/api/v1/assessments/{self.quiz.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Quiz')

    def test_quiz_submit_correct(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.post(
            f'/api/v1/assessments/{self.quiz.id}/submit/',
            {'answers': [self.correct_answer.id]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['passed'])

    def test_quiz_submit_wrong(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.post(
            f'/api/v1/assessments/{self.quiz.id}/submit/',
            {'answers': [self.wrong_answer.id]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['passed'])

    def test_quiz_results(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/v1/assessments/results/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)