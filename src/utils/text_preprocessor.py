"""
Text preprocessing utilities
"""
import re
import logging
from typing import List, Tuple
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

logger = logging.getLogger(__name__)

# Download required NLTK data (comment out after first run)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class TextPreprocessor:
    """Handle text preprocessing and cleaning"""
    
    # Common contract-related abbreviations
    ABBREVIATIONS = {
        'Ltd.': 'Limited',
        'Inc.': 'Incorporated',
        'Corp.': 'Corporation',
        'Co.': 'Company',
        'Pvt.': 'Private',
        'Govt.': 'Government',
        'Sec.': 'Section',
        'Art.': 'Article',
        'Para.': 'Paragraph',
        'pp.': 'pages',
        'etc.': 'et cetera',
    }
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove control characters
        text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
        
        # Fix common OCR errors
        text = re.sub(r'(?<=[a-z])\s+(?=[A-Z])', '', text)  # Remove space before capitalized letter in middle of sentence
        
        return text.strip()
    
    @staticmethod
    def extract_sentences(text: str) -> List[str]:
        """
        Extract sentences from text
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of sentences
        """
        try:
            return sent_tokenize(text)
        except Exception as e:
            logger.warning(f"Error in sentence tokenization: {e}")
            # Fallback to simple split
            return [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    
    @staticmethod
    def extract_words(text: str, remove_stopwords: bool = False) -> List[str]:
        """
        Extract words from text
        
        Args:
            text: Text to tokenize
            remove_stopwords: Whether to remove English stopwords
            
        Returns:
            List of words
        """
        try:
            words = word_tokenize(text.lower())
            words = [w for w in words if w.isalnum() or w in ['-', '_', '.']]
            
            if remove_stopwords:
                stop_words = set(stopwords.words('english'))
                words = [w for w in words if w not in stop_words]
            
            return words
        except Exception as e:
            logger.warning(f"Error in word tokenization: {e}")
            return text.lower().split()
    
    @staticmethod
    def expand_abbreviations(text: str) -> str:
        """
        Expand common abbreviations in contract text
        
        Args:
            text: Text with abbreviations
            
        Returns:
            Text with expanded abbreviations
        """
        for abbr, full in TextPreprocessor.ABBREVIATIONS.items():
            # Case-insensitive replacement
            pattern = re.compile(re.escape(abbr), re.IGNORECASE)
            text = pattern.sub(full, text)
        
        return text
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize whitespace and newlines"""
        # Replace multiple newlines with single newline
        text = re.sub(r'\n\s*\n', '\n', text)
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        return text.strip()
    
    @staticmethod
    def extract_section_numbers(text: str) -> List[Tuple[str, int, int]]:
        """
        Extract section/clause numbers and their positions
        
        Args:
            text: Text containing sections
            
        Returns:
            List of tuples (section_number, start_pos, end_pos)
        """
        # Match patterns like "1.", "1.1", "Article 1", "Section 1", etc.
        patterns = [
            r'\s*(?:Article|Section|Art\.|Sec\.)\s+(\d+(?:\.\d+)*)',
            r'^\s*(\d+(?:\.\d+)*)\s*[.)]',
            r'^\s*\((\d+)\)',
        ]
        
        sections = []
        for pattern in patterns:
            for match in re.finditer(pattern, text, re.MULTILINE):
                sections.append((match.group(1), match.start(), match.end()))
        
        return sorted(sections, key=lambda x: x[1])
    
    @staticmethod
    def detect_language(text: str) -> str:
        """
        Simple language detection based on character patterns
        
        Args:
            text: Text to detect language for
            
        Returns:
            'en' for English or 'hi' for Hindi
        """
        # Check for Devanagari script (used in Hindi)
        devanagari_count = sum(1 for char in text if '\u0900' <= char <= '\u097F')
        total_chars = len([char for char in text if char.isalpha()])
        
        if total_chars > 0 and (devanagari_count / total_chars) > 0.3:
            return 'hi'
        return 'en'
    
    @staticmethod
    def extract_key_terms(text: str, num_terms: int = 10) -> List[str]:
        """
        Extract key terms from text using simple frequency analysis
        
        Args:
            text: Text to extract terms from
            num_terms: Number of terms to extract
            
        Returns:
            List of key terms
        """
        words = TextPreprocessor.extract_words(text, remove_stopwords=True)
        
        # Filter short words and numbers
        words = [w for w in words if len(w) > 3 and not w.isdigit()]
        
        # Count frequency
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, _ in sorted_words[:num_terms]]
