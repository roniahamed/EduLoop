from .models import Group, Subject, Category, SubCategory, Question
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import viewsets
from .serializers import GroupSerializer, SubjectSerializer, CategorySerializer, SubCategorySerializer, QuestionSerializer, QuestionDetailSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly 
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
import random
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Group View
class GroupViewSet(ListCreateAPIView):
    queryset = Group.objects.all().order_by('-created_at')
    serializer_class = GroupSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data, many = isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
# Subject View

class SubjectViewSet(ListCreateAPIView):
    queryset = Subject.objects.select_related('group').all().order_by('-created_at')
    serializer_class = SubjectSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data, many = isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SubjectDetailViewSet(ListCreateAPIView):
    # queryset = Subject.objects.select_related('group').all().order_by('-created_at')
    serializer_class = SubjectSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        group = get_object_or_404(Group, id=group_id)
        return Subject.objects.select_related('group').filter(group=group).order_by('-created_at')
    
# Category View

class CategoryViewSet(ListCreateAPIView):
    queryset = Category.objects.select_related('subject__group').all().order_by('-created_at')
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data, many = isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CategoryDetailsViewSet(ListCreateAPIView):
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        subject_id = self.kwargs.get('subject_id')
        subject = get_object_or_404(Subject, id=subject_id)
        return Category.objects.select_related('subject__group').filter(subject=subject).order_by('-created_at')

#  SubCategory 
class SubCategoryViewSet(ListCreateAPIView):
    serializer_class = SubCategorySerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        return SubCategory.objects.select_related('category__subject__group').filter(category=category).order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data, many = isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

#Question View 

QUIZ_BATCH_SIZE = 50
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
    
    def post(self, request, *args, **kwargs):

        filters = {
            'group_id' : request.data.get('group_id'),
            'subject_id' : request.data.get('subject_id'),
            'category_ids' : request.data.get('category_ids', []),
            'subcategory_ids' : request.data.get('subcategory_ids', [])
        }

        if not filters['group_id'] or not filters['subject_id']:
            return Response({"errors": "Selecting a group and at least one subject is mandatory."}, status=status.HTTP_400_BAD_REQUEST)
        
        request.session['question_filter'] = filters 
        request.session['seen_question_ids'] = []
        request.session['question_batch'] = []

        return self.get(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        filters = request.session.get('question_filter')

        if not filters:
            return Response({'errors': "There is no active question session." })

        question_batch = request.session.get('question_batch', [])

        if not question_batch:

            seem_ids = request.session.get('seen_question_ids', [])

            queryset = self.get_base_queryset(filters)

            new_batch_ids = list(queryset.exclude(id__in = seem_ids).order_by('?').values_list('id', flat=True)[:QUIZ_BATCH_SIZE])

            if not new_batch_ids:
                return Response({'errors': "No more new questions are available for your selection."}, status=status.HTTP_404_NOT_FOUND)
                
            question_batch = new_batch_ids

            request.session['question_batch'] = question_batch
        question_id = question_batch.pop(0)
        request.session['question_batch'] = question_batch
        seem_ids = request.session['seem_question_ids', []]
        seem_ids.append(question_id)
        request.session['seem_question_ids'] = seem_ids

        try:
            question = self.get_base_queryset(filters).get(id=question_id)
        except Question.DoesNotExist:
            return self.get(request, *args, **kwargs)
        
        serializer = QuestionDetailSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        keys_to_delete = ['question_filter', 'seen_question_ids', 'question_batch']
        for key in keys_to_delete:
            if key in request.session:
                del request.session[key]
        return Response({'message': "Question session has been reset."}, status=status.HTTP_200_OK)

class BulkQuestionUploadView(APIView):
    def post(self, request, *args, **kwargs):
        
        serializer = QuestionSerializer(data = request.data, many = True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data

        questions_to_create = []

        for question_item in validated_data:
            questions_to_create.append(Question(**question_item))

        try: 
            created_questions = Question.objects.bulk_create(questions_to_create, batch_size=500)
            return Response({"message": f"{len(created_questions)} questions have been uploaded successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



        
        


