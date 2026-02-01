"""
Contract type classification module
"""
import logging
from typing import Dict, Tuple
from src.models.contract_models import ContractType
import re

logger = logging.getLogger(__name__)


class ContractClassifier:
    """Classify contract types based on content analysis"""
    
    # Keywords associated with each contract type
    KEYWORDS = {
        ContractType.EMPLOYMENT: {
            'primary': ['employment', 'employee', 'employer', 'salary', 'wages', 'compensation', 
                       'benefits', 'termination', 'performance', 'probation', 'notice period',
                       'job description', 'hours of work', 'leave', 'overtime', 'redundancy'],
            'secondary': ['confidentiality', 'non-compete', 'intellectual property', 'training'],
        },
        ContractType.VENDOR: {
            'primary': ['vendor', 'supplier', 'goods', 'services', 'purchase', 'supply',
                       'delivery', 'quality', 'price', 'payment terms', 'invoice', 'warranty',
                       'guarantee', 'defects', 'liability', 'purchase order'],
            'secondary': ['inspection', 'acceptance', 'rejection', 'replacement'],
        },
        ContractType.LEASE: {
            'primary': ['lease', 'lessor', 'lessee', 'tenant', 'landlord', 'rent', 'rental',
                       'property', 'premises', 'security deposit', 'maintenance', 'repairs',
                       'utilities', 'eviction', 'breach', 'assignment', 'sublease'],
            'secondary': ['use of property', 'permitted use', 'alterations'],
        },
        ContractType.PARTNERSHIP: {
            'primary': ['partnership', 'partners', 'partner', 'equity', 'profit', 'distribution',
                       'contribution', 'capital', 'unanimous consent', 'dissolution', 'withdrawal',
                       'buy-out', 'non-compete', 'goodwill', 'partnership agreement'],
            'secondary': ['joint venture', 'management', 'decision making'],
        },
        ContractType.SERVICE: {
            'primary': ['services', 'service provider', 'client', 'consultant', 'contractor',
                       'deliverables', 'payment', 'scope of work', 'timeline', 'milestone',
                       'acceptance', 'warranty', 'support', 'maintenance', 'terms of service'],
            'secondary': ['professional', 'expertise', 'quality assurance'],
        },
    }
    
    @staticmethod
    def classify(text: str) -> Tuple[ContractType, float]:
        """
        Classify contract type based on content
        
        Args:
            text: Contract text to classify
            
        Returns:
            Tuple of (contract_type, confidence_score)
        """
        text_lower = text.lower()
        scores = {}
        
        # Calculate scores for each contract type
        for contract_type, keywords in ContractClassifier.KEYWORDS.items():
            primary_score = ContractClassifier._count_keyword_matches(
                text_lower, keywords['primary'], multiplier=2
            )
            secondary_score = ContractClassifier._count_keyword_matches(
                text_lower, keywords['secondary'], multiplier=1
            )
            
            scores[contract_type] = primary_score + secondary_score
        
        # Find the contract type with highest score
        if not scores or max(scores.values()) == 0:
            return ContractType.OTHER, 0.0
        
        best_type = max(scores, key=scores.get)
        best_score = scores[best_type]
        
        # Normalize confidence score to 0-1 range using per-type maximum possible score
        primary_count = len(keywords['primary'])
        secondary_count = len(keywords['secondary'])
        max_possible = (primary_count * 2) + (secondary_count * 1)
        # Small positive smoothing to avoid borderline cases
        confidence = min((best_score / max_possible if max_possible > 0 else 0.0) * 1.05, 1.0)
        
        return best_type, confidence
    
    @staticmethod
    def _count_keyword_matches(text: str, keywords: list, multiplier: int = 1) -> float:
        """
        Count matches for keywords in text
        
        Args:
            text: Text to search in
            keywords: List of keywords to find
            multiplier: Score multiplier for this keyword group
            
        Returns:
            Total score
        """
        score = 0
        for keyword in keywords:
            # Use word boundary regex for exact word matches
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = len(re.findall(pattern, text))
            score += matches * multiplier
        
        return score
    
    @staticmethod
    def classify_with_reasoning(text: str) -> Dict:
        """
        Classify contract type with detailed reasoning
        
        Args:
            text: Contract text to classify
            
        Returns:
            Dictionary with classification details
        """
        contract_type, confidence = ContractClassifier.classify(text)
        
        # Find which keywords were matched
        text_lower = text.lower()
        matched_keywords = []
        
        if contract_type != ContractType.OTHER:
            keywords = ContractClassifier.KEYWORDS[contract_type]['primary']
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text_lower):
                    matched_keywords.append(keyword)
        
        return {
            'contract_type': contract_type.value,
            'confidence': confidence,
            'matched_keywords': matched_keywords[:5],  # Top 5 keywords
            'reasoning': f"Contract classified as {contract_type.value} based on keyword analysis"
        }
