from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import AccessToken
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet


class ValidateAccessTokenView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request, *args, **kwargs):
        token_key = request.data.get('key')
        if not token_key:
            return Response({"error": "Token-Schlüssel muss angegeben werden."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = AccessToken.objects.get(key=token_key, is_active=True)
            return Response({"message": "Das Token ist gültig."}, status=status.HTTP_200_OK)
        except AccessToken.DoesNotExist:
            return Response({"error": "Ungültiges oder inaktives Token."}, status=status.HTTP_400_BAD_REQUEST)
        
class GenerateAccessTokenView(APIView):
    permission_classes = [IsAdminUser]  

    def post(self, request, *args, **kwargs):
        token = AccessToken.objects.create()
        return Response({"key": token.key}, status=status.HTTP_201_CREATED)

class List_Of_AccessTokens(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request, *args, **kwargs):
        tokens = AccessToken.objects.all()
        token_list = [{"key": token.key, "description": token.description, "is_active": token.is_active, "created_at": token.created_at} for token in tokens]
        return Response(token_list, status=status.HTTP_200_OK)
    
class UpdateAccessTokenView(APIView):
    permission_classes = [IsAdminUser]  

    def put(self, request, *args, **kwargs):
        token_key = request.data.get('key')
        is_active = request.data.get('is_active')
        description = request.data.get('description', '')
        new_key = request.data.get('new_key', None)

        if not token_key:
            return Response({"error": "Token-Schlüssel muss angegeben werden."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = AccessToken.objects.get(key=token_key)
            if is_active is not None:
                token.is_active = is_active
            if new_key:
                token.key = new_key
            token.description = description
            token.save()
            return Response({"message": "Token erfolgreich aktualisiert."}, status=status.HTTP_200_OK)
        except AccessToken.DoesNotExist:
            return Response({"error": "Token nicht gefunden."}, status=status.HTTP_404_NOT_FOUND)
        
class DeleteAccessTokenView(APIView):
    permission_classes = [IsAdminUser]  

    def delete(self, request, *args, **kwargs):
        token_key = request.data.get('key')

        if not token_key:
            return Response({"error": "Token-Schlüssel muss angegeben werden."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = AccessToken.objects.get(key=token_key)
            token.delete()
            return Response({"message": "Token erfolgreich gelöscht."}, status=status.HTTP_200_OK)
        except AccessToken.DoesNotExist:
            return Response({"error": "Token nicht gefunden."}, status=status.HTTP_404_NOT_FOUND)

# User  
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
