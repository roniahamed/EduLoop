#!/usr/bin/env python3
"""
Live API Performance Test for EduLoop
Tests actual API endpoints with real data and measures performance
"""
import time
import json
import statistics
from datetime import datetime
import sys
import os

# Add the Django project to Python path
sys.path.append('/home/roni/Desktop/Eduloop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduloop.settings')

import django
django.setup()

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from questions.models import Group, Subject, Category, SubCategory, Question
from users.models import AccessToken

class LiveAPIPerformanceTest:
    def __init__(self):
        self.client = Client()
        self.results = []
        self.test_data = {}
        
    def setup_test_data(self):
        """Create test data for comprehensive API testing"""
        print("🔧 Setting up test data...")
        
        # Create test group
        self.test_data['group'] = Group.objects.create(
            name="Performance Test Group",
            description="Test group for API performance testing"
        )
        
        # Create test subject
        self.test_data['subject'] = Subject.objects.create(
            group=self.test_data['group'],
            name="Performance Test Subject",
            description="Test subject for API performance"
        )
        
        # Create test category
        self.test_data['category'] = Category.objects.create(
            group=self.test_data['group'],
            subject=self.test_data['subject'],
            name="Performance Test Category"
        )
        
        # Create test subcategory
        self.test_data['subcategory'] = SubCategory.objects.create(
            group=self.test_data['group'],
            subject=self.test_data['subject'],
            category=self.test_data['category'],
            name="Performance Test SubCategory"
        )
        
        # Create test access token
        self.test_data['token'] = AccessToken.objects.create(
            description="Performance Test Token",
            is_active=True
        )
        
        print(f"✅ Test data created successfully!")
        
    def test_endpoint(self, endpoint_name, url, method='GET', data=None, expected_status=200):
        """Test a single API endpoint and measure performance"""
        start_time = time.time()
        
        try:
            if method == 'GET':
                response = self.client.get(url)
            elif method == 'POST':
                response = self.client.post(url, data, content_type='application/json')
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            # Check response
            success = response.status_code == expected_status
            response_size = len(response.content) if hasattr(response, 'content') else 0
            
            result = {
                'endpoint': endpoint_name,
                'url': url,
                'method': method,
                'status_code': response.status_code,
                'expected_status': expected_status,
                'success': success,
                'response_time_ms': response_time,
                'response_size_bytes': response_size,
                'timestamp': datetime.now().isoformat()
            }
            
            # Add response data info if JSON
            try:
                if response.get('Content-Type', '').startswith('application/json'):
                    json_data = response.json()
                    if isinstance(json_data, dict):
                        result['response_count'] = json_data.get('count', 0)
                        result['has_results'] = 'results' in json_data
            except:
                pass
                
            self.results.append(result)
            return result
            
        except Exception as e:
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            
            error_result = {
                'endpoint': endpoint_name,
                'url': url,
                'method': method,
                'success': False,
                'response_time_ms': response_time,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            self.results.append(error_result)
            return error_result
    
    def run_comprehensive_test(self):
        """Run comprehensive API performance tests"""
        print("🚀 Starting comprehensive API performance test...")
        print("=" * 60)
        
        # Test all major endpoints
        endpoints = [
            # Groups
            ('Groups List', '/api/groups/', 'GET'),
            
            # Subjects  
            ('Subjects List', '/api/subjects/', 'GET'),
            ('Subject Details', f'/api/subject/{self.test_data["group"].id}/', 'GET'),
            
            # Categories
            ('Categories List', '/api/categories/', 'GET'),
            ('Category Details', f'/api/categories/{self.test_data["subject"].id}/', 'GET'),
            
            # SubCategories
            ('SubCategories List', '/api/subcategories/', 'GET'),
            ('SubCategory Details', f'/api/subcategories/{self.test_data["category"].id}/', 'GET'),
            
            # Questions
            ('Questions POST', '/api/questions/', 'POST'),
            
            # Users/Token validation
            ('Token Validation', '/api/token-verify/', 'POST'),
        ]
        
        # Run tests multiple times for statistical accuracy
        iterations = 3
        print(f"📊 Running {len(endpoints)} endpoints × {iterations} iterations = {len(endpoints) * iterations} total tests")
        print()
        
        for i in range(iterations):
            print(f"🔄 Iteration {i+1}/{iterations}")
            
            for endpoint_name, url, method in endpoints:
                if method == 'POST' and 'questions' in url:
                    # Test data for questions endpoint
                    test_data = json.dumps({
                        'group_id': self.test_data['group'].id,
                        'subject_id': self.test_data['subject'].id,
                        'category_ids': [self.test_data['category'].id],
                        'levels': ['easy', 'medium']
                    })
                    result = self.test_endpoint(endpoint_name, url, method, test_data)
                elif method == 'POST' and 'token-verify' in url:
                    # Test data for token validation
                    test_data = json.dumps({
                        'key': self.test_data['token'].key
                    })
                    result = self.test_endpoint(endpoint_name, url, method, test_data)
                else:
                    result = self.test_endpoint(endpoint_name, url, method)
                
                # Print result
                status_icon = "✅" if result['success'] else "❌"
                print(f"  {status_icon} {endpoint_name}: {result['response_time_ms']:.1f}ms "
                      f"(Status: {result.get('status_code', 'ERROR')})")
                
                # Small delay to avoid overwhelming the server
                time.sleep(0.1)
            
            print()
    
    def analyze_results(self):
        """Analyze test results and generate performance report"""
        if not self.results:
            print("❌ No test results to analyze")
            return
            
        print("📈 PERFORMANCE ANALYSIS RESULTS")
        print("=" * 60)
        
        # Overall statistics
        total_tests = len(self.results)
        successful_tests = len([r for r in self.results if r['success']])
        success_rate = (successful_tests / total_tests) * 100
        
        response_times = [r['response_time_ms'] for r in self.results if 'response_time_ms' in r]
        avg_response_time = statistics.mean(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        p95_response_time = statistics.quantiles(response_times, n=20)[18] if len(response_times) > 5 else 0
        
        print(f"📊 OVERALL PERFORMANCE SUMMARY")
        print(f"   Total Tests: {total_tests}")
        print(f"   Successful Tests: {successful_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Average Response Time: {avg_response_time:.1f}ms")
        print(f"   Min Response Time: {min_response_time:.1f}ms")
        print(f"   Max Response Time: {max_response_time:.1f}ms")
        print(f"   95th Percentile: {p95_response_time:.1f}ms")
        print()
        
        # Per-endpoint analysis
        print(f"🎯 PER-ENDPOINT PERFORMANCE")
        print("-" * 60)
        
        endpoints = {}
        for result in self.results:
            endpoint = result['endpoint']
            if endpoint not in endpoints:
                endpoints[endpoint] = []
            endpoints[endpoint].append(result)
        
        for endpoint, results in endpoints.items():
            successful = [r for r in results if r['success']]
            success_rate = (len(successful) / len(results)) * 100
            
            if successful:
                times = [r['response_time_ms'] for r in successful]
                avg_time = statistics.mean(times)
                min_time = min(times)
                max_time = max(times)
            else:
                avg_time = min_time = max_time = 0
                
            status_codes = list(set([r.get('status_code', 'ERROR') for r in results]))
            
            print(f"📍 {endpoint}")
            print(f"   Tests: {len(results)}, Success: {len(successful)} ({success_rate:.1f}%)")
            print(f"   Avg Time: {avg_time:.1f}ms, Range: {min_time:.1f}-{max_time:.1f}ms")
            print(f"   Status Codes: {status_codes}")
            print()
        
        # Performance grades
        print(f"🏆 PERFORMANCE GRADES")
        print("-" * 30)
        
        def get_grade(avg_time):
            if avg_time < 100: return "A+ (Excellent)"
            elif avg_time < 200: return "A (Very Good)"
            elif avg_time < 300: return "B (Good)"
            elif avg_time < 500: return "C (Fair)"
            else: return "D (Poor)"
        
        overall_grade = get_grade(avg_response_time)
        print(f"Overall Performance: {overall_grade}")
        print(f"Success Rate Grade: {'A+' if success_rate >= 99 else 'A' if success_rate >= 95 else 'B' if success_rate >= 90 else 'C'}")
        print()
        
        # Issues and recommendations
        print(f"⚠️  ISSUES DETECTED")
        print("-" * 30)
        
        issues = []
        if success_rate < 95:
            issues.append(f"Low success rate: {success_rate:.1f}% (should be >95%)")
        if avg_response_time > 300:
            issues.append(f"Slow response times: {avg_response_time:.1f}ms (should be <300ms)")
        if max_response_time > 1000:
            issues.append(f"Very slow requests detected: {max_response_time:.1f}ms")
            
        for endpoint, results in endpoints.items():
            failed_results = [r for r in results if not r['success']]
            if failed_results:
                issues.append(f"Endpoint '{endpoint}' has {len(failed_results)} failed requests")
        
        if issues:
            for i, issue in enumerate(issues, 1):
                print(f"{i}. {issue}")
        else:
            print("✅ No major issues detected!")
        
        print()
        
        return {
            'total_tests': total_tests,
            'success_rate': success_rate,
            'avg_response_time': avg_response_time,
            'performance_grade': overall_grade,
            'issues_count': len(issues)
        }
    
    def cleanup_test_data(self):
        """Clean up test data"""
        try:
            if 'token' in self.test_data:
                self.test_data['token'].delete()
            if 'subcategory' in self.test_data:
                self.test_data['subcategory'].delete()
            if 'category' in self.test_data:
                self.test_data['category'].delete()
            if 'subject' in self.test_data:
                self.test_data['subject'].delete()
            if 'group' in self.test_data:
                self.test_data['group'].delete()
            print("🧹 Test data cleaned up successfully")
        except Exception as e:
            print(f"⚠️ Error cleaning up test data: {e}")
    
    def save_results(self):
        """Save detailed results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'/home/roni/Desktop/Eduloop/live_api_performance_{timestamp}.json'
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"📄 Detailed results saved to: {filename}")

def main():
    print("🎯 EduLoop Live API Performance Test")
    print("=" * 60)
    print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tester = LiveAPIPerformanceTest()
    
    try:
        # Setup test data
        tester.setup_test_data()
        
        # Run comprehensive tests
        tester.run_comprehensive_test()
        
        # Analyze results
        summary = tester.analyze_results()
        
        # Save results
        tester.save_results()
        
        print("🎉 Live API performance test completed!")
        print(f"📊 Summary: {summary['success_rate']:.1f}% success rate, "
              f"{summary['avg_response_time']:.1f}ms avg response time")
        print(f"🏆 Performance Grade: {summary['performance_grade']}")
        
    finally:
        # Always cleanup
        tester.cleanup_test_data()

if __name__ == '__main__':
    main()