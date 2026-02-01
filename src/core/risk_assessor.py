"""
Risk assessment module for contract analysis
"""
import logging
from typing import List, Dict, Tuple
from src.models.contract_models import Clause, RiskLevel, ClauseCategory
import re

logger = logging.getLogger(__name__)


class RiskAssessor:
    """Assess risk levels in contract clauses"""
    
    # High-risk keywords and patterns
    HIGH_RISK_INDICATORS = {
        'unlimited_liability': [
            r'unlimited.*liability',
            r'liability.*unlimited',
            r'indemnify.*all.*damages',
            r'indemnification.*unlimited',
        ],
        'unilateral_termination': [
            r'terminate.*without.*cause',
            r'terminate.*at.*will',
            r'unilateral.*termination',
            r'immediate.*termination',
        ],
        'severe_penalties': [
            r'liquidated.*damages.*\d+',
            r'penalty.*clause',
            r'penalty.*amount',
            r'damages.*shall.*not.*be.*limited',
        ],
        'IP_transfer': [
            r'assign.*all.*intellectual.*property',
            r'transfer.*ownership.*ip',
            r'copyright.*transfer',
            r'patent.*transfer',
        ],
        'non_compete': [
            r'non.?compete',
            r'non.?solicitation',
            r'restriction.*business',
            r'post.*termination.*restriction',
        ],
        'lock_in': [
            r'lock.?in.*period',
            r'minimum.*term',
            r'lock.?in.*\d+',
            r'notice.*period.*\d+.*month',
        ],
    }
    
    # Medium-risk keywords
    MEDIUM_RISK_INDICATORS = {
        'partial_liability': [
            r'liability.*limited.*to',
            r'liability.*capped',
            r'maximum.*liability',
        ],
        'conditional_termination': [
            r'termination.*for.*cause',
            r'termination.*breach',
            r'grounds.*for.*termination',
        ],
        'dispute_resolution': [
            r'arbitration.*clause',
            r'jurisdiction.*disputes',
            r'governing.*law',
        ],
        'renewal': [
            r'auto.?renewal',
            r'automatic.*renewal',
            r'renewal.*period',
        ],
    }
    
    @staticmethod
    def assess_clause_risk(clause_text: str, clause_category: ClauseCategory = None) -> Tuple[RiskLevel, float, str]:
        """
        Assess risk level of a clause
        
        Args:
            clause_text: The clause text
            clause_category: Optional category of the clause
            
        Returns:
            Tuple of (risk_level, risk_score, reason)
        """
        text_lower = clause_text.lower()
        score = 0
        reasons = []
        
        # Check for high-risk indicators
        high_risk_count = 0
        for indicator, patterns in RiskAssessor.HIGH_RISK_INDICATORS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    high_risk_count += 1
                    reasons.append(indicator)
        
        # Check for medium-risk indicators
        medium_risk_count = 0
        for indicator, patterns in RiskAssessor.MEDIUM_RISK_INDICATORS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    medium_risk_count += 1
        
        # Calculate risk score (0-100)
        # Use stronger weighting for high-risk indicators so single critical matches register as high
        score = (high_risk_count * 40) + (medium_risk_count * 20)
        
        # Category-based adjustments
        if clause_category == ClauseCategory.PENALTY:
            score = min(score + 20, 100)
        elif clause_category == ClauseCategory.INDEMNITY:
            score = min(score + 15, 100)
        elif clause_category == ClauseCategory.TERMINATION:
            score = min(score + 10, 100)
        
        # Cap at 100
        score = min(score, 100)
        
        # Determine risk level
        if score >= 70:
            risk_level = RiskLevel.HIGH
        elif score >= 40:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        reason = " | ".join(set(reasons)) if reasons else "Standard clause"
        
        return risk_level, score, reason
    
    @staticmethod
    def identify_unfavorable_clauses(clauses: List[Clause]) -> List[str]:
        """
        Identify unfavorable clauses for one party
        
        Args:
            clauses: List of clauses to analyze
            
        Returns:
            List of clause IDs that are unfavorable
        """
        unfavorable_clause_ids = []
        
        for clause in clauses:
            if clause.risk_level == RiskLevel.HIGH:
                # Check if it's particularly unfavorable
                if any(keyword in clause.reason_for_risk.lower() if clause.reason_for_risk else '' 
                       for keyword in ['unlimited', 'unilateral', 'unreasonable', 'severe']):
                    unfavorable_clause_ids.append(clause.clause_id)
                    clause.is_unfavorable = True
        
        return unfavorable_clause_ids
    
    @staticmethod
    def calculate_composite_risk(clauses: List[Clause]) -> Tuple[float, RiskLevel]:
        """
        Calculate overall contract risk score
        
        Args:
            clauses: List of clauses
            
        Returns:
            Tuple of (composite_score, risk_level)
        """
        if not clauses:
            return 0.0, RiskLevel.LOW
        
        # Weight high-risk clauses more heavily
        weighted_sum = 0
        weights_sum = 0
        
        for clause in clauses:
            weight = 1.0
            if clause.risk_level == RiskLevel.HIGH:
                weight = 3.0
            elif clause.risk_level == RiskLevel.MEDIUM:
                weight = 1.5
            
            weighted_sum += clause.risk_score * weight
            weights_sum += weight
        
        composite_score = weighted_sum / weights_sum if weights_sum > 0 else 0
        
        # Determine overall risk level
        if composite_score >= 70:
            risk_level = RiskLevel.HIGH
        elif composite_score >= 40:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        return composite_score, risk_level
    
    @staticmethod
    def get_risk_recommendations(clauses: List[Clause]) -> List[str]:
        """
        Get recommendations based on risk analysis
        
        Args:
            clauses: List of clauses
            
        Returns:
            List of recommendations
        """
        recommendations = []
        high_risk_clauses = [c for c in clauses if c.risk_level == RiskLevel.HIGH]
        
        if high_risk_clauses:
            recommendations.append(f"Review {len(high_risk_clauses)} high-risk clauses with legal counsel")
            
            # Specific recommendations
            for clause in high_risk_clauses:
                if 'unlimited' in (clause.reason_for_risk or '').lower():
                    recommendations.append(f"Negotiate limits on liability in: {clause.title or 'Unnamed Clause'}")
                if 'unilateral' in (clause.reason_for_risk or '').lower():
                    recommendations.append(f"Seek mutual termination rights instead of unilateral terms")
                if 'non.?compete' in (clause.reason_for_risk or '').lower():
                    recommendations.append(f"Negotiate scope and duration of non-compete clause")
        
        return list(set(recommendations))  # Remove duplicates
