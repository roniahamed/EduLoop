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

class SubjectViewSet(ListAPIView):
    # queryset = Subject.objects.select_related('group').all().order_by('-created_at')
    serializer_class = SubjectSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        group = get_object_or_404(Group, id=group_id)
        return Subject.objects.select_related('group').filter(group=group).order_by('-created_at')
    
class CategoryViewSet(ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        subject_id = self.kwargs.get('subject_id')
        subject = get_object_or_404(Subject, id=subject_id)
        return Category.objects.select_related('subject__group').filter(subject=subject).order_by('-created_at')
    
class SubCategoryViewSet(ListAPIView):
    serializer_class = SubCategorySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        return SubCategory.objects.select_related('category__subject__group').filter(category=category).order_by('-created_at')

    



