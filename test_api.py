"""
Quick test script to verify the API is working
Run this after starting main.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("LEGAL DOCUMENT DRAFTING LLM ENGINE - QUICK TEST")
print("=" * 70)

# Test 1: Health Check
print("\n✓ Test 1: Health Check")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        print("  ✅ Server is running!")
        data = response.json()
        print(f"  Status: {data['status']}")
        print(f"  Version: {data['version']}")
    else:
        print(f"  ❌ Unexpected status: {response.status_code}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 2: List Templates
print("\n✓ Test 2: List Available Templates")
try:
    response = requests.get(f"{BASE_URL}/templates", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"  ✅ Found {data['count']} document types:")
        for template in data['templates']:
            print(f"    - {template}")
    else:
        print(f"  ❌ Error: {response.status_code}")
except Exception as e:
    print(f"  ❌ Error: {e}")

# Test 3: API Documentation
print("\n✓ Test 3: API Documentation")
print(f"  📖 Swagger UI:     http://localhost:8000/docs")
print(f"  📖 ReDoc:          http://localhost:8000/redoc")

# Test 4: Draft Document (requires OPENAI_API_KEY)
print("\n✓ Test 4: Draft Document (requires valid OPENAI_API_KEY)")
print("  ⚠️  To test document generation:")
print("  1. Set OPENAI_API_KEY in .env file")
print("  2. Run the following curl command:")
print()
print("""  curl -X POST "http://localhost:8000/draft-document" \\
    -H "Content-Type: application/json" \\
    -d '{
      "prompt": "Draft a simple loan agreement for 100000 rupees between lender A and borrower B",
      "document_type": "loan_agreement",
      "details": {
        "lender_name": "Lender A",
        "borrower_name": "Borrower B",
        "loan_amount": "100000",
        "currency": "INR",
        "interest_rate": "10",
        "tenure": "12"
      }
    }'""")

print("\n" + "=" * 70)
print("✅ API is ready! Visit http://localhost:8000/docs to explore")
print("=" * 70)
