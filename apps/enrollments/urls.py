from django.urls import path
from .views import EnrollView, MyEnrollmentsView

urlpatterns = [
    path('', MyEnrollmentsView.as_view(), name='my-enrollments'),
    path('enroll/', EnrollView.as_view(), name='enroll'),
]
