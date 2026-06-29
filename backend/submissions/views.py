from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import SubmissionSerializer
from .models import Submission
from .services.judge0 import judge_problem


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