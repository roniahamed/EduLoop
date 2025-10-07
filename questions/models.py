from django.db import models
from django.db.models import F

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('name','group')
        ordering = ['group', 'name']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.name

class Category(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='categories')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ( 'name', 'subject','group')
        ordering = ['subject', 'name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subcategories')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='subcategories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'category','subject','group')
        ordering = [ 'name', 'category','subject', 'group']
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'
    def __str__(self):
        return self.name

class Question(models.Model):
    LEVEL_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("advance", "Advance")
    ]
    # TYPE_CHOICES = [
    #     ("mcq", "Multiple Choice"),
    #     ("fill_blank", "Fill in the Blank"),
    #     ("writing", "Writing"),
    #     ("math", "Math Problem"),
    #     ("true_false", "True/False")
    # ]

    # Main relational fields
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name='questions')
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE, related_name='questions')
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='questions')
    subcategory = models.ForeignKey("SubCategory", on_delete=models.CASCADE, null=True, blank=True, related_name='questions')
    
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    type = models.CharField(max_length=200)  # e.g., "mcq", "fill_blank", etc.

    # Question-specific data inside metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        indexes = [

            # Primary filtering indexes
            models.Index(fields=['group'],name='q_group_idx'),
            models.Index(fields=['subject'],name='q_subject_idx'),
            models.Index(fields=['category'], name='q_category_idx'),

            # Conditional subcategory index (only if frequently queried)
            models.Index(fields=['subcategory'], condition= models.Q(subcategory__isnull=False),name='q_subcat_partial_idx'),

            # common query patterns
            models.Index(fields=['level', 'type'], name='q_level_type_idx'),
            models.Index(fields=['created_at'], name='q_created_idx'),

            # Composite indexes for complex queries

            models.Index(fields=['group', 'subject', 'category'], name='question_gsc_idx'),
            models.Index(fields=['group', 'subject'], name='question_gs_idx'),
            models.Index(fields=['subject', 'category'], name='question_sc_idx'),
            

            models.Index(fields=['level'], name='q_level_idx'),
            models.Index(fields=['type'], name='q_type_idx'),
        ]

    def __str__(self):
        return f"Question {self.id} - {self.type} - {self.level}"
    

