from datetime import timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings
from django.utils import timezone
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

    # How many people the room is sized for. The creator picks this up front,
    # joining is refused once the room is full, and starting early requires an
    # explicit force. Existing rooms take the lowest allowed value, which is
    # the only default that cannot retroactively make a full room look unfull.
    MIN_PARTICIPANTS = 3
    MAX_PARTICIPANTS = 9

    max_participants = models.IntegerField(
        default=MIN_PARTICIPANTS,
        validators=[
            MinValueValidator(MIN_PARTICIPANTS),
            MaxValueValidator(MAX_PARTICIPANTS),
        ],
    )

    time_limit_minutes = models.IntegerField(
        default=60
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    ROOM_STATUS = [
        ('waiting', 'Waiting'),
        ('active', 'Active'),
        ('finished', 'Finished')
    ]
    status = models.CharField(
        max_length = 20,
        choices = ROOM_STATUS,
        default = 'waiting'
    )

    started_at = models.DateTimeField(
        null = True,
        blank = True
    )

    ended_at = models.DateTimeField(
        null=True,
        blank=True
    )

    @property
    def is_full(self):
        return self.participants.count() >= self.max_participants

    @property
    def ends_at(self):
        """When this room's clock runs out, or None if it hasn't started."""
        if self.started_at is None:
            return None
        return self.started_at + timedelta(minutes=self.time_limit_minutes)

    def settle_if_expired(self):
        """
        Flip an active room to finished once its clock has run out, and report
        whether that just happened.

        Nothing ends a room on its own: it needs the creator to press End, or
        to still have the contest page open at expiry. A creator who simply
        closes the tab leaves the room active forever, which also traps every
        participant, because leaving an active room is refused. Read paths
        call this so an abandoned room settles itself on the next request.

        ended_at is backdated to the deadline rather than set to now, so a
        room that nobody touched for a week does not claim to have run for
        one.
        """
        deadline = self.ends_at
        if self.status != "active" or deadline is None or timezone.now() <= deadline:
            return False

        self.status = "finished"
        self.ended_at = deadline
        self.save(update_fields=["status", "ended_at"])
        return True

    def __str__(self):
        return self.room_code
