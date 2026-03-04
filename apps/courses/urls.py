from django.urls import path
from .views import (
    CourseListView, CourseCreateView, CourseDetailView,
    InstructorCourseListView, ModuleCreateView,
    LessonCreateView, LessonDetailView
)

urlpatterns = [
    path('', CourseListView.as_view(), name='course-list'),
    path('create/', CourseCreateView.as_view(), name='course-create'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('my/', InstructorCourseListView.as_view(), name='instructor-courses'),
    path('<int:course_pk>/modules/', ModuleCreateView.as_view(), name='module-create'),
    path('modules/<int:module_pk>/lessons/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
]
