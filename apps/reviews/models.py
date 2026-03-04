from django.db import models
from django.conf import settings
from apps.courses.models import Course


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'course')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.course.title} - {self.rating}★"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._update_course_rating()

    def _update_course_rating(self):
        from django.db.models import Avg
        avg = Review.objects.filter(course=self.course).aggregate(Avg('rating'))['rating__avg']
        self.course.average_rating = round(avg, 2) if avg else 0
        self.course.save(update_fields=['average_rating'])
