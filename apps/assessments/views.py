from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema # Importni qo'shdik
from .models import Quiz, QuizResult, Answer
from .serializers import QuizSerializer, QuizSubmitSerializer, QuizResultSerializer
from apps.enrollments.models import Enrollment

@extend_schema(
    tags=['Testlar (Assessments)'], 
    summary="Test savollarini olish",
    description="Muayyan testning barcha savollari va javob variantlarini ko'rish."
)
class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (permissions.IsAuthenticated,)

@extend_schema(
    tags=['Testlar (Assessments)'], 
    summary="Testni topshirish va natijani hisoblash",
    description="Foydalanuvchi tanlagan javob ID-larini yuboradi. Tizim avtomatik tekshirib, natijani saqlaydi."
)
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

@extend_schema(
    tags=['Testlar (Assessments)'], 
    summary="Foydalanuvchining barcha test natijalari",
    description="Tizimga kirgan foydalanuvchi topshirgan barcha testlari va ulardan olgan ballari ro'yxati."
)
class MyQuizResultsView(generics.ListAPIView):
    serializer_class = QuizResultSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return QuizResult.objects.filter(user=self.request.user)