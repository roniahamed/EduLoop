from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import AccessToken
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.models import Token



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
    
