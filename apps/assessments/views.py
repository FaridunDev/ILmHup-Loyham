from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Quiz, Question, Answer, QuizResult
from .serializers import (
    QuizSerializer, QuizCreateSerializer, QuizSubmitSerializer,
    QuizResultSerializer, QuestionCreateSerializer, AnswerCreateSerializer
)
from apps.enrollments.models import Enrollment
from apps.courses.models import Lesson


class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_instructor


@extend_schema(tags=['Testlar (Assessments)'], summary="Dars uchun yangi quiz yaratish (faqat o'qituvchi)")
class QuizCreateView(generics.CreateAPIView):
    serializer_class = QuizCreateSerializer
    permission_classes = (IsInstructor,)

    def perform_create(self, serializer):
        lesson = Lesson.objects.get(pk=self.kwargs['lesson_pk'])
        serializer.save(lesson=lesson)


@extend_schema(tags=['Testlar (Assessments)'], summary="Quizga savol va javoblar qo'shish (faqat o'qituvchi)")
class QuestionCreateView(generics.CreateAPIView):
    serializer_class = QuestionCreateSerializer
    permission_classes = (IsInstructor,)

    def perform_create(self, serializer):
        quiz = Quiz.objects.get(pk=self.kwargs['quiz_pk'])
        serializer.save(quiz=quiz)


@extend_schema(tags=['Testlar (Assessments)'], summary="Test savollarini olish")
class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (permissions.IsAuthenticated,)


@extend_schema(tags=['Testlar (Assessments)'], summary="Testni topshirish va natijani hisoblash")
class QuizSubmitView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        quiz = Quiz.objects.get(pk=pk)
        serializer = QuizSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        selected_ids = serializer.validated_data['answers']
        correct_answers = Answer.objects.filter(
            question__quiz=quiz, is_correct=True
        )
        correct_ids = set(correct_answers.values_list('id', flat=True))
        selected_set = set(selected_ids)

        score = len(correct_ids & selected_set)
        total = correct_answers.count()
        passed = (score / total * 100) >= quiz.pass_percentage if total > 0 else False

        result, _ = QuizResult.objects.update_or_create(
            user=request.user,
            quiz=quiz,
            defaults={'score': score, 'total': total, 'passed': passed}
        )

        return Response(QuizResultSerializer(result).data)


@extend_schema(tags=['Testlar (Assessments)'], summary="Foydalanuvchining barcha test natijalari")
class MyQuizResultsView(generics.ListAPIView):
    serializer_class = QuizResultSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return QuizResult.objects.filter(user=self.request.user)