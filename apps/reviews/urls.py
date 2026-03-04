from django.urls import path
from .views import ReviewListView, ReviewCreateView, ReviewUpdateDeleteView

urlpatterns = [
    path('course/<int:course_pk>/', ReviewListView.as_view(), name='course-reviews'),
    path('create/', ReviewCreateView.as_view(), name='review-create'),
    path('<int:pk>/', ReviewUpdateDeleteView.as_view(), name='review-detail'),
]
