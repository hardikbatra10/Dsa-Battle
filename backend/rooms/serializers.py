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


class MyRoomSerializer(serializers.ModelSerializer):

    creator_username = serializers.CharField(
        source='creator.username',
        read_only=True
    )

    is_creator = serializers.SerializerMethodField()

    participant_count = serializers.SerializerMethodField()

    def get_is_creator(self, obj):
        request = self.context.get('request')
        return bool(request) and obj.creator_id == request.user.id

    def get_participant_count(self, obj):
        return obj.participants.count()

    class Meta:
        model = Room

        fields = [
            'room_code',
            'creator_username',
            'is_creator',
            'participant_count',
            'topic',
            'difficulty',
            'number_of_questions',
            'time_limit_minutes',
            'status',
            'created_at',
            'started_at',
            'ended_at',
        ]
