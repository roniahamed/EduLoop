from rest_framework import serializers
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']
    
    def validate(self, data):

        if not 'password' in data and not 'confirm_password' in data:

            raise serializers.ValidationError("Passwort und Bestätigung müssen angegeben werden.")
        
        if data['password'] != data.pop('confirm_password'):

            raise serializers.ValidationError("Die Passwörter stimmen nicht überein.")
        
        if 'password' not in data or len(data['password']) < 8:

            raise serializers.ValidationError("Das Passwort muss mindestens 8 Zeichen lang sein.")
        
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        return user
    
