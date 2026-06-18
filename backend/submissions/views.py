from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import SubmissionSerializer
from .models import Submission
from django.db import models
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
        
        room_code = serializer.validated_data["room_code"]

        try:
            room = Room.objects.get(room_code=room_code)

        except Room.DoesNotExist:
            return Response(
                {"error": "Room does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )


