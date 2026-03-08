from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['full_name'] = self.user.get_full_name() or self.user.username
        data['email'] = self.user.email
        data['role'] = 'instructor' if self.user.is_instructor else 'student'
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)
    full_name = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'full_name', 'password', 'password2', 'is_instructor')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Parollar mos kelmadi!'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        full_name = validated_data.pop('full_name', '')
        user = User(**validated_data)
        if full_name:
            names = full_name.split(' ', 1)
            user.first_name = names[0]
            user.last_name = names[1] if len(names) > 1 else ''
        user.set_password(password)
        if validated_data.get('is_instructor'):
            user.is_student = False
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'avatar', 'bio', 'is_instructor', 'is_student')
        read_only_fields = ('email', 'is_instructor', 'is_student')