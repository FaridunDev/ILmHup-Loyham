from rest_framework import serializers
from .models import Review
from apps.enrollments.models import Enrollment


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user_name', 'course', 'rating', 'comment', 'created_at')
        read_only_fields = ('created_at',)

    def validate(self, attrs):
        user = self.context['request'].user
        course = attrs['course']
        if not Enrollment.objects.filter(user=user, course=course, status='active').exists():
            raise serializers.ValidationError({'detail': 'Faqat kursga yozilganlar sharh qoldira oladi!'})
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
