import requests
import json
import time

url = "http://localhost:8000/draft-document"

payload = {
  "details": {
    "borrower_name": "Akash Mehta",
    "interest_rate": "10",
    "lender_name": "Rohit Gupta",
    "loan_amount": "₹5,00,000",
    "tenure": "12"
  },
  "prompt": "Draft a Loan Agreement for ₹5,00,000 between Rohit Gupta (Lender) and Akash Mehta (Borrower), tenure 12 months, interest 10 percent, monthly repayment."
}

headers = {
  'accept': 'application/json',
  'Content-Type': 'application/json'
}

print("Sending request...")
start_time = time.time()
try:
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    print(f"Time taken: {time.time() - start_time:.2f}s")
except Exception as e:
    print(f"Error: {e}")
