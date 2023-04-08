from rest_framework import serializers
from .models import Note, XiangqiGame, OpeningBookPlayedByMasters

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content']

class XiangqiGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = XiangqiGame
        fields = '__all__'

class OpeningBookPlayedByMastersSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningBookPlayedByMasters
        fields = '__all__'