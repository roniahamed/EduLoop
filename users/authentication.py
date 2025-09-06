from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from .models import AccessToken

class TokenAuthentication(BaseAuthentication):
    keyword = 'AccessKey'
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith(self.keyword + ' '):
            return None

        try:
            _, token_key = auth_header.split()
        except ValueError:
            return None

        try:
            token = AccessToken.objects.get(key=token_key, is_active=True)
        except AccessToken.DoesNotExist:
            raise AuthenticationFailed("Ungültiges oder inaktives Token.")

        return (AnonymousUser(), token)

    def authenticate_header(self, request):
        return self.keyword