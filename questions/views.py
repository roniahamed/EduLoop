from .models import Group, Subject, Category, SubCategory, Question
from .serializers import GroupSerializer, SubjectSerializer, CategoryWriteSerializer,CategoryReadSerializer, SubCategoryReadSerializer, SubCategoryWriteSerializer, QuestionDetailSerializer, QuestionListSerializer, CategoryListSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from .permissions import IsAdminOrReadOnly
from django.contrib.sessions.backends.db import SessionStore
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.core.cache import cache 
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db import transaction
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from users.authentication import TokenAuthentication, AuthenticatedStudent
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# Group View

@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 minutes
class GroupViewSet(ListCreateAPIView):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data, many = isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_queryset(self):
        cache_key = 'groups_list'
        queryset = cache.get(cache_key)
        
        if not queryset:
            queryset = Group.objects.all().order_by('name')
            cache.set(cache_key, list(queryset), 60 * 15)  # Cache for 15 minutes
            
        return queryset
    
    def perform_create(self, serializer):
        super().perform_create(serializer)
        cache.delete('groups_list')
    
# Subject View

class SubjectViewSet(ListCreateAPIView):
    queryset = Subject.objects.select_related('group').all().order_by('group__name','name')
    serializer_class = SubjectSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'group__name']
    ordering_fields = ['name', 'group__name']
    filterset_fields = ['group__id']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data, many = isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SubjectDetailViewSet(ListAPIView):
    serializer_class = SubjectSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        group = get_object_or_404(Group, id=group_id)
        return Subject.objects.select_related('group').prefetch_related('categories').filter(group=group).order_by('group__name', 'name')
    
# Category View

class CategoryViewSet(ListCreateAPIView):
    queryset = Category.objects.select_related('subject','group').prefetch_related('subcategories').all().order_by('name')
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'subject__name', 'group__name']
    ordering_fields = ['name', 'subject__name', 'group__name']
    filterset_fields = ['subject__id', 'group__id']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryWriteSerializer
        return CategoryReadSerializer

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data = request.data, many = is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CategoryDetailsViewSet(ListAPIView):
    serializer_class = CategoryReadSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        subject_id = self.kwargs.get('subject_id')
        subject = get_object_or_404(Subject, id=subject_id)
        return Category.objects.select_related('subject','group').prefetch_related('subcategories').filter(subject=subject).order_by('name')
    
class CategoryListViewSet(ListAPIView):
    serializer_class = CategoryListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        return Category.objects.select_related('subject','group').all().order_by('name')

#  SubCategory 

class SubCategoryViewSet(ListCreateAPIView):
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category__name', 'subject__name', 'group__name']
    ordering_fields = ['name', 'category__name', 'subject__name', 'group__name']
    filterset_fields = ['category__id', 'subject__id', 'group__id']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubCategoryWriteSerializer
        return SubCategoryReadSerializer
    def get_queryset(self):
        return SubCategory.objects.select_related('category','subject','group').all().order_by('name')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data, many = isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SubCategoryDetailsViewSet(ListAPIView):
    serializer_class = SubCategoryReadSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        return SubCategory.objects.select_related('category','subject','group').filter(category=category).order_by('name')

#Question View 

