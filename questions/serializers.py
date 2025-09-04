from .models import Group, Subject, Category, SubCategory, Question
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.db.models import Q


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name','description', 'created_at']

class SubjectSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(slug_field='name', queryset=Group.objects.all())
    class Meta:
        model = Subject
        fields = ['id', 'name','description', 'group', 'created_at']
        


class CategorySerializer(serializers.ModelSerializer):
    subject = serializers.SlugRelatedField(slug_field='name', queryset=Subject.objects.all())
    class Meta:
        model = Category
        fields = ['id', 'name', 'subject','group' 'created_at']

class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category','subject', 'group' 'created_at']   


class QuestionSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(slug_field='name', queryset=Group.objects.all())
    subject = serializers.SlugRelatedField(slug_field='name', queryset=Subject.objects.all())
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all()
, allow_null=True, required=False)
    subcategory = serializers.SlugRelatedField(slug_field='name', queryset=SubCategory.objects.all(), allow_null=True, required=False)
    class Meta:
        model = Question
        fields = ['id', 'group', 'subject', 'category', 'subcategory', 'level', 'type', 'metadata', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        group = data.get('group')
        subject = data.get('subject')
        category = data.get('category')
        subcategory = data.get('subcategory')

        # Validate Subject belongs to Group
        if subject.group != group:
            raise ValidationError("The selected subject does not belong to the specified group.")

        # Validate Category belongs to Subject
        if category and category.subject != subject:
            raise ValidationError("The selected category does not belong to the specified subject.")

        # Validate SubCategory belongs to Category
        if subcategory and (not category or subcategory.category != category):
            raise ValidationError("The selected sub-category does not belong to the specified category.")

        return data
    def create(self, validated_data):
        return Question.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.group = validated_data.get('group', instance.group)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.category = validated_data.get('category', instance.category)
        instance.subcategory = validated_data.get('subcategory', instance.subcategory)
        instance.level = validated_data.get('level', instance.level)
        instance.type = validated_data.get('type', instance.type)
        instance.metadata = validated_data.get('metadata', instance.metadata)
        instance.save()
        return instance
    
class QuestionDetailSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(slug_field='name',read_only=True )
    subject = serializers.SlugRelatedField(slug_field='name',read_only=True)
    category = serializers.SlugRelatedField(slug_field='name' ,read_only=True)
    subcategory = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'group', 'subject', 'category', 'sub_category', 'level', 'type', 'metadata', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'group', 'subject', 'category', 'sub_category']
        

