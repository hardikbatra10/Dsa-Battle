from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import SubmissionSerializer, SubmissionHistorySerializer, SubmissionDetailSerializer
from .models import Submission
from .services.judge0 import judge_problem
from rooms.models import Room


class SubmitSolutionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = SubmissionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        print(serializer.validated_data)

        room = serializer.validated_data["room"]
        problem = serializer.validated_data["problem"]
        code = serializer.validated_data["code"]
        language = serializer.validated_data["language"]

        verdict = judge_problem(
            problem,
            code,
            language
        )

        submission = serializer.save(
            user=request.user,
            verdict=verdict
        )
        response_serializer = SubmissionSerializer(submission)


        # Check user belongs to room
        print("Checking participant")
        if not room.participants.filter(id=request.user.id).exists():
            return Response(
                {"error": "You are not a participant in this room"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check room is active
        print("Checking room status")
        if room.status != "active":
            return Response(
                {"error": "Room is not active"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check problem belongs to room
        print("Checking problem")   
        if not room.selected_problems.filter(id=problem.id).exists():
            return Response(
                {"error": "Problem does not belong to this room"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
class SubmissionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_code):

        try:
            room = Room.objects.get(room_code=room_code)

        except Room.DoesNotExist:
            return Response(
                {"error": "Room does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

         # User must belong to the room
        if not room.participants.filter(id=request.user.id).exists():
            return Response(
                {"error": "You are not a participant in this room"},
                status=status.HTTP_403_FORBIDDEN
            )

        submissions = Submission.objects.filter(room=room)

        # Optional query parameter:
        # /history/<room_code>/?mine=true
        mine = request.query_params.get("mine")

        if mine and mine.lower() == "true":
            submissions = submissions.filter(user=request.user)

        submissions = submissions.order_by("-submitted_at")

        serializer = SubmissionHistorySerializer(
            submissions,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
class SubmissionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, submission_id):

        # Check if submission exists
        try:
            submission = Submission.objects.get(id=submission_id)

        except Submission.DoesNotExist:
            return Response(
                {"error": "Submission does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if the requesting user belongs to the room
        if not submission.room.participants.filter(
            id=request.user.id
        ).exists():

            return Response(
                {"error": "You are not a participant in this room"},
                status=status.HTTP_403_FORBIDDEN
            )
        if submission.room.status == "active" and submission.user != request.user:
            return Response(
                {"error": "You cannot view other participants' submissions during an active contest."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = SubmissionDetailSerializer(submission)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )