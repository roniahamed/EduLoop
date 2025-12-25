from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import AccessToken
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import UserSerializer, AccessTokenSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from questions.views import StandardResultsSetPagination



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
        key = request.data.get('key', None)
        token = None
        if key:
            if AccessToken.objects.filter(key=key).exists():
                return Response({"error": "Ein Token mit diesem Schlüssel existiert bereits."}, status=status.HTTP_400_BAD_REQUEST)
            token = AccessToken.objects.create(key=key)
        else:
            token = AccessToken.objects.create()
        return Response({"key": token.key}, status=status.HTTP_201_CREATED)
    
class List_Of_AccessTokens(ListAPIView):
    permission_classes = [IsAdminUser]  
    serializer_class = AccessTokenSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        tokens = AccessToken.objects.all()
        return tokens
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

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"message": "Benutzerkonto erfolgreich gelöscht."}, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        user = request.user 
        serializer = UserSerializer(user, data = request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
