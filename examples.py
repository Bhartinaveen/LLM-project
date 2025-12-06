"""
Example usage and testing script for the Legal Document Drafting Engine
Demonstrates various document generation scenarios
"""

import json
import requests
from typing import Dict, Any

# API Base URL
BASE_URL = "http://localhost:8000"


class LegalDocumentClient:
    """Client for interacting with the Legal Document Drafting API"""

    def __init__(self, base_url: str = BASE_URL):
        """Initialize the client"""
        self.base_url = base_url

    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()

    def list_templates(self) -> Dict[str, Any]:
        """List available document templates"""
        response = requests.get(f"{self.base_url}/templates")
        return response.json()

    def draft_document(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Draft a legal document"""
        response = requests.post(f"{self.base_url}/draft-document", json=request_data)
        return response.json()

    def download_document(self, filename: str, save_path: str) -> bool:
        """Download a generated document"""
        try:
            response = requests.get(f"{self.base_url}/download/{filename}")
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                return True
            return False
        except Exception as e:
            print(f"Error downloading document: {e}")
            return False


def example_loan_agreement():
    """Example: Generate a Loan Agreement"""
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Loan Agreement")
    print("=" * 60)

    client = LegalDocumentClient()

    request_data = {
        "prompt": "Draft a Loan Agreement for ₹5,00,000 between Rohit Gupta (Lender) and Akash Mehta (Borrower), tenure 12 months, interest 10 percent, monthly repayment.",
        "document_type": "loan_agreement",
        "details": {
            "lender_name": "Rohit Gupta",
            "borrower_name": "Akash Mehta",
            "loan_amount": "₹5,00,000",
            "currency": "INR",
            "interest_rate": "10",
            "tenure": "12",
            "repayment_frequency": "Monthly",
            "date": "2024-01-01",
            "jurisdiction": "India",
            "additional_details": "Monthly repayment on the 1st of each month. Prepayment allowed without penalty.",
        },
    }

    try:
        print("\nRequest Payload:")
        print(json.dumps(request_data, indent=2))

        response = client.draft_document(request_data)

        print("\nResponse:")
        print(json.dumps(response, indent=2))

        if response.get("success"):
            print(f"\n✓ Document generated successfully!")
            print(f"  File: {response['file_path']}")
            print(f"  Download URL: {response['download_url']}")

            # Download the document
            filename = response["file_path"].split("/")[-1]
            if client.download_document(filename, f"./outputs/{filename}"):
                print(f"  ✓ Downloaded to: ./outputs/{filename}")

    except Exception as e:
        print(f"✗ Error: {e}")


def example_service_agreement():
    """Example: Generate a Service Agreement"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Service Agreement")
    print("=" * 60)

    client = LegalDocumentClient()

    request_data = {
        "prompt": "Create a Service Agreement between Tech Solutions Ltd (provider) and ABC Corporation (client) for software development and maintenance services.",
        "document_type": "service_agreement",
        "details": {
            "service_provider": "Tech Solutions Ltd",
            "service_client": "ABC Corporation",
            "service_description": "Custom software development, testing, and 24/7 maintenance support",
            "service_fees": "₹25,00,000",
            "currency": "INR",
            "payment_schedule": "50% upfront, 25% at mid-project, 25% on completion",
            "term_duration": "24",
            "jurisdiction": "India",
            "additional_details": "6-month warranty period included. SLA: 99.5% uptime.",
        },
    }

    try:
        print("\nRequest Payload:")
        print(json.dumps(request_data, indent=2))

        response = client.draft_document(request_data)

        print("\nResponse:")
        print(json.dumps(response, indent=2))

        if response.get("success"):
            print(f"\n✓ Document generated successfully!")
            print(f"  File: {response['file_path']}")

    except Exception as e:
        print(f"✗ Error: {e}")


