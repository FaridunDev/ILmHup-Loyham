from django.urls import path
from .views import MarkLessonCompleteView, MyCourseProgressView, CourseProgressDetailView

urlpatterns = [
    path('', MyCourseProgressView.as_view(), name='my-progress'),
    path('course/<int:course_pk>/', CourseProgressDetailView.as_view(), name='course-progress'),
    path('lesson/<int:lesson_pk>/complete/', MarkLessonCompleteView.as_view(), name='lesson-complete'),
]
