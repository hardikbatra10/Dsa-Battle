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