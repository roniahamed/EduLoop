from django.db import models
from django.contrib.postgres.fields import JSONField

class Group(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Subject(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('group', 'name')
        ordering = ['group', 'name']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

class Category(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subject', 'name')
        ordering = ['subject', 'name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('category', 'name')
        ordering = ['category', 'name']
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'

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
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey("SubCategory", on_delete=models.CASCADE, null=True, blank=True)
    
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    # Question-specific data inside metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)