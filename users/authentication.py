from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from .models import AccessToken

class AuthenticatedStudent:
    """
    A dummy user class for authenticated status.
    It does not have a database table.
    """
    def __init__(self, token=None):
        self.token = token

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
    @property
    def pk(self):
        return self.token.key if self.token else None
        

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
        
        student = AuthenticatedStudent(token=token)

        return (student, token)

    def authenticate_header(self, request):
        return self.keyword