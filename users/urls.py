from django.urls import path, include
from .views import ValidateAccessTokenView, GenerateAccessTokenView, List_Of_AccessTokens, UpdateAccessTokenView, DeleteAccessTokenView, UserViewSet, CurrentUserView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('token-verify/', ValidateAccessTokenView.as_view(), name='validate-token'),
    # path('',include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('token-generate/', GenerateAccessTokenView.as_view(), name='generate-token'),
    path('token-list/', List_Of_AccessTokens.as_view(), name='list-tokens'),
    path('token-update/', UpdateAccessTokenView.as_view(), name='update-token'),
    path('token-delete/', DeleteAccessTokenView.as_view(), name='delete-token'),
    path('', include(router.urls)),
    path('current-user/', CurrentUserView.as_view(), name='current-user'),
    
]