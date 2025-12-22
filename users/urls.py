from django.urls import path, include
from .views import ValidateAccessTokenView, GenerateAccessTokenView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('token-verify/', ValidateAccessTokenView.as_view(), name='validate-token'),
    # path('',include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('token-generate/', GenerateAccessTokenView.as_view(), name='generate-token'),
]