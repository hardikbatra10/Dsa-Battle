from django.db import models
from django.conf import settings
from problems.models import Problem


class Room(models.Model):

    topic = models.CharField(
        max_length=20,
        choices=Problem.TOPIC_CHOICES
    )

    difficulty = models.CharField(
        max_length=10,
        choices=Problem.DIFFICULTY_CHOICES
    )

    room_code = models.CharField(
        max_length=8,
        unique=True
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_rooms"
    )

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="joined_rooms",
        blank=True
    )

    selected_problems = models.ManyToManyField(
        Problem,
        related_name="rooms",
        blank=True
    )

    number_of_questions = models.IntegerField()

    time_limit_minutes = models.IntegerField(
        default=60
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.room_code