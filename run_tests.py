#!/usr/bin/env python3
"""
Test runner script for EduLoop project
Provides comprehensive testing with coverage reporting
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

def setup_django():
    """Setup Django for testing"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduloop.settings')
    django.setup()

def run_tests():
    """Run all tests with coverage"""
    setup_django()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    # Run tests for specific apps
    test_apps = ['users', 'questions', 'academy', 'teacher', 'ai']
    
    failures = test_runner.run_tests(test_apps)
    
    if failures:
        sys.exit(1)
    else:
        print("All tests passed! ✅")

def run_user_tests_only():
    """Run only users app tests"""
    setup_django()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2)
    
    failures = test_runner.run_tests(['users'])
    
    if failures:
        print(f"❌ {failures} test(s) failed")
        sys.exit(1)
    else:
        print("✅ All users tests passed!")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'users':
        run_user_tests_only()
    else:
        run_tests()