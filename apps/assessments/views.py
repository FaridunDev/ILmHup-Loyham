from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Quiz, QuizResult, Answer
from .serializers import QuizSerializer, QuizSubmitSerializer, QuizResultSerializer
from apps.enrollments.models import Enrollment


class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (permissions.IsAuthenticated,)


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


class MyQuizResultsView(generics.ListAPIView):
    serializer_class = QuizResultSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return QuizResult.objects.filter(user=self.request.user)
