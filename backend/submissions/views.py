from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import SubmissionSerializer
from .models import Submission


class SubmitSolutionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = SubmissionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        room = serializer.validated_data["room"]
        problem = serializer.validated_data["problem"]
        code = serializer.validated_data["code"]
        language = serializer.validated_data["language"]

        # Check user belongs to room
        if not room.participants.filter(id=request.user.id).exists():
            return Response(
                {"error": "You are not a participant in this room"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check room is active
        if room.status != "active":
            return Response(
                {"error": "Room is not active"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check problem belongs to room
        if not room.selected_problems.filter(id=problem.id).exists():
            return Response(
                {"error": "Problem does not belong to this room"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create submission
        submission = Submission.objects.create(
            user=request.user,
            room=room,
            problem=problem,
            code=code,
            language=language,
            verdict="accepted"   # temporary until Judge0 integration
        )

        response_serializer = SubmissionSerializer(submission)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )