from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Note, XiangqiGame, OpeningBookPlayedByMasters
from .serializers import NoteSerializer, XiangqiGameSerializer, OpeningBookPlayedByMastersSerializer

# Create your views here.

@permission_classes([IsAuthenticated])
class GetNoteView(APIView):
    def get(self, request):
        user = request.user
        print('auth', user.is_authenticated)
        notes = user.note_set.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user = request.user
        print('auth', user.is_authenticated)
        note = Note.objects.get(id=request.data['id'])
        note.delete()
        return Response({'message': 'Note deleted successfully'}, status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
class CreateNoteView(APIView):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            print('user is authenticated')
            serializer = NoteSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
@permission_classes([IsAuthenticated])
class RandomXiangqiGameView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            print('user is authenticated')
            game = XiangqiGame.objects.order_by('?').first()
            game_serializer = XiangqiGameSerializer(game)
            return Response(game_serializer.data, status=status.HTTP_200_OK)
        
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
@permission_classes([IsAuthenticated])
class XiangqiGameView(APIView):
    # get game by id
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            print('user is authenticated')
            id = request.data['id']
            game = XiangqiGame.objects.get(id=id)
            game_serializer = XiangqiGameSerializer(game)
            return Response(game_serializer.data, status=status.HTTP_200_OK)
        
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

@permission_classes([IsAuthenticated])
class OpeningXiangqiGameView(APIView):
    # get all unique openings
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            print('user is authenticated')
            openings = XiangqiGame.objects.values_list('OPENING', flat=True).distinct()
            return Response(openings, status=status.HTTP_200_OK)
        
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request):
        # get first 40 games with a given opening
        user = request.user
        if user.is_authenticated:
            print('user is authenticated')
            opening = request.data['opening']
            page = request.data['page'] - 1
            games = XiangqiGame.objects.filter(OPENING=opening)[page*100:(page+1)*100]
            games_serializer = XiangqiGameSerializer(games, many=True)
            return Response(games_serializer.data, status=status.HTTP_200_OK)
        
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
@permission_classes([IsAuthenticated])
class OpeningBookPlayedByMastersView(APIView):
    # post a fen string to get a list of moves
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            print('user is authenticated')
            fen = request.data['fen']
            print('fen', fen) # for debugging
            moves = OpeningBookPlayedByMasters.objects.filter(fen=fen)
            moves_serializer = OpeningBookPlayedByMastersSerializer(moves, many=True)
            return Response(moves_serializer.data, status=status.HTTP_200_OK)
        
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)