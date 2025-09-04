from .views import GroupViewSet, SubjectViewSet, CategoryViewSet, SubCategoryViewSet, QuestionViewSet, BulkQuestionUploadView, SubjectDetailViewSet, CategoryDetailsViewSet
from django.urls import path , include

urlpatterns = [
    path('groups/', GroupViewSet.as_view(), name='group-list'),
    path('subject/<int:group_id>/', SubjectDetailViewSet.as_view(), name='subject-view'),
    path('subjects/', SubjectViewSet.as_view(), name='subject-list'),

    path('categories/', CategoryViewSet.as_view(), name='category-list'),
    path('category/<int:subject_id>/', CategoryDetailsViewSet.as_view(), name='category-detail-view'),
    path('subcategories/<int:category_id>/', SubCategoryViewSet.as_view(), name='subcategory-list'),
    path('questions/', QuestionViewSet.as_view(), name='question-list'),
    path('upload-questions/', BulkQuestionUploadView.as_view(), name='question_upload'),
    
]