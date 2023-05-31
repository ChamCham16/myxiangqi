from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from XQlightPy.position import Position
from XQlightPy.search import Search
from XQlightPy.cchess import move2Iccs,Iccs2move
from .pikafish import get_best_move
    
# Pikafish
@permission_classes([IsAuthenticated])
class PikafishSearchView(APIView):
    def post(self, request):
        print('posting...')
        try:
            moves = request.data.get('moves', '')
            think_time = request.data.get('timeout', 0)
            print('moves', moves)
            print('think_time', think_time)
            best_move, ponder, info = get_best_move(moves, think_time)
            print('result', { 'mov': best_move, 'ponder': ponder, 'info': info })
            print('ohoho')
            return Response({ 'mov': best_move, 'ponder': ponder, 'info': info })
        except Exception as e:
            print(f"An error occurred while processing the request: {e}")

# XQlight (deprecated)
@permission_classes([IsAuthenticated])
class XQlightSearchView(APIView):
    def post(self, request):
        fen = request.data['fen']
        pos = Position()
        pos.fromFen(fen)
        search = Search(pos, 16)
        mov = search.searchMain(64, 60)
        return Response({ 'mov': move2Iccs(mov) })