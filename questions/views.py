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
from rest_framework.views import APIView
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Group View
class GroupViewSet(ListAPIView):
    queryset = Group.objects.all().order_by('-created_at')
    serializer_class = GroupSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

# Subject View
class SubjectViewSet(ListAPIView):
    # queryset = Subject.objects.select_related('group').all().order_by('-created_at')
    serializer_class = SubjectSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        group = get_object_or_404(Group, id=group_id)
        return Subject.objects.select_related('group').filter(group=group).order_by('-created_at')
    
# Category View
class CategoryViewSet(ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        subject_id = self.kwargs.get('subject_id')
        subject = get_object_or_404(Subject, id=subject_id)
        return Category.objects.select_related('subject__group').filter(subject=subject).order_by('-created_at')

#  SubCategory 
class SubCategoryViewSet(ListAPIView):
    serializer_class = SubCategorySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        return SubCategory.objects.select_related('category__subject__group').filter(category=category).order_by('-created_at')
    

#Question View 
class QuestionViewSet(APIView):
    
    def get_base_queryset(self, filters):
        group_id = filters.get('group_id')
        subject_id = filter.get('subject_id')
        category_ids = filter.get('category_ids', [])
        subcategory_ids = filter.get('subcategory_ids', [])

        queryset = Question.objects.select_related('group', 'subject','category','subcategory').filter(group_id = group_id, subject_id = subject_id)

        if category_ids:
            queryset = queryset.filter(subcategory__id__in = subcategory_ids)
        elif category_ids:
            queryset = queryset.filter(category__id__in = category_ids)
        
        return queryset
    
    # def post(self, request, *args, **kwargs):

        






    



