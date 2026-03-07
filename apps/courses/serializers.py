from rest_framework import serializers
from .models import Course, Module, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'content', 'video_url', 'order', 'is_preview', 'duration')


class LessonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'content', 'video_url', 'order', 'is_preview', 'duration')


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ('id', 'title', 'description', 'order', 'lessons')


class CourseListSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)
    modules_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'thumbnail', 'level',
                  'language', 'is_published', 'average_rating',
                  'instructor_name', 'modules_count', 'price', 'is_free', 'created_at')

    def get_modules_count(self, obj):
        return obj.modules.count()


class CourseDetailSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'thumbnail', 'level',
                  'language', 'is_published', 'average_rating',
                  'instructor_name', 'modules', 'price', 'is_free', 'created_at')


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'thumbnail', 'level', 'language', 'price', 'is_free')

    def create(self, validated_data):
        validated_data['instructor'] = self.context['request'].user
        return super().create(validated_data)


class CourseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'thumbnail',
                  'level', 'language', 'is_published', 'price', 'is_free')