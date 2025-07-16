from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.services import create_user

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    def validate_username(self, value):
        if get_user_model().objects.filter(username=value).exists():
            raise serializers.ValidationError("User with this username already exists")
        return value
    
    def validate_email(self, value):
        if get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists")
        return value
    
    def validate(self, data):
        password = data.get('password')    
        password2 = data.get('password2')    
        
        if password != password2:
            raise serializers.ValidationError('passwords do not match')
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        return create_user(**validated_data)