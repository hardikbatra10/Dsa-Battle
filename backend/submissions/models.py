from django.db import models
from django.conf import settings
from rooms.models import Room
from problems.models import Problem
# Create your models here.

class Submission(models.Model):
    VERDICT_CHOICES = [
        ('accepted', 'Accepted'),
        ('pending', 'Pending'),
        ('wrong_answer', 'Wrong Answer'),  
        ('runtime_error', 'Runtime Error'),
        ('compilation_error', 'Compilation Error'),
        ('time_limit_exceeded', 'Time Limit Exceeded')
    ]
    LANGUAGE_CHOICES = [
        ('cpp', 'C++'),
        ('java', 'Java'),
        ('python', 'Python'),
        ('javascript', 'Javascript')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )
    room = models.ForeignKey(
        Room,
        on_delete = models.CASCADE
    )
    problem = models.ForeignKey(
        Problem,
        on_delete = models.CASCADE
    )
    code = models.TextField()

    language = models.CharField(
        max_length = 20,
        choices = LANGUAGE_CHOICES
    )
    verdict = models.CharField(
        max_length= 20,
        choices = VERDICT_CHOICES
    )
    submitted_at = models.DateTimeField(
        auto_now_add = True
    )
    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"
