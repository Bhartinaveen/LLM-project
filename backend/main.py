"""
FastAPI Application for Legal Document Drafting
Main entry point for the LLM-based legal document generation system
"""

import logging
import sys
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field, field_validator, ConfigDict
import uvicorn

from src.llm_config import initialize_llm
from src.rag_pipeline import RAGPipeline
from src.prompt_templates import get_prompt_templates
from src.document_generator import DocumentGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("./logs/app.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Legal Document Drafting Engine",
    description="LLM-based system for generating legal documents",
    version="1.0.0",
)

# Configure CORS
from fastapi.middleware.cors import CORSMiddleware
import os

# Define allowed origins
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "https://llm-project-frontend.vercel.app",
    "https://llm-project-backend.vercel.app",
]

# Add origins from environment variable if present
env_origins = os.getenv("ALLOWED_ORIGINS")
if env_origins:
    origins.extend([origin.strip() for origin in env_origins.split(",")])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
rag_pipeline = RAGPipeline()
prompt_templates = get_prompt_templates()
doc_generator = DocumentGenerator("./outputs")


class DocumentRequest(BaseModel):
    """Request model for document drafting"""

    prompt: str = Field(
        ..., description="Natural language description of the document to generate"
    )
    document_type: Optional[str] = Field(
        None, description="Type of document (auto-detected if not provided)"
    )
    details: Optional[Dict[str, Any]] = Field(
        {}, description="Structured details for the document"
    )
    include_metadata: Optional[bool] = Field(
        True, description="Include metadata in footer"
    )

    @field_validator("prompt")
    @classmethod
    def prompt_not_empty(cls, v):
        """Validate prompt is not empty"""
        if not v or not v.strip():
            raise ValueError("Prompt cannot be empty")
        return v.strip()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "prompt": "Draft a Loan Agreement for ₹5,00,000 between Rohit Gupta (Lender) and Akash Mehta (Borrower), tenure 12 months, interest 10 percent, monthly repayment.",
                "document_type": None,
                "details": {
                    "lender_name": "Rohit Gupta",
                    "borrower_name": "Akash Mehta",
                    "loan_amount": "₹5,00,000",
                    "interest_rate": "10",
                    "tenure": "12",
                },
            }
        }
    )


class DocumentResponse(BaseModel):
    """Response model for document drafting"""

    success: bool
    message: str
    document_type: str
    file_path: str
    download_url: str
    metadata: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Error response model"""

    success: bool = False
    error: str
    detail: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class HealthResponse(BaseModel):
    """Health check response"""

    status: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    version: str


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Legal Document Drafting Engine",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "draft": "/draft-document",
            "list_templates": "/templates",
        },
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="healthy", version="1.0.0")


@app.get("/templates", tags=["Info"])
async def list_templates():
    """List available document templates"""
    try:
        templates = prompt_templates.list_templates()
        return {
            "success": True,
            "templates": templates,
            "count": len(templates),
        }
    except Exception as e:
        logger.error(f"Error listing templates: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list templates")


@app.post("/draft-document", response_model=DocumentResponse, tags=["Drafting"])
async def draft_document(request: DocumentRequest) -> DocumentResponse:
    """
    Main endpoint for drafting legal documents
    
    Args:
        request: DocumentRequest with prompt and optional details
        
    Returns:
        DocumentResponse with generated document path
    """
    try:
        logger.info(f"Received draft request: {request.prompt[:100]}...")

        # Step 1: Identify document type and retrieve context
        if request.document_type:
            doc_type = request.document_type.lower()
        else:
            rag_context = rag_pipeline.prepare_rag_context(request.prompt)
            if "error" in rag_context:
                raise ValueError("Could not identify document type from prompt")
            doc_type = rag_context.get("document_type")

        logger.info(f"Document type identified: {doc_type}")

        # Step 2: Prepare prompt with template and details
        template = prompt_templates.get_template(doc_type)
        if not template:
            raise ValueError(f"Template not found for document type: {doc_type}")

        # Merge provided details with defaults
        template_vars = _prepare_template_variables(doc_type, request.details)

        # Format the prompt for LLM
        formatted_prompt = template.format(**template_vars)
        logger.info(f"Formatted prompt prepared for {doc_type}")

        # Step 3: Generate content using LLM
        logger.info("Calling LLM for document generation...")
        llm = initialize_llm()

        try:
            response = llm.invoke(formatted_prompt)
            content = response.content
            logger.info(f"LLM response received ({len(content)} characters)")
        except Exception as llm_error:
            logger.error(f"LLM error: {str(llm_error)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate document content: {str(llm_error)}",
            )

        # Step 4: Generate DOCX document
        metadata = {
            "document_type": doc_type,
            "generated_at": datetime.now().isoformat(),
        } if request.include_metadata else None

        file_path = doc_generator.generate_document(content, doc_type, metadata)
        logger.info(f"Document generated: {file_path}")

        # Prepare response
        return DocumentResponse(
            success=True,
            message=f"Document successfully generated",
            document_type=doc_type,
            file_path=file_path,
            download_url=f"/download/{Path(file_path).name}",
            metadata=metadata,
        )

    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error in draft_document: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Failed to generate document: {str(e)}"
        )


@app.get("/download/{filename}", tags=["Download"])
async def download_document(filename: str):
    """
    Download generated document
    
    Args:
        filename: Name of the file to download
        
    Returns:
        FileResponse with the DOCX file
    """
    try:
        file_path = Path("./outputs") / filename

        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            raise HTTPException(status_code=404, detail="Document not found")

        logger.info(f"Downloading file: {file_path}")
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to download document")


@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Custom exception handler for ValueError"""
    return JSONResponse(
        status_code=400,
        content={"success": False, "error": "Invalid input", "detail": str(exc)},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": "An unexpected error occurred",
        },
    )


