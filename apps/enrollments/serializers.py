from rest_framework import serializers
from .models import Enrollment
from apps.courses.serializers import CourseListSerializer


class EnrollmentSerializer(serializers.ModelSerializer):
    course_detail = CourseListSerializer(source='course', read_only=True)

    class Meta:
        model = Enrollment
        fields = ('id', 'course', 'course_detail', 'status', 'enrolled_at')
        read_only_fields = ('status', 'enrolled_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