def example_nda():
    """Example: Generate an NDA"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Non-Disclosure Agreement (NDA)")
    print("=" * 60)

    client = LegalDocumentClient()

    request_data = {
        "prompt": "Draft an NDA between TechCorp Industries and InnovateLabs for evaluating a potential strategic partnership and technology integration.",
        "document_type": "nda",
        "details": {
            "disclosing_party": "TechCorp Industries",
            "receiving_party": "InnovateLabs",
            "purpose": "Strategic partnership evaluation and technology integration assessment",
            "info_type": "Business plans, proprietary technology, financial projections, trade secrets",
            "term_duration": "24",
            "jurisdiction": "India",
            "additional_details": "Mutual NDA. Exceptions: publicly available information, information received from third parties.",
        },
    }

    try:
        print("\nRequest Payload:")
        print(json.dumps(request_data, indent=2))

        response = client.draft_document(request_data)

        print("\nResponse:")
        print(json.dumps(response, indent=2))

        if response.get("success"):
            print(f"\n✓ Document generated successfully!")
            print(f"  File: {response['file_path']}")

    except Exception as e:
        print(f"✗ Error: {e}")


def example_employment_contract():
    """Example: Generate an Employment Contract"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Employment Contract")
    print("=" * 60)

    client = LegalDocumentClient()

    request_data = {
        "prompt": "Draft an Employment Contract for John Doe as Senior Software Developer at TechCorp with annual salary of ₹15,00,000.",
        "document_type": "employment_contract",
        "details": {
            "employee_name": "John Doe",
            "employer_name": "TechCorp Solutions",
            "position": "Senior Software Developer",
            "department": "Engineering",
            "salary": "₹15,00,000",
            "currency": "INR",
            "employment_type": "Full-time",
            "start_date": "2024-02-01",
            "jurisdiction": "India",
            "additional_details": "Includes health insurance, 30 days paid leave, performance bonus. 3 months notice period.",
        },
    }

    try:
        print("\nRequest Payload:")
        print(json.dumps(request_data, indent=2))

        response = client.draft_document(request_data)

        print("\nResponse:")
        print(json.dumps(response, indent=2))

        if response.get("success"):
            print(f"\n✓ Document generated successfully!")
            print(f"  File: {response['file_path']}")

    except Exception as e:
        print(f"✗ Error: {e}")


