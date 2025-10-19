"""
Script untuk test health endpoint
"""

import requests
import time
import sys

def test_health_endpoints(base_url="http://localhost:5000"):
    """Test semua health endpoints"""
    
    endpoints = [
        "/health",
        "/health/live", 
        "/health/ready"
    ]
    
    print(f"🔍 Testing health endpoints on {base_url}")
    print("=" * 50)
    
    for endpoint in endpoints:
        try:
            url = base_url + endpoint
            print(f"\n📡 Testing: {endpoint}")
            
            response = requests.get(url, timeout=10)
            
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.json()}")
            
            if response.status_code == 200:
                print("   ✅ SUCCESS")
            else:
                print("   ❌ FAILED")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ CONNECTION ERROR - App not running on {base_url}")
        except requests.exceptions.Timeout:
            print(f"   ❌ TIMEOUT - App too slow to respond")
        except Exception as e:
            print(f"   ❌ ERROR: {e}")

def test_with_flask_app():
    """Test dengan Flask app langsung"""
    print("\n🧪 Testing with Flask app directly...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            endpoints = ["/health", "/health/live", "/health/ready"]
            
            for endpoint in endpoints:
                print(f"\n📡 Testing: {endpoint}")
                
                response = client.get(endpoint)
                print(f"   Status Code: {response.status_code}")
                print(f"   Response: {response.get_json()}")
                
                if response.status_code in [200, 503]:  # 503 is OK for /health/ready
                    print("   ✅ SUCCESS")
                else:
                    print("   ❌ FAILED")
                    
    except Exception as e:
        print(f"❌ Error testing Flask app: {e}")

if __name__ == "__main__":
    print("🚀 Health Check Tester")
    print("=" * 50)
    
    # Test dengan Flask app langsung
    test_with_flask_app()
    
    print("\n" + "=" * 50)
    print("💡 Tips untuk Railway deployment:")
    print("   1. Gunakan /health/live untuk liveness probe")
    print("   2. Gunakan /health/ready untuk readiness probe")
    print("   3. Gunakan /health untuk general health check")
    print("   4. Pastikan app sudah running sebelum healthcheck")
