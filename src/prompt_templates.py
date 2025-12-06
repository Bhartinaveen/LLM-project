"""
Prompt Templates for Legal Document Generation
Contains structured prompts for different document types
"""

from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class PromptTemplate:
    """Base prompt template class"""

    def __init__(self, name: str, template: str, variables: List[str]):
        """
        Initialize prompt template
        
        Args:
            name: Template name
            template: Template string with {variable} placeholders
            variables: List of required variables
        """
        self.name = name
        self.template = template
        self.variables = variables

    def format(self, **kwargs) -> str:
        """
        Format template with variables
        
        Args:
            **kwargs: Variable values
            
        Returns:
            Formatted prompt string
        """
        return self.template.format(**kwargs)


class LegalPromptTemplates:
    """Collection of legal document prompt templates"""

    def __init__(self):
        """Initialize prompt templates"""
        self.templates = self._initialize_templates()
        logger.info("Legal prompt templates initialized")

    def _initialize_templates(self) -> Dict[str, PromptTemplate]:
        """Initialize all prompt templates"""

        return {
            "loan_agreement": PromptTemplate(
                name="Loan Agreement",
                template="""You are a legal expert drafting a professional Loan Agreement.
Generate a comprehensive and legally sound Loan Agreement based on the following details.

**IMPORTANT: Output the document in strictly formatted Markdown.**
- Use `# Title` for the main document title.
- Use `## Section Name` for all major section headings (e.g., 1. Definitions).
- Use `### Subsection Name` for sub-clauses if needed.
- Use `**Bold**` for defined terms or emphasis.
- Use standard paragraphs for text.
- Use `[SIGNATURE_BLOCK]` as a placeholder where signatures should go.

**Details:**
- Lender Name: {lender_name}
- Borrower Name: {borrower_name}
- Loan Amount: {loan_amount}
- Currency: {currency}
- Interest Rate: {interest_rate}%
- Tenure: {tenure} months
- Repayment Frequency: {repayment_frequency}
- Date of Agreement: {date}
- Jurisdiction: {jurisdiction}
- Additional Details: {additional_details}

**Required Sections:**
1. Title and Parties
2. Definitions and Interpretations
3. Loan Terms (Amount, Purpose, Disbursement)
4. Interest Rate and Calculation
5. Repayment Schedule and Amount
6. Payment Terms and Methods
7. Default Conditions and Remedies
8. Prepayment Options
9. Representations and Warranties
10. Indemnification
11. Termination Clause
12. Governing Law and Jurisdiction
13. Dispute Resolution
14. Signature Block

Ensure the document is formal, legally accurate, and includes all necessary clauses.""",
                variables=[
                    "lender_name",
                    "borrower_name",
                    "loan_amount",
                    "currency",
                    "interest_rate",
                    "tenure",
                    "repayment_frequency",
                    "date",
                    "jurisdiction",
                    "additional_details",
                ],
            ),
            "rental_agreement": PromptTemplate(
                name="Rental Agreement",
                template="""You are a legal expert drafting a professional Rental Agreement.
Generate a comprehensive and legally sound Rental Agreement based on the following details.

**IMPORTANT: Output the document in strictly formatted Markdown.**
- Use `# Title` for the main document title.
- Use `## Section Name` for all major section headings.
- Use `**Bold**` for emphasis.
- Use `[SIGNATURE_BLOCK]` for signatures.

**Details:**
- Landlord Name: {landlord_name}
- Tenant Name: {tenant_name}
- Property Address: {property_address}
- Property Type: {property_type}
- Rent Amount: {rent_amount}
- Currency: {currency}
- Lease Duration: {lease_duration} months
- Deposit Amount: {deposit_amount}
- Lease Start Date: {start_date}
- Jurisdiction: {jurisdiction}
- Additional Details: {additional_details}

**Required Sections:**
1. Parties and Property Description
2. Term of Lease
3. Rent Payment Terms
4. Security Deposit
5. Maintenance and Repairs
6. Utilities and Services
7. Tenant Obligations
8. Landlord Obligations
9. Entry Rights
10. Alterations to Property
11. Termination Clause
12. Eviction Conditions
13. Renewal Terms
14. Governing Law and Jurisdiction
15. Dispute Resolution
16. Signature Blocks""",
                variables=[
                    "landlord_name",
                    "tenant_name",
                    "property_address",
                    "property_type",
                    "rent_amount",
                    "currency",
                    "lease_duration",
                    "deposit_amount",
                    "start_date",
                    "jurisdiction",
                    "additional_details",
                ],
            ),
            "nda": PromptTemplate(
                name="Non-Disclosure Agreement",
                template="""You are a legal expert drafting a professional Non-Disclosure Agreement. 
Generate a comprehensive and legally sound NDA based on the following details:

Disclosing Party: {disclosing_party}
Receiving Party: {receiving_party}
Purpose of Disclosure: {purpose}
Confidential Information Type: {info_type}
Term Duration: {term_duration} months
Jurisdiction: {jurisdiction}

Additional Details: {additional_details}

Generate the document with the following sections:
1. Title and Parties
2. Definitions (Confidential Information, Disclosing Party, Receiving Party)
3. Scope of Confidential Information
4. Obligations of Receiving Party
5. Exclusions from Confidential Information
6. Term and Duration
7. Return or Destruction of Information
8. No License or Rights
9. No Obligation to Disclose
10. Remedies and Injunctive Relief
11. Indemnification
12. Governing Law and Jurisdiction
13. Entire Agreement
14. Amendment and Severability
15. Signature Block

Ensure the document is legally robust and protects sensitive information.""",
                variables=[
                    "disclosing_party",
                    "receiving_party",
                    "purpose",
                    "info_type",
                    "term_duration",
                    "jurisdiction",
                    "additional_details",
                ],
            ),
            "service_agreement": PromptTemplate(
                name="Service Agreement",
                template="""You are a legal expert drafting a professional Service Agreement. 
Generate a comprehensive and legally sound Service Agreement based on the following details:

Service Provider: {service_provider}
Service Client: {service_client}
Service Description: {service_description}
Service Fees: {service_fees}
Currency: {currency}
Payment Schedule: {payment_schedule}
Term Duration: {term_duration} months
Jurisdiction: {jurisdiction}

Additional Details: {additional_details}

Generate the document with the following sections:
1. Parties and Effective Date
2. Scope of Services
3. Service Delivery Timeline and Milestones
4. Fees and Payment Terms
5. Payment Methods and Schedule
6. Intellectual Property Rights
7. Confidentiality
8. Representations and Warranties
9. Limitation of Liability
10. Indemnification
11. Insurance Requirements
12. Term and Termination
13. Post-Termination Obligations
14. Dispute Resolution
15. Governing Law and Jurisdiction
16. Signature Block

Ensure the document clearly defines services, responsibilities, and payment terms.""",
                variables=[
                    "service_provider",
                    "service_client",
                    "service_description",
                    "service_fees",
                    "currency",
                    "payment_schedule",
                    "term_duration",
                    "jurisdiction",
                    "additional_details",
                ],
            ),
            "employment_contract": PromptTemplate(
                name="Employment Contract",
                template="""You are a legal expert drafting a professional Employment Contract. 
Generate a comprehensive and legally sound Employment Contract based on the following details:

Employee Name: {employee_name}
Employer Name: {employer_name}
Position: {position}
Department: {department}
Salary: {salary}
Currency: {currency}
Employment Type: {employment_type}
Start Date: {start_date}
Jurisdiction: {jurisdiction}

Additional Details: {additional_details}

Generate the document with the following sections:
1. Parties and Effective Date
2. Position and Responsibilities
3. Reporting Structure
4. Compensation and Benefits
5. Working Hours and Leave Policy
6. Confidentiality and Non-Disclosure
7. Non-Compete and Non-Solicitation
8. Intellectual Property Rights
9. Performance Standards
10. Termination Clause (Notice Period, Severance)
11. Grounds for Immediate Termination
12. Post-Employment Obligations
13. Dispute Resolution
14. Governing Law and Jurisdiction
15. Entire Agreement
16. Signature Block

Ensure the document is comprehensive and protects both employer and employee interests.""",
                variables=[
                    "employee_name",
                    "employer_name",
                    "position",
                    "department",
                    "salary",
                    "currency",
                    "employment_type",
                    "start_date",
                    "jurisdiction",
                    "additional_details",
                ],
            ),
            "partnership_deed": PromptTemplate(
                name="Partnership Deed",
                template="""You are a legal expert drafting a professional Partnership Deed. 
Generate a comprehensive and legally sound Partnership Deed based on the following details:

Partner Names: {partner_names}
Business Name: {business_name}
Business Description: {business_description}
Principal Place of Business: {place_of_business}
Capital Contributions: {capital_contributions}
Profit Sharing Ratio: {profit_sharing_ratio}
Management Rights: {management_rights}
Jurisdiction: {jurisdiction}

Additional Details: {additional_details}

Generate the document with the following sections:
1. Parties and Agreement Date
2. Name and Commencement of Partnership
3. Principal Place of Business
4. Nature and Objects of Partnership
5. Capital Contribution and Loans
6. Profit and Loss Sharing
7. Management and Decision Making
8. Rights and Duties of Partners
9. Restrictions on Partners
10. Banking and Accounts
11. Admission of New Partners
12. Retirement and Expulsion
13. Dissolution and Winding Up
14. Dispute Resolution
15. Governing Law and Jurisdiction
16. Signature Block

Ensure the document is legally comprehensive and covers all aspects of partnership operation.""",
                variables=[
                    "partner_names",
                    "business_name",
                    "business_description",
                    "place_of_business",
                    "capital_contributions",
                    "profit_sharing_ratio",
                    "management_rights",
                    "jurisdiction",
                    "additional_details",
                ],
            ),
            "affidavit": PromptTemplate(
                name="Affidavit",
                template="""You are a legal expert drafting a professional Affidavit. 
Generate a comprehensive and legally sound Affidavit based on the following details:

Affiant Name: {affiant_name}
Affiant Address: {affiant_address}
Date: {date}
Purpose of Affidavit: {purpose}
Statement Content: {statement_content}
Jurisdiction: {jurisdiction}

Additional Details: {additional_details}

Generate the document with the following sections:
1. Title (IN THE COURT OF...)
2. Affiant Details (Name, Address, Occupation)
3. Sworn Statement Declaration
4. Facts and Statements (Numbered paragraphs)
5. Belief and Knowledge Statement
6. Certification
7. Jurat (Oath/Affirmation)
8. Signature of Affiant
9. Witness/Notary Details
10. Notary Seal and Signature

Ensure the document follows legal affidavit format and is suitable for court filing.""",
                variables=[
                    "affiant_name",
                    "affiant_address",
                    "date",
                    "purpose",
                    "statement_content",
                    "jurisdiction",
                    "additional_details",
                ],
            ),
        }

    def get_template(self, doc_type: str) -> Optional[PromptTemplate]:
        """
        Get prompt template for document type
        
        Args:
            doc_type: Document type (e.g., 'loan_agreement')
            
        Returns:
            PromptTemplate or None
        """
        return self.templates.get(doc_type.lower())

    def list_templates(self) -> List[str]:
        """Get list of available templates"""
        return list(self.templates.keys())

    def format_prompt(self, doc_type: str, **kwargs) -> str:
        """
        Format a prompt for document generation
        
        Args:
            doc_type: Document type
            **kwargs: Template variables
            
        Returns:
            Formatted prompt string
        """
        template = self.get_template(doc_type)
        if not template:
            raise ValueError(f"Template not found for document type: {doc_type}")

        return template.format(**kwargs)


def get_prompt_templates() -> LegalPromptTemplates:
    """Get prompt templates instance"""
    return LegalPromptTemplates()
