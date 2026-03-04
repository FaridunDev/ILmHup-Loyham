from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count, Avg
from apps.courses.models import Course
from apps.enrollments.models import Enrollment
from apps.reviews.models import Review


class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_instructor


class InstructorDashboardView(APIView):
    permission_classes = (IsInstructor,)

    def get(self, request):
        courses = Course.objects.filter(instructor=request.user)

        total_courses = courses.count()
        published_courses = courses.filter(is_published=True).count()

        total_students = Enrollment.objects.filter(
            course__instructor=request.user,
            status='active'
        ).values('user').distinct().count()

        avg_rating = Review.objects.filter(
            course__instructor=request.user
        ).aggregate(Avg('rating'))['rating__avg']

        course_stats = courses.annotate(
            students_count=Count('enrollments'),
            reviews_count=Count('reviews')
        ).values(
            'id', 'title', 'is_published',
            'students_count', 'reviews_count', 'average_rating'
        )

        return Response({
            'summary': {
                'total_courses': total_courses,
                'published_courses': published_courses,
                'total_students': total_students,
                'average_rating': round(avg_rating, 2) if avg_rating else 0,
            },
            'courses': list(course_stats)
        })
