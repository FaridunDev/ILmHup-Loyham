from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Enrollment
from .serializers import EnrollmentSerializer


class EnrollView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if Enrollment.objects.filter(user=self.request.user, course=course).exists():
            raise ValidationError({'detail': 'Siz allaqachon bu kursga yozilgansiz!'})
        serializer.save(user=self.request.user)


class MyEnrollmentsView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Enrollment.objects.filter(
            user=self.request.user
        ).select_related('course')
