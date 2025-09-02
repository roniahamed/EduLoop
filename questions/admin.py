from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Group, Subject, Category, SubCategory, Question

@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)


@admin.register(Subject)
class SubjectAdmin(ModelAdmin):
    list_display = ('id', 'name', 'group', 'created_at')
    search_fields = ('name', 'group__name')
    ordering = ('-created_at',)

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name', 'subject', 'created_at')
    search_fields = ('name', 'subject__name')
    ordering = ('-created_at',)

@admin.register(SubCategory)
class SubCategoryAdmin(ModelAdmin):
    list_display = ('id', 'name', 'category', 'created_at')
    search_fields = ('name', 'category__name')
    ordering = ('-created_at',)

@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ('id', 'type', 'level', 'group', 'subject', 'category', 'sub_category', 'created_at', 'updated_at')
    search_fields = ('type', 'level', 'group__name', 'subject__name', 'category__name', 'sub_category__name')
    list_filter = ('type', 'level', 'group', 'subject', 'category', 'sub_category')
    ordering = ('-created_at',)