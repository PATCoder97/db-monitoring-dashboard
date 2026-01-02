import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("Testing Metrics API - Issue #4")
print("=" * 70)

# Test 1: Trigger manual metrics collection by checking databases
print("\n1. Triggering metrics collection (GET /api/databases)")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/api/databases")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} databases - metrics should be collected")
except Exception as e:
    print(f"Error: {e}")

# Wait a moment for scheduler to potentially run
print("\nWaiting 3 seconds for metrics to be stored...")
time.sleep(3)

# Test 2: Get metrics history for casaos database
print("\n2. Get Metrics History (GET /api/metrics/history/casaos)")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/api/metrics/history/casaos")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} metric records for 'casaos' database")
    if data:
        print("\nLatest metrics:")
        for metric in data[:5]:  # Show first 5
            print(f"  - {metric['timestamp']}: {metric['metric_type']} = {metric['value']}")
    else:
        print("No metrics found yet. Metrics are collected every 5 minutes by scheduler.")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Get metrics filtered by type
print("\n3. Get Size Metrics Only (GET /api/metrics/history/casaos?metric_type=size)")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/api/metrics/history/casaos?metric_type=size")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} size metric records")
    if data:
        for metric in data[:3]:
            print(f"  - {metric['timestamp']}: {metric['value']} bytes")
except Exception as e:
    print(f"Error: {e}")

# Test 4: Get metrics for postgres database
print("\n4. Get Metrics History (GET /api/metrics/history/postgres)")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/api/metrics/history/postgres")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} metric records for 'postgres' database")
except Exception as e:
    print(f"Error: {e}")

# Test 5: Get metrics with custom days parameter
print("\n5. Get 30 Days History (GET /api/metrics/history/casaos?days=30)")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/api/metrics/history/casaos?days=30")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} metric records in last 30 days")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 70)
print("Metrics API Testing Complete!")
print("=" * 70)
print("\nNOTE: Scheduler collects metrics every 5 minutes automatically.")
print("Check back in 5 minutes to see more historical data.")
print(f"\nSwagger UI: {BASE_URL}/docs")
