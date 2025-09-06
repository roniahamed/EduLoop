from django.urls import path
from .views import ValidateAccessTokenView

urlpatterns = [
    path('token-verify', ValidateAccessTokenView.as_view(), name='validate-token'),
]