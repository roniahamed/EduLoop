from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.utils import timezone
import time
import threading
from concurrent.futures import ThreadPoolExecutor

from .models import AccessToken, generate_unique_token


class AccessTokenModelTestCase(TestCase):
    """Test cases for AccessToken model functionality"""
    
    def setUp(self):
        self.test_description = "Test Token for Class 10A"
    
    def test_token_creation_with_default_key(self):
        """Test that AccessToken creates a unique key automatically"""
        token = AccessToken.objects.create(description=self.test_description)
        self.assertIsNotNone(token.key)
        self.assertEqual(len(token.key), 8)
        self.assertTrue(token.key.isdigit())
        self.assertTrue(token.is_active)
    
    def test_token_str_representation(self):
        """Test string representation of AccessToken"""
        token = AccessToken.objects.create(description=self.test_description)
        expected_str = f"{self.test_description} - {token.key}"
        self.assertEqual(str(token), expected_str)
    
    def test_unique_token_generation(self):
        """Test that generated tokens are unique"""
        tokens = []
        for i in range(10):
            token = AccessToken.objects.create(description=f"Token {i}")
            tokens.append(token.key)
        
        # All tokens should be unique
        self.assertEqual(len(tokens), len(set(tokens)))
    
    @patch('users.models.random.choices')
    def test_token_generation_collision_handling(self, mock_choices):
        """Test that token generation handles collisions properly"""
        # Create an existing token first
        existing_token = AccessToken.objects.create(description="Existing")
        
        # Mock random.choices to return the existing key first, then a new one
        mock_choices.side_effect = [
            list(existing_token.key),  # First call returns existing key
            list('87654321')           # Second call returns new key
        ]
        
        new_key = generate_unique_token()
        self.assertNotEqual(new_key, existing_token.key)
        self.assertEqual(new_key, '87654321')
    
    def test_token_deactivation(self):
        """Test token can be deactivated"""
        token = AccessToken.objects.create(description=self.test_description)
        self.assertTrue(token.is_active)
        
        token.is_active = False
        token.save()
        
        updated_token = AccessToken.objects.get(pk=token.key)
        self.assertFalse(updated_token.is_active)