QUIZ_BATCH_SIZE = 50
class QuestionViewSet(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def get_base_queryset(self, filters):
        group_id = filters.get('group_id')
        subject_id = filters.get('subject_id')
        category_ids = filters.get('category_ids', [])
        subcategory_ids = filters.get('subcategory_ids', [])
        levels = filters.get('levels', [])

        queryset = Question.objects.select_related('group', 'subject','category','subcategory').filter(group_id = group_id, subject_id = subject_id)

        if levels:
            queryset = queryset.filter(level__in=levels)

        if subcategory_ids:
            queryset = queryset.filter(subcategory__id__in = subcategory_ids)
        elif category_ids:
            queryset = queryset.filter(category__id__in = category_ids)
        
        return queryset
    
    def post(self, request, *args, **kwargs):

        filters = {
            'group_id' : request.data.get('group_id'),
            'subject_id' : request.data.get('subject_id'),
            'category_ids' : request.data.get('category_ids', []),
            'subcategory_ids' : request.data.get('subcategory_ids', []),
            'levels': request.data.get('levels', [])
        }

        if not filters['group_id'] or not filters['subject_id']:
            return Response({"errors": "Selecting a group and at least one subject is mandatory."}, status=status.HTTP_400_BAD_REQUEST)
        
        s = SessionStore()
        s.create()

        s['question_filter'] = filters 
        s['seen_question_ids'] = []
        s['question_batch'] = []
        s.save()

        queryset = self.get_base_queryset(filters)
        new_batch_ids = list(queryset.order_by('?').values_list('id', flat=True)[:QUIZ_BATCH_SIZE])

        first_question_data = None

        if new_batch_ids:
            question_id = new_batch_ids.pop(0)
            s['seen_question_ids'] = [question_id]
            s['question_batch'] = new_batch_ids
            s.save()
            try:
                question_obj = queryset.get(id=question_id)
                serializer = QuestionDetailSerializer(question_obj)
                first_question_data = serializer.data
            except Question.DoesNotExist:
                first_question_data = None

        return Response({
            'session_id': s.session_key,
            'question': first_question_data
        }, status=status.HTTP_200_OK)
    

    
    def get(self, request, *args, **kwargs):
        filters = request.session.get('question_filter')

        if not filters:
            return Response({'errors': "There is no active question this section." }, status=status.HTTP_400_BAD_REQUEST)

        question_batch = request.session.get('question_batch', [])

        if not question_batch:

            seen_ids = request.session.get('seen_question_ids', [])

            queryset = self.get_base_queryset(filters)

            new_batch_ids = list(queryset.exclude(id__in = seen_ids).order_by('?').values_list('id', flat=True)[:QUIZ_BATCH_SIZE])

            if not new_batch_ids:
                return Response({'errors': "No more new questions are available for your selection."}, status=status.HTTP_404_NOT_FOUND)
                
            question_batch = new_batch_ids

            request.session['question_batch'] = question_batch

        question_id = question_batch.pop(0)
        request.session['question_batch'] = question_batch
        seen_ids = request.session.get('seen_question_ids', [])
        seen_ids.append(question_id)
        request.session['seen_question_ids'] = seen_ids

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
    permission_classes = [IsAdminOrReadOnly]
    def post(self, request, *args, **kwargs):

        if not isinstance(request.data, list):
            return Response({"error": "Expected a list of items."}, status=status.HTTP_400_BAD_REQUEST)
        if not request.data:
            return Response({"message": "No data provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        group_names = {item.get('group') for item in request.data if item.get('group')}
        subject_lookups = {(item.get('group'), item.get('subject')) for item in request.data}
        category_lookups = {(item.get('group'), item.get('subject'), item.get('category')) for item in request.data}
        subcategory_lookups = {(item.get('group'), item.get('subject'), item.get('category'), item.get('subcategory')) for item in request.data if item.get('subcategory')}


        groups = Group.objects.filter(name__in=group_names)
        subjects = Subject.objects.select_related('group').filter(group__name__in={l[0] for l in subject_lookups}, name__in={l[1] for l in subject_lookups})
        categories = Category.objects.select_related('group', 'subject').filter(group__name__in={l[0] for l in category_lookups}, subject__name__in={l[1] for l in category_lookups}, name__in={l[2] for l in category_lookups})
        subcategories = SubCategory.objects.select_related('group', 'subject', 'category').filter(group__name__in={l[0] for l in subcategory_lookups}, subject__name__in={l[1] for l in subcategory_lookups}, category__name__in={l[2] for l in subcategory_lookups}, name__in={l[3] for l in subcategory_lookups})

        groups_map = {g.name: g for g in groups}
        subjects_map = {(s.group.name, s.name): s for s in subjects}
        categories_map = {(c.group.name, c.subject.name, c.name): c for c in categories}
        subcategories_map = {(sc.group.name, sc.subject.name, sc.category.name, sc.name): sc for sc in subcategories}
        
        questions_to_create = []
        errors = []

        for index, item_data in enumerate(request.data):
            group_name = item_data.get('group')
            subject_name = item_data.get('subject')
            category_name = item_data.get('category')
            subcategory_name = item_data.get('subcategory')

            group = groups_map.get(group_name)
            if not group:
                errors.append({"row": index + 2, "errors": {"group": f"Group '{group_name}' not found."}})
                continue
            subject = subjects_map.get((group_name, subject_name))
            if not subject:
                errors.append({"row": index + 2, "errors": {"subject": f"Subject '{subject_name}' not found in group '{group_name}'."}})
                continue
            category = categories_map.get((group_name, subject_name, category_name))
            if not category:
                errors.append({"row": index + 2, "errors": {"category": f"Category '{category_name}' not found."}})
                continue

            subcategory = None
            if subcategory_name:
                subcategory = subcategories_map.get((group_name, subject_name, category_name, subcategory_name))
                if not subcategory:
                    errors.append({"row": index + 2, "errors": {"subcategory": f"SubCategory '{subcategory_name}' not found."}})
                    continue
            
            questions_to_create.append(Question(
                group=group, subject=subject, category=category, subcategory=subcategory,
                level=item_data.get('level'), type=item_data.get('type'), metadata=item_data.get('metadata', {})
            ))
        

        if errors:
            return Response({
                "message": "Upload failed. Please fix the errors.",
                "Failed find: ": len(errors),
                "failed_items": errors
            }, status=status.HTTP_400_BAD_REQUEST)


        created_questions = []

        if questions_to_create:
            try:
                created_questions = Question.objects.bulk_create(questions_to_create)
            except Exception as e:
                return Response({"error": f"An error occurred during database operation: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        response_data = {
            "message": f"Successfully uploaded {len(created_questions)} out of {len(request.data)} questions."
        }

        return Response({
            "message": f"Successfully uploaded {len(created_questions)} questions."
        }, status=status.HTTP_201_CREATED)



# Dashboard 

from users.models import AccessToken
from django.contrib.auth.models import User

class Home_Dashboard(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        total_groups = Group.objects.count()
        total_subjects = Subject.objects.count()
        total_categories = Category.objects.count()
        total_subcategories = SubCategory.objects.count()
        total_questions = Question.objects.count()
        total_token = AccessToken.objects.count()
        total_users = User.objects.count()

        data = {
            "total_groups": total_groups,
            "total_subjects": total_subjects,
            "total_categories": total_categories,
            "total_subcategories": total_subcategories,
            "total_questions": total_questions,
            "total_access_tokens": total_token,
            "total_users": total_users,
        }

        return Response(data, status=status.HTTP_200_OK)



from rest_framework.generics import ListAPIView

class Question_Dashboard(ListAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination
    serializer_class = QuestionListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['created_at', 'group__name', 'subject__name', 'category__name', 'subcategory__name']
    search_fields = ['group__name', 'subject__name', 'category__name', 'subcategory__name']
    filterset_fields = ['level', 'type', 'group__id', 'subject__id', 'category__id', 'subcategory__id']

    def get_queryset(self):
        questions = Question.objects.select_related('group', 'subject', 'category', 'subcategory').all().order_by('-created_at')
        return questions
    
