from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LessonCompletion, CourseProgress
from .serializers import LessonCompletionSerializer, CourseProgressSerializer
from apps.courses.models import Lesson
from apps.enrollments.models import Enrollment


class MarkLessonCompleteView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, lesson_pk):
        lesson = Lesson.objects.get(pk=lesson_pk)
        course = lesson.module.course

        enrolled = Enrollment.objects.filter(
            user=request.user, course=course, status='active'
        ).exists()
        if not enrolled:
            return Response(
                {'detail': 'Bu kursga yozilmagansiz!'},
                status=status.HTTP_403_FORBIDDEN
            )

        completion, created = LessonCompletion.objects.get_or_create(
            user=request.user, lesson=lesson
        )

        progress, _ = CourseProgress.objects.get_or_create(
            user=request.user, course=course
        )
        progress.calculate()

        return Response({
            'detail': 'Dars tugatildi!' if created else 'Dars avval tugatilgan.',
            'progress': CourseProgressSerializer(progress).data
        })


class MyCourseProgressView(generics.ListAPIView):
    serializer_class = CourseProgressSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return CourseProgress.objects.filter(user=self.request.user)


class CourseProgressDetailView(generics.RetrieveAPIView):
    serializer_class = CourseProgressSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return CourseProgress.objects.get(
            user=self.request.user,
            course_id=self.kwargs['course_pk']
        )
