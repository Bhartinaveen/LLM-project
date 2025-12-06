# API Reference Guide

## Base URL
```
http://localhost:8000
```

## Authentication
Currently no authentication required. For production, add API key authentication.

## Content-Type
All requests should use:
```
Content-Type: application/json
```

---

## Endpoints

### 1. Health Check
Check if the API is running.

```http
GET /health
```

**Response (200 OK)**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.123456",
  "version": "1.0.0"
}
```

**Example**:
```bash
curl http://localhost:8000/health
```

---

### 2. List Available Templates
Get list of all supported document types.

```http
GET /templates
```

**Response (200 OK)**:
```json
{
  "success": true,
  "templates": [
    "loan_agreement",
    "rental_agreement",
    "nda",
    "service_agreement",
    "employment_contract",
    "partnership_deed",
    "affidavit"
  ],
  "count": 7
}
```

**Example**:
```bash
curl http://localhost:8000/templates
```

---

### 3. Draft Document (Main Endpoint)
Generate a legal document based on user prompt and details.

```http
POST /draft-document
Content-Type: application/json
```

**Request Body** (JSON):
```json
{
  "prompt": "Natural language description of the document",
  "document_type": "Optional: one of the supported types",
  "details": {
    "key1": "value1",
    "key2": "value2"
  },
  "include_metadata": true
}
```

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | Natural language description of the document to generate |
| `document_type` | string | No | Document type (auto-detected if not provided). Options: `loan_agreement`, `rental_agreement`, `nda`, `service_agreement`, `employment_contract`, `partnership_deed`, `affidavit` |
| `details` | object | No | Structured details for the document (optional, defaults provided) |
| `include_metadata` | boolean | No | Include metadata in footer (default: true) |

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Document successfully generated",
  "document_type": "loan_agreement",
  "file_path": "./outputs/Loan-Agreement_20240101_120000.docx",
  "download_url": "/download/Loan-Agreement_20240101_120000.docx",
  "metadata": {
    "document_type": "loan_agreement",
    "generated_at": "2024-01-01T12:00:00.123456"
  }
}
```

**Response (400 Bad Request)**:
```json
{
  "success": false,
  "error": "Invalid input",
  "detail": "Prompt cannot be empty",
  "timestamp": "2024-01-01T12:00:00.123456"
}
```

**Response (500 Internal Server Error)**:
```json
{
  "success": false,
  "error": "Internal server error",
  "detail": "An unexpected error occurred",
  "timestamp": "2024-01-01T12:00:00.123456"
}
```

---

### 4. Download Document
Download a previously generated document.

```http
GET /download/{filename}
```

**Path Parameters**:
- `filename`: Name of the DOCX file to download (e.g., `Loan-Agreement_20240101_120000.docx`)

**Response (200 OK)**:
- Binary DOCX file

**Response (404 Not Found)**:
```json
{
  "detail": "Document not found"
}
```

**Example**:
```bash
curl -o document.docx http://localhost:8000/download/Loan-Agreement_20240101_120000.docx
```

---

## Request Examples

### Example 1: Loan Agreement with Auto-Detection
```bash
curl -X POST http://localhost:8000/draft-document \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "I need a loan agreement for 5 lakh rupees between Rohit Gupta and Akash Mehta"
  }'
```

### Example 2: Loan Agreement with Explicit Details
```bash
curl -X POST http://localhost:8000/draft-document \
  -H "Content-Type: application/json" \
  -d '{
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
      "additional_details": "Monthly repayment on the 1st of each month"
    }
  }'
```

### Example 3: Service Agreement
```bash
curl -X POST http://localhost:8000/draft-document \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a service agreement for software development",
    "document_type": "service_agreement",
    "details": {
      "service_provider": "Tech Solutions Ltd",
      "service_client": "ABC Corporation",
      "service_description": "Custom software development",
      "service_fees": "₹25,00,000",
      "currency": "INR",
      "payment_schedule": "50% upfront, 50% on completion",
      "term_duration": "24"
    }
  }'
```

### Example 4: NDA
```bash
curl -X POST http://localhost:8000/draft-document \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Draft an NDA between Company A and Company B",
    "document_type": "nda",
    "details": {
      "disclosing_party": "Company A",
      "receiving_party": "Company B",
      "purpose": "Business partnership evaluation",
      "info_type": "Proprietary technology and financial data",
      "term_duration": "24",
      "jurisdiction": "India"
    }
  }'
```

---

## Document Type Details

### Loan Agreement
**Key Variables**:
- `lender_name`: Name of the lender
- `borrower_name`: Name of the borrower
- `loan_amount`: Amount being loaned
- `currency`: Currency (e.g., INR)
- `interest_rate`: Interest rate percentage
- `tenure`: Loan duration in months
- `repayment_frequency`: How often repayment occurs (e.g., Monthly)
- `date`: Agreement date
- `jurisdiction`: Jurisdiction for the agreement
- `additional_details`: Any additional terms

**Typical Prompt**:
```
Draft a Loan Agreement for ₹5,00,000 between Rohit Gupta (Lender) and Akash Mehta (Borrower), tenure 12 months, interest 10 percent, monthly repayment.
```

