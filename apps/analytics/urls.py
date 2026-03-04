from django.urls import path
from .views import InstructorDashboardView

urlpatterns = [
    path('dashboard/', InstructorDashboardView.as_view(), name='instructor-dashboard'),
]