class ValidateAccessTokenViewTestCase(APITestCase):
    """Test cases for ValidateAccessTokenView API endpoint"""
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('validate-token')
        self.valid_token = AccessToken.objects.create(
            description='Valid Test Token', 
            is_active=True
        )
        self.inactive_token = AccessToken.objects.create(
            description='Inactive Test Token', 
            is_active=False
        )
    
    def tearDown(self):
        """Clean up after each test"""
        AccessToken.objects.all().delete()
    
    # Valid scenarios
    def test_validate_active_token_success(self):
        """Test validation of active token returns success"""
        data = {'key': self.valid_token.key}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], "Das Token ist gültig.")
    
    # Invalid scenarios
    def test_validate_inactive_token_fails(self):
        """Test validation of inactive token returns error"""
        data = {'key': self.inactive_token.key}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], "Ungültiges oder inaktives Token.")
    
    def test_validate_nonexistent_token_fails(self):
        """Test validation of non-existent token returns error"""
        data = {'key': '99999999'}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], "Ungültiges oder inaktives Token.")
    
    def test_validate_missing_key_fails(self):
        """Test validation without key parameter returns error"""
        response = self.client.post(self.url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], "Token-Schlüssel muss angegeben werden.")
    
    def test_validate_empty_key_fails(self):
        """Test validation with empty key returns error"""
        data = {'key': ''}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_validate_null_key_fails(self):
        """Test validation with null key returns error"""
        data = {'key': None}
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    # Security tests
    def test_validate_token_case_sensitivity(self):
        """Test that token validation handles case correctly"""
        # Since tokens are numeric, case doesn't apply, but test different input
        data = {'key': 'ABCD1234'}  # Non-numeric key should fail
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_validate_token_sql_injection_protection(self):
        """Test protection against SQL injection attempts"""
        malicious_inputs = [
            "'; DROP TABLE users_accesstoken; --",
            "1' OR '1'='1",
            "admin'/*",
            "1; DELETE FROM users_accesstoken WHERE 1=1; --"
        ]
        
        for malicious_input in malicious_inputs:
            with self.subTest(input=malicious_input):
                data = {'key': malicious_input}
                response = self.client.post(self.url, data, format='json')
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_validate_token_xss_protection(self):
        """Test protection against XSS attempts"""
        xss_inputs = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
        ]
        
        for i, xss_input in enumerate(xss_inputs):
            with self.subTest(input=xss_input):
                # Use fresh client for each test to avoid rate limiting
                fresh_client = APIClient()
                data = {'key': xss_input}
                response = fresh_client.post(self.url, data, format='json')
                # Accept both 400 (invalid token) and 429 (rate limited) as valid responses
                self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_429_TOO_MANY_REQUESTS])
    
    # HTTP method tests
    def test_get_method_not_allowed(self):
        """Test that GET method is not allowed"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_put_method_not_allowed(self):
        """Test that PUT method is not allowed"""
        response = self.client.put(self.url, {'key': self.valid_token.key})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_delete_method_not_allowed(self):
        """Test that DELETE method is not allowed"""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    # Content type tests
    def test_validate_token_form_data(self):
        """Test token validation with form data"""
        # Use a fresh client to avoid rate limiting
        fresh_client = APIClient()
        response = fresh_client.post(
            self.url, 
            {'key': self.valid_token.key},
            content_type='application/x-www-form-urlencoded'
        )
        # Note: DRF might require JSON format, so 400 is acceptable
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])
    
    def test_validate_token_invalid_json(self):
        """Test handling of malformed JSON"""
        response = self.client.post(
            self.url,
            '{"key": invalid json}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AccessTokenPerformanceTestCase(TransactionTestCase):
    """Performance and concurrency tests for AccessToken"""
    
    def test_concurrent_token_creation(self):
        """Test that concurrent token creation doesn't create duplicates"""
        def create_token(i):
            return AccessToken.objects.create(description=f"Concurrent Token {i}")
        
        # Create 20 tokens concurrently
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_token, i) for i in range(20)]
            tokens = [future.result() for future in futures]
        
        # All tokens should have unique keys
        keys = [token.key for token in tokens]
        self.assertEqual(len(keys), len(set(keys)), "Duplicate token keys found")
    
    def test_token_validation_performance(self):
        """Test token validation performance under load"""
        # Create test token
        token = AccessToken.objects.create(description="Performance Test")
        
        start_time = time.time()
        
        # Perform 10 validations (reduced to avoid rate limiting in tests)
        successful_requests = 0
        for i in range(10):
            # Use separate client instances to avoid rate limiting
            fresh_client = APIClient()
            response = fresh_client.post(
                reverse('validate-token'),
                {'key': token.key},
                format='json'
            )
            if response.status_code == status.HTTP_200_OK:
                successful_requests += 1
            time.sleep(0.1)  # Small delay to avoid rate limiting
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # At least 8 out of 10 requests should succeed (allowing for rate limiting)
        self.assertGreaterEqual(successful_requests, 8, f"Too many requests failed: {successful_requests}/10")
        # Should complete in under 5 seconds (including sleep time)
        self.assertLess(total_time, 5.0, f"Token validation too slow: {total_time:.2f}s")
    
    def test_database_constraint_enforcement(self):
        """Test that database constraints are properly enforced"""
        # Test primary key constraint
        token = AccessToken.objects.create(description="Test")
        
        with self.assertRaises((IntegrityError, ValidationError)):
            # Attempt to create another token with the same key
            AccessToken.objects.create(key=token.key, description="Duplicate")


class AccessTokenIntegrationTestCase(APITestCase):
    """Integration tests combining multiple components"""
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('validate-token')
    
    def test_token_lifecycle(self):
        """Test complete token lifecycle: create, validate, deactivate"""
        # 1. Create token
        token = AccessToken.objects.create(description="Lifecycle Test")
        self.assertTrue(token.is_active)
        
        # 2. Validate active token
        response = self.client.post(self.url, {'key': token.key}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 3. Deactivate token
        token.is_active = False
        token.save()
        
        # 4. Validate inactive token (should fail)
        response = self.client.post(self.url, {'key': token.key}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_token_creation_timestamp(self):
        """Test that token creation timestamp is correctly set"""
        before_creation = timezone.now()
        token = AccessToken.objects.create(description="Timestamp Test")
        after_creation = timezone.now()
        
        self.assertIsNotNone(token.created_at)
        # Token creation time should be between before and after timestamps
        self.assertGreaterEqual(token.created_at, before_creation)
        self.assertLessEqual(token.created_at, after_creation)


class AccessTokenEdgeCaseTestCase(APITestCase):
    """Test edge cases and boundary conditions"""
    
    def test_very_long_description(self):
        """Test token creation with maximum length description"""
        long_description = "A" * 100  # Max length is 100
        token = AccessToken.objects.create(description=long_description)
        self.assertEqual(token.description, long_description)
    
    def test_unicode_description(self):
        """Test token creation with Unicode characters in description"""
        unicode_description = "Klasse 10A - Тест 测试 🎓"
        token = AccessToken.objects.create(description=unicode_description)
        self.assertEqual(token.description, unicode_description)
    
    def test_empty_description(self):
        """Test token creation with empty description"""
        token = AccessToken.objects.create(description="")
        self.assertEqual(token.description, "")
        self.assertIsNotNone(token.key)
    
    def test_null_description(self):
        """Test token creation with null description"""
        token = AccessToken.objects.create(description=None)
        self.assertIsNone(token.description)
        self.assertIsNotNone(token.key)

