from rest_framework import serializers

from .models import Room

class RoomSerializer(serializers.ModelSerializer):

    creator_username = serializers.CharField(
        source='creator.username',
        read_only=True
    )

    participant_usernames = serializers.SerializerMethodField()

    def get_participant_usernames(self, obj):
        return list(obj.participants.values_list('username', flat=True))

    class Meta:
        model = Room

        fields = [
            'id',
            'creator',
            'creator_username',
            'participants',
            'participant_usernames',
            'topic',
            'difficulty',
            'room_code',
            'selected_problems',
            'number_of_questions',
            'time_limit_minutes',
            'created_at',
            'status',
            'started_at',
            'ended_at'
        ]

        read_only_fields = [
            'room_code',
            'creator',
            'selected_problems',
            'created_at',
            'status',
            'started_at',
            'ended_at'
        ]

class JoinRoomSerializer(serializers.Serializer):
    room_code = serializers.CharField(max_length = 8)
    