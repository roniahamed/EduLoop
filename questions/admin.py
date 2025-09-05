from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Group, Subject, Category, SubCategory, Question

@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ('id', 'name','description' ,'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)
    list_per_page = 15


@admin.register(Subject)
class SubjectAdmin(ModelAdmin):
    list_display = ('id', 'name','description', 'group', 'created_at')
    search_fields = ('name', 'group__name')
    ordering = ('-created_at',)
    list_per_page = 15
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name', 'subject','group','created_at')
    search_fields = ('name', 'subject__name')
    ordering = ('-created_at',)
    list_per_page = 15

@admin.register(SubCategory)
class SubCategoryAdmin(ModelAdmin):
    list_display = ('id', 'name', 'category','subject','group', 'created_at')
    search_fields = ('name', 'category__name')
    ordering = ('-created_at',)
    list_per_page = 15

@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ('id', 'type', 'level', 'group', 'subject', 'category', 'subcategory', 'created_at', 'updated_at')
    search_fields = ('type', 'level', 'group__name', 'subject__name', 'category__name', 'subcategory__name')
    list_filter = ('type', 'level', 'group', 'subject', 'category', 'subcategory')
    ordering = ('-created_at',)
    list_per_page = 15