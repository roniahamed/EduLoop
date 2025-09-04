from .views import GroupViewSet, SubjectViewSet, CategoryViewSet, SubCategoryViewSet, QuestionViewSet, BulkQuestionUploadView
from django.urls import path , include

urlpatterns = [
    path('groups/', GroupViewSet.as_view(), name='group-list'),
    path('subjects/<int:group_id>/', SubjectViewSet.as_view(), name='subject-list'),
    path('categories/<int:subject_id>/', CategoryViewSet.as_view(), name='category-list'),
    path('subcategories/<int:category_id>/', SubCategoryViewSet.as_view(), name='subcategory-list'),
    path('questions/', QuestionViewSet.as_view(), name='question-list'),
    path('upload-questions/', BulkQuestionUploadView.as_view(), name='question_upload'),
    
]