"""
Data models for contract analysis
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class ContractType(str, Enum):
    """Enumeration of contract types"""
    EMPLOYMENT = "employment"
    VENDOR = "vendor"
    LEASE = "lease"
    PARTNERSHIP = "partnership"
    SERVICE = "service"
    OTHER = "other"


class RiskLevel(str, Enum):
    """Risk severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ClauseCategory(str, Enum):
    """Categories of contract clauses"""
    OBLIGATION = "obligation"
    RIGHT = "right"
    PROHIBITION = "prohibition"
    PENALTY = "penalty"
    INDEMNITY = "indemnity"
    TERMINATION = "termination"
    ARBITRATION = "arbitration"
    CONFIDENTIALITY = "confidentiality"
    IP_OWNERSHIP = "ip_ownership"
    OTHER = "other"


class NamedEntity(BaseModel):
    """Named entity extracted from contract"""
    text: str
    entity_type: str  # PERSON, ORG, DATE, MONEY, GPE, etc.
    start_char: int
    end_char: int


class Clause(BaseModel):
    """Represents a single contract clause"""
    clause_id: str
    title: Optional[str] = None
    text: str
    start_position: int
    end_position: int
    category: ClauseCategory
    risk_level: RiskLevel
    risk_score: float = Field(ge=0, le=100)
    reason_for_risk: Optional[str] = None
    plain_language_explanation: str
    suggested_alternative: Optional[str] = None
    entities: List[NamedEntity] = []
    is_unfavorable: bool = False
    compliance_flags: List[str] = []


class ContractMetadata(BaseModel):
    """Metadata about the contract"""
    contract_type: ContractType
    language: str  # 'en' or 'hi'
    parties: List[str] = []
    effective_date: Optional[str] = None
    expiration_date: Optional[str] = None
    jurisdiction: Optional[str] = None
    financial_amount: Optional[str] = None
    file_name: str
    file_size: int
    processed_at: datetime


class ContractAnalysis(BaseModel):
    """Complete contract analysis result"""
    contract_id: str
    metadata: ContractMetadata
    summary: str
    clauses: List[Clause] = []
    composite_risk_score: float = Field(ge=0, le=100)
    composite_risk_level: RiskLevel
    key_risks: List[str] = []
    compliance_issues: List[str] = []
    unfavorable_clauses: List[str] = []  # clause_ids of unfavorable clauses
    recommendations: List[str] = []
    audit_trail_id: str
    analysis_timestamp: datetime


class AuditLogEntry(BaseModel):
    """Audit log entry for tracking analysis"""
    log_id: str
    contract_id: str
    action: str  # 'upload', 'analyze', 'export', 'feedback'
    timestamp: datetime
    user_ip: Optional[str] = None
    details: Dict[str, Any] = {}
    status: str  # 'success', 'failure', 'partial'


class ExportRequest(BaseModel):
    """Request for exporting analysis results"""
    format: str  # 'pdf', 'json', 'docx'
    include_audit_trail: bool = False
    include_recommendations: bool = True
