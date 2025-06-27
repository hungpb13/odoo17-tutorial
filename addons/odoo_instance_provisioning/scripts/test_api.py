#!/usr/bin/env python3
"""
Demo script to test Odoo Instance Provisioning API
Usage: python3 test_api.py
"""

import requests
import json
import time
import sys

# Configuration
ODOO_URL = "http://localhost:8069"
API_BASE = f"{ODOO_URL}/api/provisioning"

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    
    try:
        response = requests.get(f"{API_BASE}/health", timeout=10)
        result = response.json()
        
        if result.get('success'):
            print("✓ Health check passed")
            return True
        else:
            print("✗ Health check failed:", result.get('error'))
            return False
    except Exception as e:
        print(f"✗ Health check error: {e}")
        return False

def test_get_plans():
    """Test get available plans"""
    print("\nTesting get plans...")
    
    try:
        response = requests.get(f"{API_BASE}/plans", timeout=10)
        result = response.json()
        
        if result.get('success'):
            plans = result.get('data', [])
            print(f"✓ Found {len(plans)} plans")
            for plan in plans:
                print(f"  - {plan['name']} (ID: {plan['id']})")
            return plans[0]['id'] if plans else None
        else:
            print("✗ Get plans failed:", result.get('error'))
            return None
    except Exception as e:
        print(f"✗ Get plans error: {e}")
        return None

def test_validate_subdomain(subdomain):
    """Test subdomain validation"""
    print(f"\nTesting subdomain validation for '{subdomain}'...")
    
    try:
        response = requests.post(
            f"{API_BASE}/validate_subdomain",
            json={"subdomain": subdomain},
            timeout=10
        )
        result = response.json()
        
        if result.get('success'):
            available = result.get('available')
            print(f"✓ Subdomain '{subdomain}' is {'available' if available else 'taken'}")
            return available
        else:
            print("✗ Subdomain validation failed:", result.get('error'))
            return False
    except Exception as e:
        print(f"✗ Subdomain validation error: {e}")
        return False

def test_create_instance(plan_id):
    """Test instance creation"""
    print("\nTesting instance creation...")
    
    # Generate unique subdomain
    import random
    subdomain = f"test{random.randint(1000, 9999)}"
    
    data = {
        "customer_email": "test@example.com",
        "customer_name": "Test User",
        "customer_phone": "0123456789",
        "company_name": "Test Company Ltd",
        "plan_id": plan_id,
        "subdomain": subdomain,
        "admin_email": "admin@example.com",
        "priority": "normal"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/create_instance",
            json=data,
            timeout=30
        )
        result = response.json()
        
        if result.get('success'):
            request_id = result.get('request_id')
            print(f"✓ Instance request created: {request_id}")
            print(f"  Subdomain: {subdomain}")
            print(f"  Estimated time: {result['data']['estimated_time']} minutes")
            return request_id, subdomain
        else:
            print("✗ Instance creation failed:", result.get('error'))
            return None, None
    except Exception as e:
        print(f"✗ Instance creation error: {e}")
        return None, None

def test_request_status(request_id):
    """Test request status check"""
    print(f"\nTesting request status for {request_id}...")
    
    try:
        response = requests.get(
            f"{API_BASE}/request_status/{request_id}",
            timeout=10
        )
        result = response.json()
        
        if result.get('success'):
            data = result.get('data')
            print(f"✓ Request status: {data['state']}")
            print(f"  Customer: {data['customer_name']}")
            print(f"  Company: {data['company_name']}")
            print(f"  Subdomain: {data['subdomain']}")
            if data.get('instance_url'):
                print(f"  URL: {data['instance_url']}")
            return data
        else:
            print("✗ Request status failed:", result.get('error'))
            return None
    except Exception as e:
        print(f"✗ Request status error: {e}")
        return None

def test_instance_info(subdomain):
    """Test instance info"""
    print(f"\nTesting instance info for {subdomain}...")
    
    try:
        response = requests.get(
            f"{API_BASE}/instance_info/{subdomain}",
            timeout=10
        )
        result = response.json()
        
        if result.get('success'):
            data = result.get('data')
            print(f"✓ Instance info retrieved")
            print(f"  Name: {data['name']}")
            print(f"  State: {data['state']}")
            print(f"  URL: {data['url']}")
            print(f"  CPU Usage: {data['cpu_usage']}%")
            print(f"  Memory Usage: {data['memory_usage']}%")
            return data
        else:
            print("✗ Instance info failed:", result.get('error'))
            return None
    except Exception as e:
        print(f"✗ Instance info error: {e}")
        return None

def test_instance_logs(subdomain):
    """Test instance logs"""
    print(f"\nTesting instance logs for {subdomain}...")
    
    try:
        response = requests.get(
            f"{API_BASE}/instance_logs/{subdomain}",
            params={"hours": 1, "limit": 10},
            timeout=10
        )
        result = response.json()
        
        if result.get('success'):
            data = result.get('data')
            logs = data.get('logs', [])
            print(f"✓ Retrieved {len(logs)} log entries")
            
            for log in logs[:3]:  # Show first 3 logs
                print(f"  [{log['level']}] {log['message']}")
            
            summary = data.get('summary', {})
            print(f"  Total logs: {summary.get('total', 0)}")
            
            return data
        else:
            print("✗ Instance logs failed:", result.get('error'))
            return None
    except Exception as e:
        print(f"✗ Instance logs error: {e}")
        return None

def test_manage_instance(subdomain):
    """Test instance management"""
    print(f"\nTesting instance management for {subdomain}...")
    
    # Test backup action
    try:
        response = requests.post(
            f"{API_BASE}/manage_instance/{subdomain}",
            json={"action": "backup"},
            timeout=60
        )
        result = response.json()
        
        if result.get('success'):
            print(f"✓ Backup action successful: {result['message']}")
            return True
        else:
            print("✗ Backup action failed:", result.get('error'))
            return False
    except Exception as e:
        print(f"✗ Backup action error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Odoo Instance Provisioning API Tests")
    print("=" * 50)
    
    # Test 1: Health check
    if not test_health_check():
        print("\n❌ Health check failed. Make sure Odoo server is running.")
        sys.exit(1)
    
    # Test 2: Get plans
    plan_id = test_get_plans()
    if not plan_id:
        print("\n❌ No plans available. Please create a service plan first.")
        sys.exit(1)
    
    # Test 3: Validate subdomain
    test_subdomain = "mytestcompany"
    test_validate_subdomain(test_subdomain)
    
    # Test 4: Create instance
    request_id, subdomain = test_create_instance(plan_id)
    if not request_id:
        print("\n❌ Instance creation failed.")
        sys.exit(1)
    
    # Test 5: Monitor request status
    print("\n⏳ Monitoring request status (waiting for provisioning)...")
    max_attempts = 12  # 2 minutes
    attempt = 0
    
    while attempt < max_attempts:
        time.sleep(10)  # Wait 10 seconds
        attempt += 1
        
        status_data = test_request_status(request_id)
        if not status_data:
            continue
        
        state = status_data.get('state')
        if state == 'completed':
            print("✓ Instance provisioning completed!")
            break
        elif state == 'failed':
            print("✗ Instance provisioning failed!")
            break
        else:
            print(f"  Still {state}... (attempt {attempt}/{max_attempts})")
    
    # Test 6: Instance info (if completed)
    if subdomain:
        time.sleep(5)  # Wait a bit more
        test_instance_info(subdomain)
        test_instance_logs(subdomain)
        test_manage_instance(subdomain)
    
    print("\n🎉 API tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
