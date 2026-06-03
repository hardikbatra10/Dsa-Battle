from rest_framework import serializers

from .models import Problem

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem

        fields = [
            'id',
            'title',
            'description',
            'difficulty',
            'topic',
            'example_input',
            'example_output',
            'constraints',
            'created_by',
            'created_at',
        ]

        read_only_fields = [
            'created_by',
            'created_at'
        ]