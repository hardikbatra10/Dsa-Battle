from rest_framework import serializers

from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room

        fields = [
            'id',
            'creator',
            'participants',
            'topic',
            'difficulty',
            'room_code',
            'selected_problems',
            'number_of_questions',
            'time_limit_minutes',
            'created_at'
        ]

        read_only_fields = [
            'room_code',
            'creator',
            'selected_problems',
            'created_at'
        ]

class JoinRoomSerializer(serializers.Serializer):
    room_code = serializers.CharField(max_length = 8)
    