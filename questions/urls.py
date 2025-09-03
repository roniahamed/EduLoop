from .views import GroupViewSet, SubjectViewSet, CategoryViewSet
from django.urls import path , include

urlpatterns = [
    path('groups/', GroupViewSet.as_view(), name='group-list'),
    path('subjects/<int:group_id>/', SubjectViewSet.as_view(), name='subject-list'),
    path('categories/<int:subject_id>/', CategoryViewSet.as_view(), name='category-list'),

    
]