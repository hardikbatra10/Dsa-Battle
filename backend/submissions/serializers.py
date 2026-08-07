from rest_framework import serializers
from .models import Submission
from problems.models import Problem
from rooms.models import Room

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission

        fields = [
            'id',
            'user',
            'room',
            'problem',
            'code',
            'language',
            'verdict',
            'failure_detail',
            'submitted_at'
        ]

        read_only_fields = [
            'user',
            'verdict',
            'failure_detail',
            'submitted_at'
        ]

class RunCodeSerializer(serializers.Serializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    problem = serializers.PrimaryKeyRelatedField(queryset=Problem.objects.all())
    code = serializers.CharField()
    language = serializers.ChoiceField(choices=Submission.LANGUAGE_CHOICES)

class SubmissionHistorySerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    problem_title = serializers.CharField(
        source="problem.title",
        read_only=True
    )

    class Meta:

        model = Submission

        fields = [
            "id",
            "username",
            "problem_title",
            "language",
            "verdict",
            "submitted_at",
        ]

class MySubmissionSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    problem_title = serializers.CharField(
        source="problem.title",
        read_only=True
    )

    topic = serializers.CharField(
        source="problem.topic",
        read_only=True
    )

    difficulty = serializers.CharField(
        source="problem.difficulty",
        read_only=True
    )

    room_code = serializers.CharField(
        source="room.room_code",
        read_only=True
    )

    class Meta:

        model = Submission

        fields = [
            "id",
            "username",
            "problem_title",
            "topic",
            "difficulty",
            "room_code",
            "language",
            "verdict",
            "submitted_at",
        ]


class SubmissionDetailSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    problem_title = serializers.CharField(
        source="problem.title",
        read_only=True
    )

    room_code = serializers.CharField(
        source="room.room_code",
        read_only=True
    )

    class Meta:

        model = Submission

        fields = [
            "id",
            "username",
            "room_code",
            "problem_title",
            "language",
            "code",
            "verdict",
            "failure_detail",
            "submitted_at",
        ]