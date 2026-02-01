"""
NER processor for extracting named entities from contracts
"""
import logging
import re
from typing import List
import spacy
from spacy.tokens import Doc
from src.models.contract_models import NamedEntity

logger = logging.getLogger(__name__)

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.warning("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
    nlp = None


class NERProcessor:
    """Extract named entities from contract text"""
    
    # Custom patterns for contract-specific entities
    AMOUNT_PATTERNS = [
        r'(?:Rs\.?|INR|₹)\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'(?:USD|$|USD\$)\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        r'(?:Amount|Amount payable|Total|Sum)\s*(?:of|to)?\s*(?:Rs\.?|INR|₹|USD|$)?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
    ]
    
    DATE_PATTERNS = [
        r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
        r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',
        r'(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2}),?\s+(\d{4})',
    ]
    
    # Entity types
    ENTITY_TYPES = {
        'PERSON': 'PERSON',
        'ORG': 'ORG',
        'DATE': 'DATE',
        'MONEY': 'MONEY',
        'GPE': 'GPE',
        'LOCATION': 'LOCATION',
        'JURISDICTION': 'GPE',
        'LIABILITY': 'LIABILITY',
        'DURATION': 'DURATION',
    }
    
    @staticmethod
    def extract_entities(text: str) -> List[NamedEntity]:
        """
        Extract all named entities from text
        
        Args:
            text: Contract text
            
        Returns:
            List of extracted entities
        """
        entities = []
        
        # Use spaCy if available
        if nlp:
            try:
                doc = nlp(text)
                for ent in doc.ents:
                    entity = NamedEntity(
                        text=ent.text,
                        entity_type=ent.label_,
                        start_char=ent.start_char,
                        end_char=ent.end_char
                    )
                    entities.append(entity)
            except Exception as e:
                logger.warning(f"Error in spaCy NER: {e}")
        
        # Add pattern-based extractions
        pattern_entities = NERProcessor._extract_by_patterns(text)
        entities.extend(pattern_entities)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_entities = []
        for entity in entities:
            key = (entity.text.lower(), entity.entity_type)
            if key not in seen:
                seen.add(key)
                unique_entities.append(entity)
        
        return unique_entities
    
    @staticmethod
    def _extract_by_patterns(text: str) -> List[NamedEntity]:
        """Extract entities using regex patterns"""
        entities = []
        
        # Extract amounts
        for pattern in NERProcessor.AMOUNT_PATTERNS:
            for match in re.finditer(pattern, text):
                entity = NamedEntity(
                    text=match.group(0),
                    entity_type='MONEY',
                    start_char=match.start(),
                    end_char=match.end()
                )
                entities.append(entity)
        
        # Extract dates
        for pattern in NERProcessor.DATE_PATTERNS:
            for match in re.finditer(pattern, text):
                entity = NamedEntity(
                    text=match.group(0),
                    entity_type='DATE',
                    start_char=match.start(),
                    end_char=match.end()
                )
                entities.append(entity)
        
        # Extract jurisdictions (common Indian states and countries)
        jurisdictions = ['India', 'Delhi', 'Mumbai', 'Bangalore', 'Pune', 'Hyderabad',
                        'India', 'United States', 'UK', 'US', 'England', 'New York']
        for jurisdiction in jurisdictions:
            pattern = r'\b' + re.escape(jurisdiction) + r'\b'
            for match in re.finditer(pattern, text):
                entity = NamedEntity(
                    text=match.group(0),
                    entity_type='JURISDICTION',
                    start_char=match.start(),
                    end_char=match.end()
                )
                entities.append(entity)
        
        # Extract durations
        duration_patterns = [
            r'(\d+)\s*(year|month|week|day|years|months|weeks|days)',
            r'(one|two|three|four|five|six|seven|eight|nine|ten)\s+(year|month|week|day|years|months|weeks|days)',
        ]
        for pattern in duration_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entity = NamedEntity(
                    text=match.group(0),
                    entity_type='DURATION',
                    start_char=match.start(),
                    end_char=match.end()
                )
                entities.append(entity)
        
        return entities
    
    @staticmethod
    def extract_parties(text: str) -> List[str]:
        """
        Extract party names from contract
        
        Args:
            text: Contract text
            
        Returns:
            List of party names
        """
        parties = []
        
        if not nlp:
            return parties
        
        try:
            doc = nlp(text)
            
            # Extract organizations
            for ent in doc.ents:
                if ent.label_ in ['ORG', 'PERSON']:
                    parties.append(ent.text)
            
            # Look for "between" and "and" patterns
            between_pattern = r'between\s+([^,]+)\s+and\s+([^,]+?)(?:\s+of|\s+located|\s+having|,|\.|where)'
            for match in re.finditer(between_pattern, text[:500], re.IGNORECASE):
                parties.extend([match.group(1).strip(), match.group(2).strip()])
            
            # Remove duplicates while preserving order
            seen = set()
            unique_parties = []
            for party in parties:
                if party.lower() not in seen:
                    seen.add(party.lower())
                    unique_parties.append(party)
            
            return unique_parties[:2]  # Usually only 2 main parties
        
        except Exception as e:
            logger.warning(f"Error extracting parties: {e}")
            return parties
    
    @staticmethod
    def extract_specific_info(text: str) -> dict:
        """
        Extract specific contract information
        
        Args:
            text: Contract text
            
        Returns:
            Dictionary with extracted information
        """
        info = {
            'parties': NERProcessor.extract_parties(text),
            'dates': [],
            'amounts': [],
            'jurisdictions': [],
            'entities': NERProcessor.extract_entities(text)
        }
        
        # Extract dates
        for entity in info['entities']:
            if entity.entity_type == 'DATE':
                if entity.text not in info['dates']:
                    info['dates'].append(entity.text)
        
        # Extract amounts
        for entity in info['entities']:
            if entity.entity_type == 'MONEY':
                if entity.text not in info['amounts']:
                    info['amounts'].append(entity.text)
        
        # Extract jurisdictions
        for entity in info['entities']:
            if entity.entity_type == 'JURISDICTION':
                if entity.text not in info['jurisdictions']:
                    info['jurisdictions'].append(entity.text)
        
        return info
