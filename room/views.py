from django.shortcuts import render
from .models import Room
from .serializers import RoomSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
    
@permission_classes([IsAuthenticated])
class CreateRoomView(APIView):
    def post(self, request):
        # check if room already exists
        if Room.objects.filter(slug=request.data['slug']).exists():
            return Response({'error': 'Room already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # get room and slug from request and create a new room
        room = Room.objects.create(name=request.data['name'], slug=request.data['slug'])
        room.save()

        return Response({'message': 'Room created successfully'}, status=status.HTTP_201_CREATED)
    
@permission_classes([IsAuthenticated])
class GetRoomView(APIView):
    def post(self, request):
        # get all room with slug starting with server name, server name can be HoChiMinh, HaNoi, etc...
        rooms = Room.objects.filter(slug__startswith=request.data['server_name'])
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)