### Rental Agreement
**Key Variables**:
- `landlord_name`: Name of property owner
- `tenant_name`: Name of tenant
- `property_address`: Full property address
- `property_type`: Type of property (e.g., Residential 2-BHK)
- `rent_amount`: Monthly rent amount
- `currency`: Currency
- `lease_duration`: Duration in months
- `deposit_amount`: Security deposit amount
- `start_date`: Lease start date
- `jurisdiction`: Jurisdiction
- `additional_details`: Additional terms

**Typical Prompt**:
```
Create a rental agreement for a 2-bedroom apartment at 123 Main Street between John Smith (Landlord) and Jane Doe (Tenant), monthly rent ₹25,000.
```

### Non-Disclosure Agreement (NDA)
**Key Variables**:
- `disclosing_party`: Party disclosing information
- `receiving_party`: Party receiving information
- `purpose`: Purpose of disclosure
- `info_type`: Type of confidential information
- `term_duration`: Duration in months
- `jurisdiction`: Jurisdiction
- `additional_details`: Additional terms

**Typical Prompt**:
```
Draft an NDA between TechCorp and InnovateLabs for partnership evaluation.
```

### Service Agreement
**Key Variables**:
- `service_provider`: Service provider name
- `service_client`: Client name
- `service_description`: Description of services
- `service_fees`: Service cost
- `currency`: Currency
- `payment_schedule`: Payment schedule
- `term_duration`: Duration in months
- `jurisdiction`: Jurisdiction
- `additional_details`: Additional terms

**Typical Prompt**:
```
Create a service agreement for website maintenance between Web Solutions (provider) and RetailCorp (client).
```

### Employment Contract
**Key Variables**:
- `employee_name`: Employee name
- `employer_name`: Employer name
- `position`: Job position
- `department`: Department
- `salary`: Annual/Monthly salary
- `currency`: Currency
- `employment_type`: Full-time, Part-time, Contract
- `start_date`: Start date
- `jurisdiction`: Jurisdiction
- `additional_details`: Additional benefits/terms

**Typical Prompt**:
```
Draft an Employment Contract for John Doe as Senior Developer at TechCorp, annual salary ₹15,00,000.
```

### Partnership Deed
**Key Variables**:
- `partner_names`: Names of all partners
- `business_name`: Business name
- `business_description`: Description of business
- `place_of_business`: Business location
- `capital_contributions`: Capital amounts
- `profit_sharing_ratio`: Profit sharing percentages
- `management_rights`: Management structure
- `jurisdiction`: Jurisdiction
- `additional_details`: Additional terms

**Typical Prompt**:
```
Create a partnership deed between Raj Kumar and Priya Singh for a consulting business.
```

### Affidavit
**Key Variables**:
- `affiant_name`: Name of person making statement
- `affiant_address`: Address of affiant
- `date`: Date of affidavit
- `purpose`: Purpose of affidavit
- `statement_content`: Content of the statement
- `jurisdiction`: Jurisdiction
- `additional_details`: Additional details

**Typical Prompt**:
```
Draft an affidavit for Rajesh Kumar regarding a property ownership claim.
```

---

## Error Handling

### Error Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Document generated successfully |
| 400 | Bad Request | Missing required field, invalid input |
| 404 | Not Found | Document file not found |
| 500 | Server Error | OpenAI API error, unexpected exception |

### Error Response Format
```json
{
  "success": false,
  "error": "Error type",
  "detail": "Detailed error message",
  "timestamp": "2024-01-01T12:00:00.123456"
}
```

---

## Rate Limiting
Currently not implemented. Production deployment should include:
- Per-minute request limits
- Per-user quotas
- Cost tracking for API usage

---

## Testing the API

### Using Swagger UI
1. Go to http://localhost:8000/docs
2. Expand any endpoint
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"
6. View the response

### Using curl
```bash
# Check health
curl http://localhost:8000/health

# List templates
curl http://localhost:8000/templates

# Draft document
curl -X POST http://localhost:8000/draft-document \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Draft a loan agreement..."}'

# Download document
curl -O http://localhost:8000/download/filename.docx
```

### Using Python
```python
import requests

# Draft document
response = requests.post(
    "http://localhost:8000/draft-document",
    json={
        "prompt": "Draft a loan agreement for ₹5,00,000...",
        "document_type": "loan_agreement",
        "details": {...}
    }
)

print(response.json())

# Download document
if response.status_code == 200:
    result = response.json()
    download_response = requests.get(
        f"http://localhost:8000{result['download_url']}"
    )
    with open("document.docx", "wb") as f:
        f.write(download_response.content)
```

---

## Performance Notes

- **Typical Response Time**: 10-40 seconds (LLM processing time)
- **DOCX Generation Time**: < 1 second
- **File Size**: 50-200 KB per document
- **Concurrent Requests**: Supported by async processing

---

## Best Practices

1. **Always check `success` field** in response
2. **Provide detailed `details` object** for better results
3. **Use `document_type` parameter** to avoid auto-detection
4. **Save `download_url`** for later retrieval
5. **Include `jurisdiction`** for location-specific clauses
6. **Review generated documents** before using legally

---

## Troubleshooting

### API Not Responding
- Check if server is running: `python main.py`
- Check firewall settings
- Verify port 8000 is available

### Document Generation Fails
- Check OpenAI API key in `.env`
- Check API quota and billing
- Review error details in logs

### Downloaded File is Empty
- Wait for generation to complete
- Check file exists in `./outputs` folder
- Verify download URL from response

---

**API Version**: 1.0.0
**Last Updated**: December 2024
