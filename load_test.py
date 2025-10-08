import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

# Configuration
BASE_URL = 'http://localhost:8000/api'  # Adjust if different
NUM_USERS = 10000
ENDPOINTS = [
    '/groups/',
    '/subjects/',
    '/categories/',
    '/subcategories/',
    '/questions/',  # This might need POST for session, but for simplicity GET
]

results = []
results_lock = threading.Lock()

def make_request(endpoint):
    start_time = time.time()
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        end_time = time.time()
        response_time = end_time - start_time
        success = response.status_code == 200
        return {'endpoint': endpoint, 'success': success, 'response_time': response_time, 'status_code': response.status_code}
    except Exception as e:
        end_time = time.time()
        response_time = end_time - start_time
        return {'endpoint': endpoint, 'success': False, 'response_time': response_time, 'error': str(e)}

def load_test_user(user_id):
    user_results = []
    for endpoint in ENDPOINTS:
        result = make_request(endpoint)
        user_results.append(result)
    with results_lock:
        results.extend(user_results)

def main():
    print(f"Starting load test with {NUM_USERS} users...")

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=NUM_USERS) as executor:
        futures = [executor.submit(load_test_user, i) for i in range(NUM_USERS)]
        for future in as_completed(futures):
            future.result()  # Wait for completion

    end_time = time.time()
    total_time = end_time - start_time

    # Analyze results
    total_requests = len(results)
    successful_requests = sum(1 for r in results if r['success'])
    success_rate = (successful_requests / total_requests) * 100 if total_requests > 0 else 0

    response_times = [r['response_time'] for r in results]
    avg_response_time = statistics.mean(response_times) if response_times else 0
    min_response_time = min(response_times) if response_times else 0
    max_response_time = max(response_times) if response_times else 0
    median_response_time = statistics.median(response_times) if response_times else 0

    print("\nLoad Test Results:")
    print(f"Total Requests: {total_requests}")
    print(f"Successful Requests: {successful_requests}")
    print(f"Success Rate: {success_rate:.2f}%")
    print(f"Total Time: {total_time:.2f} seconds")
    print(f"Average Response Time: {avg_response_time:.2f} seconds")
    print(f"Min Response Time: {min_response_time:.2f} seconds")
    print(f"Max Response Time: {max_response_time:.2f} seconds")
    print(f"Median Response Time: {median_response_time:.2f} seconds")

    # Group by endpoint
    endpoint_stats = {}
    for r in results:
        ep = r['endpoint']
        if ep not in endpoint_stats:
            endpoint_stats[ep] = []
        endpoint_stats[ep].append(r)

    print("\nPer Endpoint Stats:")
    for ep, res in endpoint_stats.items():
        ep_success = sum(1 for r in res if r['success'])
        ep_rate = (ep_success / len(res)) * 100
        ep_avg_time = statistics.mean([r['response_time'] for r in res])
        print(f"{ep}: Success Rate {ep_rate:.2f}%, Avg Time {ep_avg_time:.2f}s")

if __name__ == '__main__':
    main()
