from rest_framework import serializers
from .models import Quiz, Question, Answer, QuizResult


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text')


class AnswerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'is_correct')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'order', 'answers')


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ('id', 'title', 'pass_percentage', 'questions')


class QuizSubmitSerializer(serializers.Serializer):
    answers = serializers.ListField(
        child=serializers.IntegerField(),
        help_text='Tanlangan javoblar ID lari'
    )


class QuizResultSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)

    class Meta:
        model = QuizResult
        fields = ('id', 'quiz_title', 'score', 'total', 'passed', 'submitted_at')