def _prepare_template_variables(doc_type: str, user_details: Dict[str, Any]) -> Dict[str, str]:
    """
    Prepare template variables with defaults
    
    Args:
        doc_type: Type of document
        user_details: User-provided details
        
    Returns:
        Dictionary of template variables
    """
    defaults = {
        "loan_agreement": {
            "lender_name": "Lender",
            "borrower_name": "Borrower",
            "loan_amount": "Amount to be specified",
            "currency": "INR",
            "interest_rate": "0",
            "tenure": "12",
            "repayment_frequency": "Monthly",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "jurisdiction": "India",
            "additional_details": "As per mutual agreement",
        },
        "rental_agreement": {
            "landlord_name": "Landlord",
            "tenant_name": "Tenant",
            "property_address": "Property Address",
            "property_type": "Residential",
            "rent_amount": "Amount to be specified",
            "currency": "INR",
            "lease_duration": "12",
            "deposit_amount": "Amount to be specified",
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "jurisdiction": "India",
            "additional_details": "As per mutual agreement",
        },
        "nda": {
            "disclosing_party": "Party A",
            "receiving_party": "Party B",
            "purpose": "Business evaluation",
            "info_type": "Confidential Information",
            "term_duration": "24",
            "jurisdiction": "India",
            "additional_details": "As per mutual agreement",
        },
        "service_agreement": {
            "service_provider": "Service Provider",
            "service_client": "Client",
            "service_description": "Services to be specified",
            "service_fees": "Amount to be specified",
            "currency": "INR",
            "payment_schedule": "As per invoice",
            "term_duration": "12",
            "jurisdiction": "India",
            "additional_details": "As per mutual agreement",
        },
        "employment_contract": {
            "employee_name": "Employee",
            "employer_name": "Employer",
            "position": "Position Title",
            "department": "Department",
            "salary": "Amount to be specified",
            "currency": "INR",
            "employment_type": "Full-time",
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "jurisdiction": "India",
            "additional_details": "As per mutual agreement",
        },
        "partnership_deed": {
            "partner_names": "Partner 1, Partner 2",
            "business_name": "Business Name",
            "business_description": "Business Description",
            "place_of_business": "Location",
            "capital_contributions": "Amount to be specified",
            "profit_sharing_ratio": "Equal",
            "management_rights": "Equal",
            "jurisdiction": "India",
            "additional_details": "As per mutual agreement",
        },
        "affidavit": {
            "affiant_name": "Affiant Name",
            "affiant_address": "Affiant Address",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "purpose": "Statement of facts",
            "statement_content": "Facts to be specified",
            "jurisdiction": "India",
            "additional_details": "As per requirement",
        },
    }

    # Get defaults for document type
    template_vars = defaults.get(doc_type, {})

    # Override with user-provided details
    template_vars.update(user_details)

    return template_vars


if __name__ == "__main__":
    logger.info("Starting Legal Document Drafting Engine API...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
