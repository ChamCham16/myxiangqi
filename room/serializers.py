from rest_framework import serializers
from .models import XiangqiRoom

class XiangqiRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = XiangqiRoom
        fields = ['id', 'name', 'white', 'black']