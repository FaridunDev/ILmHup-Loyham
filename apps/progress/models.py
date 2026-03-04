from django.db import models
from django.conf import settings
from apps.courses.models import Lesson, Course


class LessonCompletion(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='completed_lessons'
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='completions')
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.email} - {self.lesson.title}"


class CourseProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='course_progress'
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress')
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_completed = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.email} - {self.course.title} - {self.percentage}%"

    def calculate(self):
        total = Lesson.objects.filter(module__course=self.course).count()
        if total == 0:
            return
        completed = LessonCompletion.objects.filter(
            user=self.user,
            lesson__module__course=self.course
        ).count()
        self.percentage = round((completed / total) * 100, 2)
        self.is_completed = self.percentage >= 100
        self.save()
