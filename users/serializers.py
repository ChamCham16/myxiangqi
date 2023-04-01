from rest_framework import serializers
from .models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(username=data['username']).first()
        if user is None:
            raise serializers.ValidationError("User does not exist")
        if not user.check_password(data['password']):
            raise serializers.ValidationError("Incorrect password")
        return data

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords must match")
        return data
    
    def create(self, validated_data):
        instance = self.Meta.model(username=validated_data['username'], email=validated_data['email'])
        # hash password
        instance.set_password(validated_data['password1'])
        instance.save()
        return instance