"""
Contract Analysis Engine - Main orchestrator
"""
import logging
from typing import Optional
from src.utils.file_processor import FileProcessor
from src.utils.text_preprocessor import TextPreprocessor
from src.core.contract_classifier import ContractClassifier
from src.core.ner_processor import NERProcessor
from src.core.clause_extractor import ClauseExtractor
from src.core.risk_assessor import RiskAssessor
from src.core.compliance_checker import ComplianceChecker
from src.core.llm_integration import LLMIntegration
from src.models.contract_models import ContractAnalysis, ContractMetadata, ContractType, AuditLogEntry
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class ContractAnalysisEngine:
    """Main orchestrator for contract analysis"""
    
    def __init__(self, use_llm: bool = True, llm_provider: str = "claude"):
        """
        Initialize analysis engine
        
        Args:
            use_llm: Whether to use LLM for enhanced analysis
            llm_provider: LLM provider to use (claude or openai)
        """
        self.use_llm = use_llm
        self.llm = None
        
        if use_llm:
            try:
                self.llm = LLMIntegration(provider=llm_provider)
            except Exception as e:
                logger.warning(f"Failed to initialize LLM: {e}")
                self.use_llm = False
    
    def analyze_contract(self, file_path: str, contract_type: Optional[str] = None) -> ContractAnalysis:
        """
        Perform complete contract analysis
        
        Args:
            file_path: Path to contract file
            contract_type: Optional contract type (auto-detect if not provided)
            
        Returns:
            ContractAnalysis object with complete analysis
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format not supported
        """
        contract_id = str(uuid.uuid4())
        
        # Step 1: Extract text from file
        logger.info(f"Extracting text from {file_path}")
        text, file_type = FileProcessor.extract_text(file_path)
        file_info = FileProcessor.get_file_info(file_path)
        
        # Step 2: Preprocess text
        logger.info("Preprocessing text")
        text = TextPreprocessor.clean_text(text)
        text = TextPreprocessor.normalize_whitespace(text)
        detected_language = TextPreprocessor.detect_language(text)
        
        # Step 3: Classify contract
        logger.info("Classifying contract type")
        if contract_type:
            try:
                classified_type = ContractType[contract_type.upper()]
                confidence = 1.0
            except KeyError:
                classified_type, confidence = ContractClassifier.classify(text)
        else:
            classified_type, confidence = ContractClassifier.classify(text)
        
        # Step 4: Extract entities
        logger.info("Extracting named entities")
        entities = NERProcessor.extract_entities(text)
        specific_info = NERProcessor.extract_specific_info(text)
        
        # Step 5: Extract clauses
        logger.info("Extracting clauses")
        clauses = ClauseExtractor.extract_clauses(text)
        
        # Step 6: Assess risks
        logger.info("Assessing risks")
        unfavorable_ids = RiskAssessor.identify_unfavorable_clauses(clauses)
        composite_score, composite_risk = RiskAssessor.calculate_composite_risk(clauses)
        key_risks = list(set([c.reason_for_risk for c in clauses if c.risk_level.value == "high"]))
        recommendations = RiskAssessor.get_risk_recommendations(clauses)
        
        # Step 7: Check compliance
        logger.info("Checking compliance with Indian laws")
        compliance_result = ComplianceChecker.check_compliance(text, classified_type.value)
        compliance_issues = compliance_result.get('warnings', [])
        compliance_issues.extend(ComplianceChecker.check_Indian_specific_requirements(text))
        
        # Step 8: Generate summary
        logger.info("Generating summary")
        if self.use_llm and self.llm:
            try:
                summary = self.llm.generate_summary(text[:3000], classified_type.value)
            except Exception as e:
                logger.warning(f"LLM summary generation failed: {e}")
                summary = self._generate_fallback_summary(classified_type, clauses)
        else:
            summary = self._generate_fallback_summary(classified_type, clauses)
        
        # Create metadata
        metadata = ContractMetadata(
            contract_type=classified_type,
            language=detected_language,
            parties=specific_info['parties'],
            effective_date=specific_info['dates'][0] if specific_info['dates'] else None,
            jurisdiction=specific_info['jurisdictions'][0] if specific_info['jurisdictions'] else None,
            financial_amount=specific_info['amounts'][0] if specific_info['amounts'] else None,
            file_name=file_info['file_name'],
            file_size=file_info['file_size'],
            processed_at=datetime.now()
        )
        
        # Create complete analysis
        analysis = ContractAnalysis(
            contract_id=contract_id,
            metadata=metadata,
            summary=summary,
            clauses=clauses,
            composite_risk_score=composite_score,
            composite_risk_level=composite_risk,
            key_risks=key_risks,
            compliance_issues=compliance_issues,
            unfavorable_clauses=unfavorable_ids,
            recommendations=recommendations,
            audit_trail_id=str(uuid.uuid4()),
            analysis_timestamp=datetime.now()
        )
        
        logger.info(f"Analysis complete for contract {contract_id}")
        return analysis
    
    @staticmethod
    def _generate_fallback_summary(contract_type: ContractType, clauses: list) -> str:
        """Generate summary without LLM"""
        high_risk_count = len([c for c in clauses if c.risk_level.value == "high"])
        return (
            f"This is a {contract_type.value} contract with {len(clauses)} clauses. "
            f"Risk assessment identified {high_risk_count} high-risk clauses. "
            f"Review the detailed analysis for specific concerns and recommendations."
        )
