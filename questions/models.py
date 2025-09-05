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
    TYPE_CHOICES = [
        ("mcq", "Multiple Choice"),
        ("fill_blank", "Fill in the Blank"),
        ("writing", "Writing"),
        ("math", "Math Problem"),
        ("true_false", "True/False")
    ]

    # Main relational fields
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name='questions')
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE, related_name='questions')
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='questions')
    subcategory = models.ForeignKey("SubCategory", on_delete=models.CASCADE, null=True, blank=True, related_name='questions')
    
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    # Question-specific data inside metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Question {self.id} - {self.type} - {self.level}"
    

