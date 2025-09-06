from django.urls import path, include
from .views import ValidateAccessTokenView

urlpatterns = [
    path('token-verify/', ValidateAccessTokenView.as_view(), name='validate-token'),
    path('',include('rest_framework.urls')),
]