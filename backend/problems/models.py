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
        ('string', 'String'),
        ('linked_list', 'Linked List'),
        ('stack_queue', 'Stack & Queue'),
        ('trees', 'Trees'),
        ('graphs', 'Graphs'),
        ('heap', 'Heap'),
        ('dp', 'DP'),
        ('greedy', 'Greedy'),
        ('backtracking', 'Backtracking'),
        ('binary_search', 'Binary Search'),
        ('two_pointers', 'Two Pointers'),
        ('sliding_window', 'Sliding Window'),
        ('bit_manipulation', 'Bit Manipulation'),
        ('math', 'Math'),
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
        return f"TestCase #{self.id} - {self.problem.title}"