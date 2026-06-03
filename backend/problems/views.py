from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProblemSerializer
from .models import Problem

class CreateProblemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProblemSerializer(data=request.data) 

        if serializer.is_valid():
            serializer.save(created_by = request.user)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ListProblemView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        queryset = Problem.objects.all().order_by('-created_at')
        serializer = ProblemSerializer(queryset, many = True)

        return Response(serializer.data)
