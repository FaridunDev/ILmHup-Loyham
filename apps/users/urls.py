from django.urls import path
from .views import RegisterView, ProfileView, MyTokenObtainPairView, MyTokenRefreshView, SocialAuthView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token-refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('social/<str:backend>/', SocialAuthView.as_view(), name='social-auth'),
]