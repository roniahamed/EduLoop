from .views import GroupViewSet, SubjectViewSet, CategoryViewSet, SubCategoryViewSet, QuestionViewSet, BulkQuestionUploadView, SubjectDetailViewSet, CategoryDetailsViewSet, SubCategoryDetailsViewSet, Home_Dashboard
from django.urls import path , include

urlpatterns = [
    path('groups/', GroupViewSet.as_view(), name='group-list'),

    # subject views
    path('subject/<int:group_id>/', SubjectDetailViewSet.as_view(), name='subject-view'),
    path('subjects/', SubjectViewSet.as_view(), name='subject-list'),

        # category views
    path('categories/', CategoryViewSet.as_view(), name='category-list-all'),

    path('categories/<int:subject_id>/', CategoryDetailsViewSet.as_view(), name='category-detail-view'),

    # subcategory views
    path('subcategories/', SubCategoryViewSet.as_view(), name='subcategory-list-all'),
    path('subcategories/<int:category_id>/', SubCategoryDetailsViewSet.as_view(), name='subcategory-list-by-category'),

    # question views
    path('questions/', QuestionViewSet.as_view(), name='question-list'),
    path('upload-questions/', BulkQuestionUploadView.as_view(), name='question_upload'),

    # Dashboard
    path('dashboard/', Home_Dashboard.as_view(), name='dashboard-view'),
    
]