def example_rental_agreement():
    """Example: Generate a Rental Agreement"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Rental Agreement")
    print("=" * 60)

    client = LegalDocumentClient()

    request_data = {
        "prompt": "Create a Rental Agreement for a 2-bedroom apartment at 123 Main Street, Mumbai between Priya Sharma (Landlord) and Rajesh Kumar (Tenant).",
        "document_type": "rental_agreement",
        "details": {
            "landlord_name": "Priya Sharma",
            "tenant_name": "Rajesh Kumar",
            "property_address": "123 Main Street, Bandra, Mumbai - 400050",
            "property_type": "Residential 2-BHK Apartment",
            "rent_amount": "₹30,000",
            "currency": "INR",
            "lease_duration": "12",
            "deposit_amount": "₹60,000",
            "start_date": "2024-02-15",
            "jurisdiction": "Maharashtra, India",
            "additional_details": "Deposit refundable. Utilities separate. No pets allowed. Annual rent increase 5%.",
        },
    }

    try:
        print("\nRequest Payload:")
        print(json.dumps(request_data, indent=2))

        response = client.draft_document(request_data)

        print("\nResponse:")
        print(json.dumps(response, indent=2))

        if response.get("success"):
            print(f"\n✓ Document generated successfully!")
            print(f"  File: {response['file_path']}")

    except Exception as e:
        print(f"✗ Error: {e}")


def example_partnership_deed():
    """Example: Generate a Partnership Deed"""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Partnership Deed")
    print("=" * 60)

    client = LegalDocumentClient()

    request_data = {
        "prompt": "Create a Partnership Deed between Raj Kumar and Priya Singh for starting a management consulting business.",
        "document_type": "partnership_deed",
        "details": {
            "partner_names": "Raj Kumar, Priya Singh",
            "business_name": "Strategic Solutions Consulting LLP",
            "business_description": "Management consulting, strategic planning, and business advisory services",
            "place_of_business": "New Delhi, India",
            "capital_contributions": "₹50,00,000 each (Total: ₹1,00,00,000)",
            "profit_sharing_ratio": "50:50 (Equal)",
            "management_rights": "Equal partnership rights and responsibilities",
            "jurisdiction": "India",
            "additional_details": "Annual audit mandatory. Dispute resolution through arbitration. Notice period 6 months for withdrawal.",
        },
    }

    try:
        print("\nRequest Payload:")
        print(json.dumps(request_data, indent=2))

        response = client.draft_document(request_data)

        print("\nResponse:")
        print(json.dumps(response, indent=2))

        if response.get("success"):
            print(f"\n✓ Document generated successfully!")
            print(f"  File: {response['file_path']}")

    except Exception as e:
        print(f"✗ Error: {e}")


def example_auto_detect():
    """Example: Auto-detect document type from prompt"""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Auto-Detect Document Type")
    print("=" * 60)

    client = LegalDocumentClient()

    # No document_type specified - system will auto-detect
    request_data = {
        "prompt": "I need to draft an affidavit sworn by Ramesh Singh, resident of Mumbai, stating facts about a property dispute where he claims rightful ownership.",
        "details": {
            "affiant_name": "Ramesh Singh",
            "affiant_address": "Mumbai, Maharashtra, India",
            "purpose": "Property ownership dispute declaration",
            "statement_content": "I declare that I am the rightful owner of the property located at Plot No. 123, XYZ Street, Mumbai.",
        },
    }

    try:
        print("\nRequest Payload:")
        print(json.dumps(request_data, indent=2))

        response = client.draft_document(request_data)

        print("\nResponse:")
        print(json.dumps(response, indent=2))

        if response.get("success"):
            print(f"\n✓ Document generated successfully!")
            print(f"  Detected Type: {response['document_type']}")
            print(f"  File: {response['file_path']}")

    except Exception as e:
        print(f"✗ Error: {e}")


def show_available_templates():
    """Show available templates"""
    print("\n" + "=" * 60)
    print("AVAILABLE DOCUMENT TEMPLATES")
    print("=" * 60)

    client = LegalDocumentClient()

    try:
        response = client.list_templates()
        if response.get("success"):
            print(f"\nAvailable Templates ({response['count']}):")
            for i, template in enumerate(response["templates"], 1):
                print(f"  {i}. {template.replace('_', ' ').title()}")
    except Exception as e:
        print(f"✗ Error: {e}")


def check_api_health():
    """Check API health status"""
    print("\n" + "=" * 60)
    print("API HEALTH CHECK")
    print("=" * 60)

    client = LegalDocumentClient()

    try:
        response = client.health_check()
        print(f"\nAPI Status: {response['status']}")
        print(f"Version: {response['version']}")
        print(f"Timestamp: {response['timestamp']}")
        print("\n✓ API is running and healthy!")
    except Exception as e:
        print(f"\n✗ Error: API is not accessible at {BASE_URL}")
        print(f"  Make sure the server is running: python main.py")
        print(f"  Error: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("LEGAL DOCUMENT DRAFTING ENGINE - EXAMPLES & TESTING")
    print("=" * 60)

    # Check API health first
    check_api_health()

    # Show available templates
    show_available_templates()

    # Run examples
    print("\n" + "=" * 60)
    print("RUNNING EXAMPLES")
    print("=" * 60)
    print("\nNote: Make sure the API is running before executing examples.")
    print("Start the API with: python main.py")

    # Uncomment the examples you want to run:

    # example_loan_agreement()
    # example_service_agreement()
    # example_nda()
    # example_employment_contract()
    # example_rental_agreement()
    # example_partnership_deed()
    # example_auto_detect()

    print("\n" + "=" * 60)
    print("To run examples, uncomment them in the __main__ section")
    print("=" * 60)
