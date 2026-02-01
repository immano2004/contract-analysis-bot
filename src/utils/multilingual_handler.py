"""
Multilingual handler for contract analysis
"""
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class MultilingualHandler:
    """Handle multilingual contracts"""
    
    # Hindi to English translation dictionary (common legal terms)
    HINDI_TO_ENGLISH_LEGAL = {
        'अनुबंध': 'contract',
        'पक्ष': 'party',
        'शर्त': 'clause',
        'दायित्व': 'liability',
        'दंड': 'penalty',
        'समाप्त': 'terminate',
        'गोपनीय': 'confidential',
        'मुनाफा': 'profit',
        'पारिश्रमिक': 'compensation',
        'कार्यकाल': 'tenure',
    }
    
    @staticmethod
    def detect_language(text: str) -> str:
        """
        Detect if text is in English or Hindi
        
        Args:
            text: Input text
            
        Returns:
            'en' or 'hi'
        """
        # Count Devanagari characters (Hindi script)
        devanagari_count = sum(1 for char in text if '\u0900' <= char <= '\u097F')
        latin_count = sum(1 for char in text if ord(char) < 128)
        
        if devanagari_count > 0 and devanagari_count > latin_count:
            return 'hi'
        return 'en'
    
    @staticmethod
    def translate_hindi_to_english(text: str) -> str:
        """
        Simple translation of Hindi legal terms to English
        
        Args:
            text: Hindi text
            
        Returns:
            Text with Hindi terms replaced by English equivalents
        """
        import re
        
        for hindi_term, english_term in MultilingualHandler.HINDI_TO_ENGLISH_LEGAL.items():
            # Case-insensitive replacement
            pattern = re.compile(re.escape(hindi_term), re.IGNORECASE)
            text = pattern.sub(english_term, text)
        
        return text
    
    @staticmethod
    def normalize_contract_text(text: str) -> Tuple[str, str]:
        """
        Normalize contract text and detect language
        
        Args:
            text: Raw contract text
            
        Returns:
            Tuple of (normalized_text, language)
        """
        language = MultilingualHandler.detect_language(text)
        
        if language == 'hi':
            # For Hindi text, we keep it as-is but could translate if needed
            # For now, just return with language marker
            pass
        
        return text, language
