# Quick Start Guide

## System Requirements
- Python 3.8 or higher
- 100MB disk space (for dependencies)
- Internet connection (for OpenAI API)
- OpenAI API key

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure OpenAI API Key
Create a `.env` file in the project root:
```bash
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Start the Server
```bash
python main.py
```

You should see:
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4. Test the API

Open your browser and go to:
- **Interactive Docs**: http://localhost:8000/docs
- **API Docs**: http://localhost:8000/redoc

## Generating Your First Document

### Using the Web UI (Swagger)
1. Go to http://localhost:8000/docs
2. Expand the `/draft-document` endpoint
3. Click "Try it out"
4. Paste this example JSON:

```json
{
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
}
```

5. Click "Execute"
6. Download the generated DOCX file from the response

### Using curl
```bash
curl -X POST "http://localhost:8000/draft-document" \
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
      "repayment_frequency": "Monthly"
    }
  }'
```

### Using Python
```python
import requests
import json

response = requests.post(
    "http://localhost:8000/draft-document",
    json={
        "prompt": "Draft a Loan Agreement for ₹5,00,000 between Rohit Gupta and Akash Mehta, tenure 12 months, interest 10%",
        "document_type": "loan_agreement",
        "details": {
            "lender_name": "Rohit Gupta",
            "borrower_name": "Akash Mehta",
            "loan_amount": "₹5,00,000",
            "currency": "INR",
            "interest_rate": "10",
            "tenure": "12"
        }
    }
)

result = response.json()
print(json.dumps(result, indent=2))
```

## Common Errors & Solutions

### Error: "OPENAI_API_KEY not found"
**Solution**: Create `.env` file with your OpenAI API key
```bash
echo OPENAI_API_KEY=sk-your-key >> .env
```

### Error: "Module not found"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Error: "Connection refused"
**Solution**: Make sure the server is running
```bash
python main.py
```

### Error: "API rate limit"
**Solution**: Your OpenAI account may have hit rate limits. Wait a few moments and retry.

## Supported Document Types

Quick reference for `document_type` parameter:

1. **loan_agreement** - Loan agreements between lender and borrower
2. **rental_agreement** - Property rental/lease agreements
3. **nda** - Non-disclosure agreements
4. **service_agreement** - Service contracts
5. **employment_contract** - Employee contracts
6. **partnership_deed** - Partnership agreements
7. **affidavit** - Sworn statements

## Next Steps

- Review the full [README.md](README.md) for detailed documentation
- Check [examples.py](examples.py) for more usage examples
- Explore the API documentation at http://localhost:8000/docs
- Review generated documents in the `./outputs` folder

## Troubleshooting

View logs:
```bash
# Windows
type logs\app.log

# Linux/Mac
tail -f logs/app.log
```

## Need Help?

1. Check the README.md file
2. Review the API documentation at http://localhost:8000/docs
3. Check the logs in `./logs/app.log`
4. Review examples.py for working examples

Enjoy document generation! 📄
