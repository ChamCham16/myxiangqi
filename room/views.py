from django.shortcuts import render
from .models import XiangqiRoom
from .serializers import XiangqiRoomSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
    
@permission_classes([IsAuthenticated])
class CreateXiangqiRoomView(APIView):
    def post(self, request):
        # check if room already exists
        if XiangqiRoom.objects.filter(slug=request.data['slug']).exists():
            return Response({'error': 'Room already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # get room and slug from request and create a new room
        room = XiangqiRoom.objects.create(name=request.data['name'], slug=request.data['slug'])
        room.save()

        # serialize the room and return it
        serializer = XiangqiRoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@permission_classes([IsAuthenticated])
class GetXiangqiRoomView(APIView):
    def get(self, request):
        rooms = XiangqiRoom.objects.all()
        serializer = XiangqiRoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)