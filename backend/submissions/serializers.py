from rest_framework import serializers
from .models import Submission

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
            'submitted_at'
        ]

        read_only_fields = [
            'user',
            'verdict',
            'submitted_at'
        ]

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
            "submitted_at",
        ]