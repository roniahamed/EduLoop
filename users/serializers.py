from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AccessToken
from rest_framework.serializers import ModelSerializer



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(default=True)
    is_active = serializers.BooleanField(default=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'confirm_password', 'is_staff', 'is_active']
    
    def validate(self, data):

        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)

        if self.instance is None or 'password' in data or 'confirm_password' in data:


        
            if password is None or password != confirm_password:

                raise serializers.ValidationError("Die Passwörter stimmen nicht überein.")
        
            if len(password) < 8:

                raise serializers.ValidationError("Das Passwort muss mindestens 8 Zeichen lang sein.")
            data.pop('confirm_password', None)
        
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    

class AccessTokenSerializer(ModelSerializer):
    class Meta:
        model = AccessToken
        fields = ['key', 'description', 'is_active', 'created_at']