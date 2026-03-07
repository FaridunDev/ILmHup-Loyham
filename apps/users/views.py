from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.utils import load_strategy, load_backend
from social_core.exceptions import MissingBackend
from .serializers import RegisterSerializer, UserProfileSerializer, MyTokenObtainPairSerializer

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


@extend_schema(tags=['Users'], summary="Login qilish - token, rol va ism qaytaradi")
@method_decorator(ratelimit(key='ip', rate='5/m', method='POST', block=True), name='post')
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@extend_schema(tags=['Users'], summary="JWT tokenni yangilash (refresh)")
class MyTokenRefreshView(TokenRefreshView):
    pass


@extend_schema(tags=['Users'], summary="Ijtimoiy tarmoq orqali login (google, github, facebook)")
class SocialAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, backend):
        token = request.data.get('access_token')
        if not token:
            return Response(
                {'error': 'access_token kerak'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            strategy = load_strategy(request)
            backend_obj = load_backend(strategy, backend, redirect_uri=None)
            user = backend_obj.do_auth(token)
            if not user:
                return Response(
                    {'error': 'Foydalanuvchi topilmadi'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'full_name': user.get_full_name() or user.username,
                'email': user.email,
                'role': 'instructor' if user.is_instructor else 'student',
            })
        except MissingBackend:
            return Response(
                {'error': "Noto'g'ri backend"},
                status=status.HTTP_400_BAD_REQUEST
            )