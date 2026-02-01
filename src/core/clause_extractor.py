"""
Clause extraction and analysis module
"""
import logging
import re
from typing import List, Tuple
from src.models.contract_models import Clause, ClauseCategory, RiskLevel
from src.core.risk_assessor import RiskAssessor
from src.core.llm_analysis import analyze_clause as llm_analyze

logger = logging.getLogger(__name__)

class ClauseExtractor:
    """Extract and analyze clauses from contract text"""

    
    @staticmethod
    def extract_clauses(text: str) -> List[Clause]:
        """
        Extract clauses from contract text
        
        Args:
            text: Contract text
            
        Returns:
            List of extracted clauses
        """
        clauses = []
        
        # Split text into potential clauses
        # Look for numbered sections, headers, etc.
        clause_texts = ClauseExtractor._split_into_clauses(text)
        
        for idx, (clause_text, start_pos, end_pos) in enumerate(clause_texts):
            clause_id = f"clause_{idx + 1}"
            
            # Default values
            category = ClauseCategory.OTHER
            explanation = None
            alternative = None

            # Try LLM analysis (safe fallback on any error)
            try:
                llm_result = llm_analyze(clause_text)
                if isinstance(llm_result, dict):
                    # Map type -> ClauseCategory if possible
                    t = llm_result.get('type') or llm_result.get('category')
                    if isinstance(t, str):
                        t_norm = t.strip().lower()
                        # Match to known ClauseCategory values
                        try:
                            category = ClauseCategory(t_norm) if t_norm in [c.value for c in ClauseCategory] else ClauseCategory.OTHER
                        except Exception:
                            category = ClauseCategory.OTHER

                    # Map risk -> RiskLevel if provided
                    r = llm_result.get('risk')
                    try:
                        risk_level = RiskLevel(r.strip().lower()) if isinstance(r, str) and r.strip().lower() in [x.value for x in RiskLevel] else None
                    except Exception:
                        risk_level = None

                    explanation = llm_result.get('explanation')
                    alternative = llm_result.get('suggestion')
                else:
                    llm_result = None
            except Exception as e:
                logger.debug("LLM analysis skipped or failed for clause %s: %s", clause_id, e)
                llm_result = None

            # Assess numeric risk using existing heuristics; prefer LLM risk level if available
            assessed_risk_level, risk_score, reason = RiskAssessor.assess_clause_risk(clause_text, category)
            if 'risk_level' in locals() and risk_level is not None:
                # Use LLM-provided categorical risk but keep numeric score
                risk_level = risk_level
            else:
                risk_level = assessed_risk_level
            
            # Extract title if available
            title = ClauseExtractor._extract_clause_title(clause_text)
            
            # Generate plain language explanation
            explanation = ClauseExtractor._generate_explanation(clause_text, category)
            
            # Suggest alternative if needed
            alternative = ClauseExtractor._suggest_alternative(clause_text, risk_level)
            
            clause = Clause(
                clause_id=clause_id,
                title=title,
                text=clause_text,
                start_position=start_pos,
                end_position=end_pos,
                category=category,
                risk_level=risk_level,
                risk_score=risk_score,
                reason_for_risk=reason,
                plain_language_explanation=explanation,
                suggested_alternative=alternative,
            )
            
            clauses.append(clause)
        
        return clauses
    
    @staticmethod
    def _split_into_clauses(text: str) -> List[Tuple[str, int, int]]:
        """
        Split contract text into individual clauses
        
        Returns:
            List of tuples (clause_text, start_position, end_position)
        """
        clauses = []
        
        # Pattern for numbered clauses (1. 2. 1.1, etc.)
        clause_pattern = r'(?:^|\n)\s*(?:Article|Section|Clause|Article\s+\(|Section\s+\()?(\d+(?:\.\d+)*)\s*[.)]\s*([^\n])'
        
        matches = list(re.finditer(clause_pattern, text, re.MULTILINE))
        
        if not matches:
            # If no numbered clauses found, treat entire text as one clause
            return [(text, 0, len(text))]
        
        for i, match in enumerate(matches):
            start = match.start()
            
            # End position is the start of next clause or end of text
            if i < len(matches) - 1:
                end = matches[i + 1].start()
            else:
                end = len(text)
            
            clause_text = text[start:end].strip()
            if clause_text:
                clauses.append((clause_text, start, end))
        
        return clauses
    
    @staticmethod
    def _extract_clause_title(clause_text: str) -> str:
        """Extract title from clause text"""
        # Try to find a title in the first line
        first_line = clause_text.split('\n')[0]
        
        # Remove numbering
        title = re.sub(r'^\s*\d+(?:\.\d+)*\s*[.)]\s*', '', first_line)
        
        # Clean up
        title = title.strip()
        
        # Limit length
        if len(title) > 100:
            title = title[:97] + "..."
        
        return title if title else None
    
    @staticmethod
    def _generate_explanation(clause_text: str, category: ClauseCategory) -> str:
        """
        Generate plain language explanation of a clause
        
        Args:
            clause_text: The clause text
            category: Clause category
            
        Returns:
            Plain language explanation
        """
        explanations = {
            ClauseCategory.OBLIGATION: "This clause describes what you are required to do under the contract.",
            ClauseCategory.RIGHT: "This clause describes rights you have under the contract.",
            ClauseCategory.PROHIBITION: "This clause describes what you are not allowed to do.",
            ClauseCategory.PENALTY: "This clause describes what happens if the contract is breached.",
            ClauseCategory.INDEMNITY: "This clause describes how one party may need to compensate the other for losses.",
            ClauseCategory.TERMINATION: "This clause describes how the contract can be ended.",
            ClauseCategory.ARBITRATION: "This clause describes how disputes will be resolved.",
            ClauseCategory.CONFIDENTIALITY: "This clause describes how confidential information should be protected.",
            ClauseCategory.IP_OWNERSHIP: "This clause describes who owns intellectual property created under this contract.",
            ClauseCategory.OTHER: "This clause contains important contract terms.",
        }
        
        base_explanation = explanations.get(category, explanations[ClauseCategory.OTHER])
        
        # Add specific details from the clause
        if category == ClauseCategory.PENALTY:
            # Look for amounts
            amounts = re.findall(r'(?:Rs\.?|₹|USD|\$)\s*(\d+(?:,\d{3})*(?:\.\d{2})?)', clause_text)
            if amounts:
                base_explanation += f" The penalty amount may be {amounts[0]}."
        
        return base_explanation
    
    @staticmethod
    def _suggest_alternative(clause_text: str, risk_level: RiskLevel) -> str:
        """
        Suggest alternative language for high-risk clauses
        
        Args:
            clause_text: The clause text
            risk_level: Risk level of the clause
            
        Returns:
            Suggested alternative text or None
        """
        if risk_level != RiskLevel.HIGH:
            return None
        
        # Suggest alternatives for common high-risk patterns
        alternatives = {}
        
        if re.search(r'unlimited.*liability', clause_text.lower()):
            alternatives['unlimited_liability'] = (
                "Consider negotiating: 'Liability shall be limited to direct damages not exceeding "
                "the fees paid in the preceding 12 months.'"
            )
        
        if re.search(r'terminate.*without.*cause|terminate.*at.*will', clause_text.lower()):
            alternatives['unilateral_termination'] = (
                "Consider negotiating: 'Either party may terminate with 30 days written notice "
                "and payment of accrued fees.'"
            )
        
        if re.search(r'non.?compete', clause_text.lower()):
            alternatives['non_compete'] = (
                "Consider negotiating scope and duration: 'Non-compete shall apply only within "
                "the same industry for a period of 1 year after termination and limited to the "
                "geographic area of operations.'"
            )
        
        if alternatives:
            return list(alternatives.values())[0]
        
        return None
