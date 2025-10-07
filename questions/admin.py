from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Group, Subject, Category, SubCategory, Question
from django.contrib.sessions.models import Session


@admin.register(Session)
class SessionAdmin(ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ('session_key', 'expire_date', '_session_data')
    search_fields = ('session_key',)
    ordering = ('-expire_date',)
    list_per_page = 15
    list_filter = ('expire_date',)
@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ('id', 'name','description' ,'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)
    list_per_page = 50


@admin.register(Subject)
class SubjectAdmin(ModelAdmin):
    list_display = ('id', 'name','description', 'group', 'created_at')
    search_fields = ('name', 'group__name')
    ordering = ('-created_at',)
    list_per_page = 50
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name', 'subject','group','created_at')
    search_fields = ('name', 'subject__name')
    ordering = ('-created_at',)
    list_per_page = 50

@admin.register(SubCategory)
class SubCategoryAdmin(ModelAdmin):
    list_display = ('id', 'name', 'category','subject','group', 'created_at')
    search_fields = ('name', 'category__name')
    ordering = ('-created_at',)
    list_per_page = 50

@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ('id', 'type', 'level', 'group', 'subject', 'category', 'subcategory', 'created_at', 'updated_at')
    search_fields = ('id','type', 'level', 'group__name', 'subject__name', 'category__name', 'subcategory__name')
    list_filter = ('type', 'level', 'group', 'subject', 'category', 'subcategory')
    ordering = ('-created_at',)
    list_per_page = 50
    readonly_fields = ('created_at', 'updated_at')
    list_max_show_all = 900

    raw_id_fields = ('group', 'subject', 'category', 'subcategory')

    fieldsets = (
        ('Basic Information', {
            'fields': ('group', 'subject', 'category', 'subcategory')
        }),
        ('Question Details', {
            'fields': ('type', 'level', 'metadata')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'group', 'subject', 'category', 'subcategory'
        )