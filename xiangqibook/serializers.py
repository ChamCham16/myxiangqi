from rest_framework import serializers
from .models import Book, XiangqiBook, XiangqiSection, XiangqiScript

class CreateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'content']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class CreateXiangqiBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = XiangqiBook
        fields = ['id', 'title', 'description']

class XiangqiBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = XiangqiBook
        fields = '__all__'

class CreateXiangqiSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = XiangqiSection
        fields = ['id', 'title', 'path', 'description']

class XiangqiSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = XiangqiSection
        fields = '__all__'

class CreateXiangqiScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = XiangqiScript
        fields = ['id', 'title', 'content']

class UpdateXiangqiScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = XiangqiScript
        fields = ['id', 'content']

class XiangqiScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = XiangqiScript
        fields = '__all__'