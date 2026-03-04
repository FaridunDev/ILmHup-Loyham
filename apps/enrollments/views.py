from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema # Importni qo'shdik
from .models import Enrollment
from .serializers import EnrollmentSerializer

@extend_schema(
    tags=['Kurslarga yozilish (Enrollments)'], 
    summary="Yangi kursga yozilish",
    description="Foydalanuvchi tanlangan kursga a'zo bo'ladi. Agar foydalanuvchi allaqachon a'zo bo'lsa, xatolik qaytaradi."
)
class EnrollView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if Enrollment.objects.filter(user=self.request.user, course=course).exists():
            raise ValidationError({'detail': 'Siz allaqachon bu kursga yozilgansiz!'})
        serializer.save(user=self.request.user)

@extend_schema(
    tags=['Kurslarga yozilish (Enrollments)'], 
    summary="Foydalanuvchining barcha kurslari ro'yxati",
    description="Tizimga kirgan foydalanuvchi o'zi yozilgan (sotib olgan) barcha kurslar ro'yxatini ko'ra oladi."
)
class MyEnrollmentsView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Enrollment.objects.filter(
            user=self.request.user
        ).select_related('course')