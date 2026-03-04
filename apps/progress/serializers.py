from rest_framework import serializers
from .models import LessonCompletion, CourseProgress


class LessonCompletionSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)

    class Meta:
        model = LessonCompletion
        fields = ('id', 'lesson', 'lesson_title', 'completed_at')
        read_only_fields = ('completed_at',)


class CourseProgressSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = CourseProgress
        fields = ('id', 'course', 'course_title', 'percentage', 'is_completed', 'last_updated')
