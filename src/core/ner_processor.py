"""
Lightweight NER processor for contracts (Regex-based only)
Cloud safe • No spaCy • No heavy ML
"""

import logging
import re
from typing import List
from src.models.contract_models import NamedEntity

logger = logging.getLogger(__name__)


class NERProcessor:
    """Extract named entities using rule-based patterns only"""

    # -----------------------------
    # MONEY
    # -----------------------------
    AMOUNT_PATTERNS = [
        r'(?:Rs\.?|INR|₹)\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?',
        r'(?:USD|\$)\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?',
    ]

    # -----------------------------
    # DATE
    # -----------------------------
    DATE_PATTERNS = [
        r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',
        r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}',
    ]

    # -----------------------------
    # JURISDICTIONS
    # -----------------------------
    JURISDICTIONS = [
        "India", "Delhi", "Mumbai", "Bangalore", "Pune",
        "Hyderabad", "United States", "UK", "England", "New York"
    ]

    # -----------------------------
    # DURATION
    # -----------------------------
    DURATION_PATTERNS = [
        r'\d+\s*(?:year|month|week|day|years|months|weeks|days)',
    ]

    # -----------------------------
    # ORGANIZATIONS (party names)
    # -----------------------------
    ORG_PATTERN = r'\b[A-Z][A-Za-z &,.]*(?:Ltd|Limited|LLP|Inc|Corporation|Corp|Pvt|Private)\b'

    BETWEEN_PATTERN = r'between\s+([A-Z][A-Za-z &,.]+?)\s+and\s+([A-Z][A-Za-z &,.]+)'


    # =====================================================
    # MAIN ENTITY EXTRACTION
    # =====================================================
    @staticmethod
    def extract_entities(text: str) -> List[NamedEntity]:

        entities = []

        def add_entities(patterns, label):
            for pattern in patterns:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    entities.append(
                        NamedEntity(
                            text=match.group(0),
                            entity_type=label,
                            start_char=match.start(),
                            end_char=match.end(),
                        )
                    )

        add_entities(NERProcessor.AMOUNT_PATTERNS, "MONEY")
        add_entities(NERProcessor.DATE_PATTERNS, "DATE")
        add_entities(NERProcessor.DURATION_PATTERNS, "DURATION")

        # jurisdictions
        for place in NERProcessor.JURISDICTIONS:
            for match in re.finditer(r'\b' + re.escape(place) + r'\b', text):
                entities.append(
                    NamedEntity(
                        text=match.group(0),
                        entity_type="JURISDICTION",
                        start_char=match.start(),
                        end_char=match.end(),
                    )
                )

        # organizations
        for match in re.finditer(NERProcessor.ORG_PATTERN, text):
            entities.append(
                NamedEntity(
                    text=match.group(0),
                    entity_type="ORG",
                    start_char=match.start(),
                    end_char=match.end(),
                )
            )

        # remove duplicates
        seen = set()
        unique = []
        for e in entities:
            key = (e.text.lower(), e.entity_type)
            if key not in seen:
                seen.add(key)
                unique.append(e)

        return unique


    # =====================================================
    # PARTY EXTRACTION
    # =====================================================
    @staticmethod
    def extract_parties(text: str) -> List[str]:

        parties = []

        # Between X and Y
        for match in re.finditer(NERProcessor.BETWEEN_PATTERN, text[:500], re.IGNORECASE):
            parties.extend([match.group(1).strip(), match.group(2).strip()])

        # company names
        for match in re.findall(NERProcessor.ORG_PATTERN, text):
            parties.append(match.strip())

        # unique
        seen = set()
        unique = []
        for p in parties:
            if p.lower() not in seen:
                seen.add(p.lower())
                unique.append(p)

        return unique[:2]


    # =====================================================
    # SPECIFIC INFO
    # =====================================================
    @staticmethod
    def extract_specific_info(text: str) -> dict:

        entities = NERProcessor.extract_entities(text)

        return {
            "parties": NERProcessor.extract_parties(text),
            "dates": [e.text for e in entities if e.entity_type == "DATE"],
            "amounts": [e.text for e in entities if e.entity_type == "MONEY"],
            "jurisdictions": [e.text for e in entities if e.entity_type == "JURISDICTION"],
            "entities": entities,
        }
