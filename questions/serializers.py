from .models import Group, Subject, Category, SubCategory, Question
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.db.models import Q

# Group Serializer

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name','description', 'created_at']
    
    def validate(self, attrs):
        name = attrs.get('name')
         # Validate unique group name
        if Group.objects.filter(name=name).exists():
            raise serializers.ValidationError(
                "Group with this name already exists."
            )
        return attrs

# Subject Serializer

class SubjectSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(slug_field='name', queryset=Group.objects.all())
    class Meta:
        model = Subject
        fields = ['id', 'name','description', 'group', 'created_at']

    def validate(self, attrs):
        group = attrs.get('group')
        name = attrs.get('name')
         # Validate Subject belongs to Group
        if Subject.objects.select_related('group').filter(group=group, name = name).exists():
            raise serializers.ValidationError(
                "Subject with this group already exists."
            )
        return attrs
        

# Category Serializer

class CategoryReadSerializer(serializers.ModelSerializer):
    subject = serializers.SlugRelatedField(slug_field='name', read_only=True)
    group = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'subject','group', 'created_at']
        read_only_fields = ['id', 'created_at', 'name', 'subject', 'group']


class CategoryWriteSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(slug_field='name', queryset=Group.objects.all())
    subject = serializers.CharField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'subject','group', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        subject_name = attrs.get('subject')
        group_instance = attrs.get('group')
        category_name = attrs.get('name')

        try:
            subject_instance = Subject.objects.select_related('group').get(name=subject_name, group=group_instance)
        except Subject.DoesNotExist:
            raise serializers.ValidationError({
                "subject": f"Subject '{subject_name}' not found in group '{group_instance.name}'."
            })
        

        
         # Validate Category belongs to Subject
        if Category.objects.select_related('subject','group', ).filter(name = category_name , subject=subject_instance, group=group_instance).exists():
            raise serializers.ValidationError(
                "Category with this subject and group already exists."
            )
        attrs['subject'] = subject_instance
        return attrs



# SubCategory Serializer

class SubCategoryReadSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    subject = serializers.SlugRelatedField(slug_field='name', read_only=True)
    group = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category','subject', 'group', 'created_at']
        read_only_fields = ['id', 'created_at', 'name', 'category','subject', 'group']

class SubCategoryWriteSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    subject = serializers.CharField()
    group = serializers.SlugRelatedField(slug_field='name', queryset=Group.objects.all())

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category','subject', 'group', 'created_at']   

    def validate(self, attrs):
        subject_name = attrs.get('subject')
        group_instance = attrs.get('group')
        category_name = attrs.get('category')
        sub_category_name = attrs.get('name')

        try:
            subject_instance = Subject.objects.select_related('group').get(name=subject_name, group=group_instance)
        except Subject.DoesNotExist:
            raise serializers.ValidationError({
                "subject": f"Subject '{subject_name}' not found in group '{group_instance.name}'."
            })

        try:
            category_instance = Category.objects.select_related('subject','group').get(name=category_name, subject = subject_instance, group=group_instance)
        except Category.DoesNotExist:
            raise serializers.ValidationError({
                  "category": f"Category '{category_name}' not found for the given group and subject."
            })
        
        
         # Validate Category belongs to Subject
        if SubCategory.objects.select_related('category', 'subject', 'group').filter(name = category_name,  category = category_instance, subject=subject_instance, group=group_instance).exists():
            raise serializers.ValidationError(
                "Category with this subject and group already exists."
            )
        attrs['category'] = category_instance
        attrs['subject'] = subject_instance
        return attrs


# Question Serializer
class QuestionWriteSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(slug_field='name', queryset=Group.objects.all())
    subject = serializers.CharField()
    category = serializers.CharField()
    subcategory = serializers.CharField(allow_null=True, required=False, allow_blank=True)
    class Meta:
        model = Question
        fields = ['group', 'subject', 'category', 'subcategory', 'level', 'type', 'metadata']
    
    def validate(self, attrs):
        group_instance = attrs.get('group')
        subject_name = attrs.get('subject')
        category_name = attrs.get('category')
        subcategory_name = attrs.get('subcategory')


        try:
            subject_instance = Subject.objects.get(group=group_instance, name=subject_name)
        except Subject.DoesNotExist:
            raise serializers.ValidationError({
                "subject": f"Subject '{subject_name}' does not exist in group '{group_instance.name}'."
            })
        
        try:
            category_instance = Category.objects.get(group=group_instance, subject=subject_instance, name=category_name)
        except Category.DoesNotExist:
            raise serializers.ValidationError({
                "category": f"Category '{category_name}' does not exist for the specified group and subject."
            })
        
        subcategory_instance = None

        if subcategory_name:
            try:
                subcategory_instance = SubCategory.objects.get( group=group_instance, subject=subject_instance, category=category_instance, name=subcategory_name)
            except SubCategory.DoesNotExist:
                raise serializers.ValidationError({
                    "subcategory": "SubCategory not found for the given group, subject, and category."
                })
        
        attrs['subject'] = subject_instance
        attrs['category'] = category_instance
        attrs['subcategory'] = subcategory_instance
        return attrs
    
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
    

# Question Detail Serializer
class QuestionDetailSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(slug_field='name',read_only=True )
    subject = serializers.SlugRelatedField(slug_field='name',read_only=True)
    category = serializers.SlugRelatedField(slug_field='name' ,read_only=True)
    subcategory = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'group', 'subject', 'category', 'sub_category', 'level', 'type', 'metadata', 'created_at', 'updated_at']
        read_only_fields = fields
        

