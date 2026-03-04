from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .serializers import RegisterSerializer, UserProfileSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

User = get_user_model()


@extend_schema(tags=['Users'], summary="Yangi foydalanuvchini ro'yxatdan o'tkazish")
@method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True), name='post')
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

@extend_schema(tags=['Users'], summary="Foydalanuvchi profilini ko'rish va tahrirlash")
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


@extend_schema(tags=['Users'], summary="Login qilish va JWT token olish")
class MyTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(tags=['Users'], summary="JWT tokenni yangilash (refresh)")
class MyTokenRefreshView(TokenRefreshView):
    pass