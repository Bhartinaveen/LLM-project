"""
RAG (Retrieval-Augmented Generation) Pipeline
Handles legal document templates and retrieval
"""

import logging
import json
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class LegalTemplateDatabase:
    """In-memory database of legal document templates"""

    def __init__(self):
        """Initialize template database"""
        self.templates = self._load_templates()
        logger.info(f"Loaded {len(self.templates)} document templates")

    def _load_templates(self) -> Dict[str, Dict]:
        """
        Load legal document templates
        
        Returns:
            Dictionary of document templates
        """
        return {
            "loan_agreement": {
                "type": "Loan Agreement",
                "sections": [
                    "parties",
                    "loan_terms",
                    "interest_rate",
                    "repayment_schedule",
                    "default_conditions",
                    "prepayment",
                    "governing_law",
                    "signatures",
                ],
                "key_elements": [
                    "loan_amount",
                    "interest_rate",
                    "tenure",
                    "repayment_frequency",
                    "lender_name",
                    "borrower_name",
                    "date",
                ],
            },
            "rental_agreement": {
                "type": "Rental Agreement",
                "sections": [
                    "parties",
                    "property_description",
                    "rental_terms",
                    "rent_amount",
                    "deposit",
                    "maintenance",
                    "termination",
                    "governing_law",
                    "signatures",
                ],
                "key_elements": [
                    "property_address",
                    "rent_amount",
                    "lease_duration",
                    "landlord_name",
                    "tenant_name",
                    "deposit_amount",
                ],
            },
            "nda": {
                "type": "Non-Disclosure Agreement",
                "sections": [
                    "parties",
                    "definitions",
                    "confidential_information",
                    "obligations",
                    "exclusions",
                    "term",
                    "return_of_information",
                    "governing_law",
                    "signatures",
                ],
                "key_elements": [
                    "parties_names",
                    "purpose",
                    "term_months",
                    "jurisdiction",
                ],
            },
            "service_agreement": {
                "type": "Service Agreement",
                "sections": [
                    "parties",
                    "scope_of_services",
                    "terms",
                    "fees",
                    "payment_terms",
                    "intellectual_property",
                    "termination",
                    "governing_law",
                    "signatures",
                ],
                "key_elements": [
                    "service_provider",
                    "service_client",
                    "service_description",
                    "fees",
                    "payment_schedule",
                ],
            },
            "employment_contract": {
                "type": "Employment Contract",
                "sections": [
                    "parties",
                    "position_details",
                    "responsibilities",
                    "compensation",
                    "benefits",
                    "term",
                    "confidentiality",
                    "termination",
                    "governing_law",
                    "signatures",
                ],
                "key_elements": [
                    "employee_name",
                    "employer_name",
                    "position",
                    "salary",
                    "start_date",
                    "employment_type",
                ],
            },
            "partnership_deed": {
                "type": "Partnership Deed",
                "sections": [
                    "parties",
                    "name_of_partnership",
                    "principal_place_of_business",
                    "nature_of_business",
                    "capital_contribution",
                    "profit_sharing",
                    "management",
                    "dissolution",
                    "governing_law",
                    "signatures",
                ],
                "key_elements": [
                    "partner_names",
                    "business_name",
                    "business_description",
                    "capital_contributions",
                    "profit_sharing_ratio",
                ],
            },
            "affidavit": {
                "type": "Affidavit",
                "sections": [
                    "title",
                    "affiant_details",
                    "statement_of_facts",
                    "certification",
                    "jurat",
                    "signature",
                ],
                "key_elements": [
                    "affiant_name",
                    "affiant_address",
                    "statement_content",
                    "date",
                ],
            },
        }

    def get_template(self, doc_type: str) -> Optional[Dict]:
        """
        Retrieve template for a document type
        
        Args:
            doc_type: Type of document (e.g., 'loan_agreement')
            
        Returns:
            Template dictionary or None
        """
        return self.templates.get(doc_type.lower())

    def list_document_types(self) -> List[str]:
        """
        Get list of available document types
        
        Returns:
            List of document type keys
        """
        return list(self.templates.keys())

    def search_templates(self, query: str) -> List[str]:
        """
        Search templates by keyword
        
        Args:
            query: Search query
            
        Returns:
            List of matching template keys
        """
        query_lower = query.lower()
        results = []
        for key, template in self.templates.items():
            if (
                query_lower in key.lower()
                or query_lower in template["type"].lower()
            ):
                results.append(key)
        return results


class RAGPipeline:
    """RAG pipeline for legal document generation"""

    def __init__(self):
        """Initialize RAG pipeline"""
        self.template_db = LegalTemplateDatabase()
        logger.info("RAG Pipeline initialized")

    def identify_document_type(self, prompt: str) -> Optional[str]:
        """
        Identify document type from user prompt
        
        Args:
            prompt: User prompt
            
        Returns:
            Document type key or None
        """
        prompt_lower = prompt.lower()
        keywords = {
            "loan_agreement": ["loan", "lender", "borrower"],
            "rental_agreement": ["rental", "lease", "tenant", "landlord"],
            "nda": ["confidential", "nda", "non-disclosure"],
            "service_agreement": ["service", "provider", "client"],
            "employment_contract": ["employment", "employee", "hired", "job"],
            "partnership_deed": ["partnership", "partner", "business"],
            "affidavit": ["affidavit", "sworn", "statement"],
        }

        for doc_type, keywords_list in keywords.items():
            if any(kw in prompt_lower for kw in keywords_list):
                return doc_type

        # Default to searching templates
        searches = self.template_db.search_templates(prompt)
        return searches[0] if searches else None

    def retrieve_relevant_context(
        self, prompt: str, doc_type: str
    ) -> Dict[str, any]:
        """
        Retrieve relevant context for document generation
        
        Args:
            prompt: User prompt
            doc_type: Document type
            
        Returns:
            Context dictionary with template and guidelines
        """
        template = self.template_db.get_template(doc_type)
        if not template:
            logger.warning(f"Template not found for document type: {doc_type}")
            return {}

        context = {
            "document_type": doc_type,
            "template": template,
            "sections": template.get("sections", []),
            "key_elements": template.get("key_elements", []),
            "user_prompt": prompt,
        }

        logger.info(f"Retrieved context for document type: {doc_type}")
        return context

    def prepare_rag_context(self, prompt: str) -> Dict[str, any]:
        """
        Full RAG pipeline: identify type and retrieve context
        
        Args:
            prompt: User prompt
            
        Returns:
            Complete RAG context
        """
        doc_type = self.identify_document_type(prompt)
        if not doc_type:
            logger.warning("Could not identify document type from prompt")
            return {"error": "Document type could not be identified"}

        context = self.retrieve_relevant_context(prompt, doc_type)
        return context


def get_rag_pipeline() -> RAGPipeline:
    """Get RAG pipeline instance"""
    return RAGPipeline()
