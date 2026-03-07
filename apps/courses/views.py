from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .models import Course, Module, Lesson
from .serializers import (
    CourseListSerializer, CourseDetailSerializer,
    CourseCreateSerializer, CourseUpdateSerializer, ModuleSerializer,
    LessonSerializer, LessonDetailSerializer
)
from apps.enrollments.models import Enrollment


class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_instructor


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.instructor == request.user


@extend_schema(tags=['Kurslar (Courses)'], summary="Barcha nashr etilgan kurslar ro'yxatini olish")
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.filter(is_published=True)
    serializer_class = CourseListSerializer
    permission_classes = (permissions.AllowAny,)


@extend_schema(tags=['Kurslar (Courses)'], summary="Yangi kurs yaratish (Faqat o'qituvchilar uchun)")
class CourseCreateView(generics.CreateAPIView):
    serializer_class = CourseCreateSerializer
    permission_classes = (IsInstructor,)


@extend_schema(tags=['Kurslar (Courses)'], summary="Kurs ma'lumotlarini ko'rish, tahrirlash yoki o'chirish")
class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CourseDetailSerializer
        if self.request.method in ('PUT', 'PATCH'):
            return CourseUpdateSerializer
        return CourseCreateSerializer


@extend_schema(tags=['Kurslar (Courses)'], summary="O'qituvchining o'zi yaratgan kurslar ro'yxati")
class InstructorCourseListView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = (IsInstructor,)

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user)


@extend_schema(tags=['Kurslar (Courses)'], summary="Kurs ichida yangi modul yaratish")
class ModuleCreateView(generics.CreateAPIView):
    serializer_class = ModuleSerializer
    permission_classes = (IsInstructor,)

    def perform_create(self, serializer):
        course = Course.objects.get(pk=self.kwargs['course_pk'], instructor=self.request.user)
        serializer.save(course=course)


@extend_schema(tags=['Kurslar (Courses)'], summary="Modul ichida yangi dars yaratish")
class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonDetailSerializer
    permission_classes = (IsInstructor,)

    def perform_create(self, serializer):
        module = Module.objects.get(pk=self.kwargs['module_pk'])
        serializer.save(module=module)


@extend_schema(tags=['Kurslar (Courses)'], summary="Darsning to'liq mazmunini ko'rish (Video, kontent)")
class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        lesson = self.get_object()
        user = self.request.user
        if lesson.is_preview:
            return LessonDetailSerializer
        enrolled = Enrollment.objects.filter(
            user=user, course=lesson.module.course, status='active'
        ).exists()
        if enrolled or user.is_instructor:
            return LessonDetailSerializer
        return LessonSerializer