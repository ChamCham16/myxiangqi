from rest_framework import serializers
from .models import Room
from users.models import User

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class RoomSerializer(serializers.ModelSerializer):
    white_player = UserNameSerializer()
    black_player = UserNameSerializer()

    class Meta:
        model = Room
        fields = '__all__'