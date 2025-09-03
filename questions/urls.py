from .views import GroupViewSet
from django.urls import path , include
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('groups/', GroupViewSet.as_view(), name='group-list'),
]