import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Group, Subject, Category, SubCategory, Question


class QuestionsAPITestCase(APITestCase):
    def setUp(self):
        # Create superuser for admin tests
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.client.force_authenticate(user=self.admin_user)

        # Create regular user for non-admin tests
        self.regular_user = User.objects.create_user('user', 'user@test.com', 'password')

        # Create test data
        self.group = Group.objects.create(name='Test Group', description='Test Description')
        self.subject = Subject.objects.create(group=self.group, name='Test Subject', description='Test Description')
        self.category = Category.objects.create(group=self.group, subject=self.subject, name='Test Category')
        self.subcategory = SubCategory.objects.create(group=self.group, subject=self.subject, category=self.category, name='Test SubCategory')
        self.question = Question.objects.create(
            group=self.group,
            subject=self.subject,
            category=self.category,
            subcategory=self.subcategory,
            level='easy',
            type='mcq',
            metadata={'question': 'What is 2+2?', 'options': ['3', '4', '5'], 'answer': '4'}
        )

    def test_group_list(self):
        url = reverse('group-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_group_create(self):
        url = reverse('group-list')
        data = {'name': 'New Group', 'description': 'New Description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 2)

    def test_subject_list(self):
        url = reverse('subject-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subject_create(self):
        url = reverse('subject-list')
        data = {'group': self.group.name, 'name': 'New Subject', 'description': 'New Description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subject_detail_by_group(self):
        url = reverse('subject-view', kwargs={'group_id': self.group.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_category_list_all(self):
        url = reverse('category-list-all')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_create(self):
        url = reverse('category-list-all')
        data = {'group': self.group.name, 'subject': self.subject.name, 'name': 'New Category'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_category_detail_by_subject(self):
        url = reverse('category-detail-view', kwargs={'subject_id': self.subject.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subcategory_list_all(self):
        url = reverse('subcategory-list-all')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subcategory_create(self):
        url = reverse('subcategory-list-all')
        data = {
            'group': self.group.name,
            'subject': self.subject.name,
            'category': self.category.name,
            'name': 'New SubCategory'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subcategory_detail_by_category(self):
        url = reverse('subcategory-list-by-category', kwargs={'category_id': self.category.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_question_start_session(self):
        url = reverse('question-list')
        data = {
            'group_id': self.group.id,
            'subject_id': self.subject.id,
            'category_ids': [self.category.id],
            'levels': ['easy']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('session_id', response.data)
        self.assertIn('question', response.data)

    def test_question_get_next_without_session(self):
        url = reverse('question-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_question_reset_session(self):
        url = reverse('question-list')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bulk_question_upload(self):
        url = reverse('question_upload')
        data = [
            {
                'group': self.group.name,
                'subject': self.subject.name,
                'category': self.category.name,
                'subcategory': self.subcategory.name,
                'level': 'medium',
                'type': 'mcq',
                'metadata': {'question': 'Test?', 'options': ['A', 'B'], 'answer': 'A'}
            }
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_permissions_read_only_for_non_admin(self):
        # Switch to regular user
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('group-list')
        response = self.client.post(url, {'name': 'Test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_pagination(self):
        # Create more data for pagination
        for i in range(15):
            Group.objects.create(name=f'Group {i}')
        url = reverse('group-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertLessEqual(len(response.data['results']), 10)  # page_size=10
