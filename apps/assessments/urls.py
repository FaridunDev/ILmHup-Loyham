from django.urls import path
from .views import QuizDetailView, QuizSubmitView, MyQuizResultsView

urlpatterns = [
    path('<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('<int:pk>/submit/', QuizSubmitView.as_view(), name='quiz-submit'),
    path('results/', MyQuizResultsView.as_view(), name='quiz-results'),
]
