from django.urls import path
from .views import (
    QuizCreateView, QuizDetailView,
    QuizSubmitView, MyQuizResultsView,
    QuestionCreateView
)

urlpatterns = [
    path('lessons/<int:lesson_pk>/quiz/create/', QuizCreateView.as_view(), name='quiz-create'),
    path('quizzes/<int:quiz_pk>/questions/', QuestionCreateView.as_view(), name='question-create'),
    path('<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('<int:pk>/submit/', QuizSubmitView.as_view(), name='quiz-submit'),
    path('results/', MyQuizResultsView.as_view(), name='quiz-results'),
]