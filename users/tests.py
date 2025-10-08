from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import AccessToken


class UsersAPITestCase(APITestCase):
    def setUp(self):
        self.valid_token = AccessToken.objects.create(description='Test Token', is_active=True)
        self.invalid_token = AccessToken.objects.create(description='Inactive Token', is_active=False)

    def test_validate_access_token_valid(self):
        url = reverse('validate-token')
        data = {'key': self.valid_token.key}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_validate_access_token_invalid(self):
        url = reverse('validate-token')
        data = {'key': self.invalid_token.key}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_validate_access_token_missing_key(self):
        url = reverse('validate-token')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_validate_access_token_nonexistent(self):
        url = reverse('validate-token')
        data = {'key': 'nonexistent'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

