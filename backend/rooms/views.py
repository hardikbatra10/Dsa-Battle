from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import RoomSerializer, JoinRoomSerializer
from .models import Room
from problems.models import Problem
import uuid, random


class CreateRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        topic = serializer.validated_data['topic']
        difficulty = serializer.validated_data['difficulty']
        number_of_questions = serializer.validated_data['number_of_questions']
        time_limit_minutes = serializer.validated_data['time_limit_minutes']

        available_problems = Problem.objects.filter(
            topic = topic,
            difficulty = difficulty
        )

        if available_problems.count() < number_of_questions:
            return Response(
                {
                    "error": f"Only {available_problems.count()} problems available for the selected filters."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        selected_problems = random.sample(
            list(available_problems),
            number_of_questions
        )

        room_code = str(uuid.uuid4())[:8]

        room = Room.objects.create(
            creator=request.user,
            topic=topic,
            difficulty=difficulty,
            room_code=room_code,
            number_of_questions=number_of_questions,
            time_limit_minutes=time_limit_minutes
        )
        room.participants.add(request.user)

        room.selected_problems.set(selected_problems)

        response_serializer = RoomSerializer(room)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
class JoinRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = JoinRoomSerializer(data = request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        room_code = serializer.validated_data["room_code"]

        try:
            room = Room.objects.get(room_code=room_code)

        except Room.DoesNotExist:
            return Response(
                {"error": "Room does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        if room.participants.filter(id=request.user.id).exists():
            return Response(
                {"error": "You have already joined this room"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        room.participants.add(request.user)


        response_serializer = RoomSerializer(room)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )

class RoomDetailView(APIView):
    def get(self, request, room_code):
        try:
            room = Room.objects.get(room_code=room_code)

        except Room.DoesNotExist:
            return Response(
                {"error": "Room does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = RoomSerializer(room)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )