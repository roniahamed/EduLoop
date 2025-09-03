from .models import Group, Subject, Category, SubCategory, Question
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import viewsets
from .serializers import GroupSerializer, SubjectSerializer, CategorySerializer, SubCategorySerializer, QuestionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class GroupViewSet(ListAPIView):
    queryset = Group.objects.all().order_by('-created_at')
    serializer_class = GroupSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.select_related('group').all().order_by('-created_at')
    serializer_class = SubjectSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        group_id = self.request.query_params.get('group_id')
        if group_id:
            queryset = queryset.filter(group__id=group_id)
        return queryset
    


