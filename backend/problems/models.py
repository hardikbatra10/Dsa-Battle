from django.db import models
from django.conf import settings


class Problem(models.Model):

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    TOPIC_CHOICES = [
        ('array', 'Array'),
        ('trees', 'Trees'),
        ('graphs', 'Graphs'),
        ('dp', 'DP'),
    ]

    title = models.CharField(
        max_length=255,
        unique=True
    )

    description = models.TextField()

    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES
    )

    topic = models.CharField(
        max_length=20,
        choices=TOPIC_CHOICES
    )

    example_input = models.TextField()

    example_output = models.TextField()

    constraints = models.TextField(
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title   
    
class TestCase(models.Model):
    problem = models.ForeignKey(
        Problem,
        on_delete = models.CASCADE,
        related_name= "test_cases"
    )

    input_data = models.TextField()

    expected_output = models.TextField()

    is_sample = models.BooleanField(
        default = False
    )
    def __str__(self):
        return f"{self.problem.title}"