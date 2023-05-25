from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import XiangqiBook, XiangqiSection, XiangqiScript, Book
from .serializers import CreateBookSerializer, BookSerializer, CreateXiangqiBookSerializer, XiangqiBookSerializer, CreateXiangqiSectionSerializer, XiangqiSectionSerializer, CreateXiangqiScriptSerializer, XiangqiScriptSerializer, UpdateXiangqiScriptSerializer

# Create your views here.

@permission_classes([IsAuthenticated])
class GetBookView(APIView):
    def get(self, request):
        user = request.user
        print('auth', user.is_authenticated)
        books = user.book_set.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user = request.user
        print('auth', user.is_authenticated)
        note = Book.objects.get(id=request.data['id'])
        note.delete()
        return Response({'message': 'Note deleted successfully'}, status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
class CreateBookView(APIView):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            print('user is authenticated')
            serializer = CreateBookSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

@permission_classes([IsAuthenticated])
class XiangqiBookView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            print('user is authenticated')
            books = user.xiangqibook_set.all()
            serializer = XiangqiBookSerializer(books, many=True)
            return Response(serializer.data)
        
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            print('user is authenticated')
            book = XiangqiBook.objects.get(id=request.data['book_id'])
            book.delete()
            return Response({'message': 'Book deleted successfully'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
@permission_classes([IsAuthenticated])
class CreateXiangqiBookView(APIView):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            print('user is authenticated')

            title = request.data['title']
            books = user.xiangqibook_set.all()
            for book in books:
                if book.title == title:
                    return Response({'error': 'Book already exists'}, status=status.HTTP_400_BAD_REQUEST)
                
            serializer = CreateXiangqiBookSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)

                # create default section
                book = XiangqiBook.objects.get(id=serializer.data['id'])
                data = {
                    'title': book.title,
                    'path': '/' + book.title,
                    'description': book.description,
                }
                section_serializer = CreateXiangqiSectionSerializer(data=data)
                if section_serializer.is_valid():
                    section_serializer.save(book=book)
                else:
                    return Response(section_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                book_serializer = XiangqiBookSerializer(book)

                return Response(book_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
@permission_classes([IsAuthenticated])
class XiangqiSectionView(APIView):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            print('user is authenticated')
            section = XiangqiSection.objects.get(id=request.data['section_id'])

            # check if section is default section
            if section.title == section.book.title:
                return Response({'error': 'Cannot delete default section'}, status=status.HTTP_400_BAD_REQUEST)

            section.delete()
            return Response({'message': 'Section deleted successfully'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
@permission_classes([IsAuthenticated])
class CreateXiangqiSectionView(APIView):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            print('user is authenticated')

            book_id = request.data['book_id']
            book = XiangqiBook.objects.get(id=book_id)

            section_path = request.data['path']
            sections = book.xiangqisection_set.all()
            for section in sections:
                if section.path == section_path:
                    return Response({'error': 'Section already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = CreateXiangqiSectionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(book=book)

                section_serializer = XiangqiSectionSerializer(book.xiangqisection_set.get(id=serializer.data['id']))
                return Response(section_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
@permission_classes([IsAuthenticated])
class XiangqiScriptView(APIView):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            print('user is authenticated')
            script = XiangqiScript.objects.get(id=request.data['script_id'])
            script.delete()
            return Response({'message': 'Script deleted successfully'}, status=status.HTTP_200_OK)
        
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
@permission_classes([IsAuthenticated])
class CreateXiangqiScriptView(APIView):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            print('user is authenticated')

            book_id = request.data['book_id']
            book = XiangqiBook.objects.get(id=book_id)

            section_id = request.data['section_id']
            section = book.xiangqisection_set.get(id=section_id)

            if 'content' not in request.data:
                request.data['content'] = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w moves|'

            serializer = CreateXiangqiScriptSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(section=section)

                script_serializer = XiangqiScriptSerializer(section.xiangqiscript_set.get(id=serializer.data['id']))
                return Response(script_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
@permission_classes([IsAuthenticated])
class UpdateXiangqiScriptView(APIView):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            print('user is authenticated')

            script_id = request.data['script_id']
            script = XiangqiScript.objects.get(id=script_id)

            serializer = UpdateXiangqiScriptSerializer(script, data=request.data)
            if serializer.is_valid():
                serializer.save()

                script_serializer = XiangqiScriptSerializer(script)
                return Response(script_serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

@permission_classes([IsAuthenticated])
class ReadBookView(APIView):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            print('user is authenticated')

            book_id = request.data['book_id']

            def generateBook(book_id: int):
                book = XiangqiBook.objects.get(id=book_id)
                sections = book.xiangqisection_set.all()
                section_serializers = XiangqiSectionSerializer(sections, many=True)

                root = []
                for section in sections:
                    node = {}
                    section_serializer = XiangqiSectionSerializer(section)
                    # node = section_serializer.data.copy()
                    node['section'] = section_serializer.data

                    scripts = section.xiangqiscript_set.all()
                    script_serializers = XiangqiScriptSerializer(scripts, many=True)
                    node['scripts'] = script_serializers.data

                    node['children'] = []
                    path = section_serializer.data['path'].split('/')[1:]

                    if len(path) == 0:
                        root.append(node)
                        continue

                    parent = root
                    for i in range(len(path)):
                        for child in parent:
                            if child['section']['title'] == path[i]:
                                parent = child['children']
                                break
                    parent.append(node)

                # in this case, there is only one root as the default section
                return root[0]

            data = {
                'bookAsTree': generateBook(book_id),
            }

            return Response(data)
        
        return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)