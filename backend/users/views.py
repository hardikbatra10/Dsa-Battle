from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, UserSerializer 
from submissions.models import Submission
from rooms.models import Room


class RegisterUserView(APIView):
    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class MeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user 

        serializer = UserSerializer(user)

        return Response(serializer.data)
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        rooms_created = Room.objects.filter(
            creator=user
        ).count()

        submissions = Submission.objects.filter(
            user=user
        )

        problems_solved = submissions.filter(
            verdict="accepted"
        ).values("problem").distinct().count()

        total_submissions = submissions.count()

        return Response(
            {
                "username": user.username,
                "email": user.email,
                "rooms_created": rooms_created,
                "problems_solved": problems_solved,
                "total_submissions": total_submissions
            },
            status=status.HTTP_200_OK
        )