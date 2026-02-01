"""
Unit tests for contract analysis modules
"""
import unittest
from src.utils.file_processor import FileProcessor
from src.utils.text_preprocessor import TextPreprocessor
from src.core.contract_classifier import ContractClassifier
from src.models.contract_models import ContractType


class TestTextPreprocessor(unittest.TestCase):
    """Test text preprocessing functions"""
    
    def test_clean_text(self):
        """Test text cleaning"""
        text = "This   is  a   test.  With   multiple   spaces."
        cleaned = TextPreprocessor.clean_text(text)
        self.assertNotIn("   ", cleaned)
        self.assertIn("test", cleaned)
    
    def test_extract_sentences(self):
        """Test sentence extraction"""
        text = "This is sentence one. This is sentence two. And this is the third."
        sentences = TextPreprocessor.extract_sentences(text)
        self.assertGreaterEqual(len(sentences), 2)
    
    def test_extract_words(self):
        """Test word extraction"""
        text = "This is a test sentence"
        words = TextPreprocessor.extract_words(text)
        self.assertGreater(len(words), 0)
        self.assertIn("test", words)
    
    def test_detect_language_english(self):
        """Test English language detection"""
        text = "This is an English contract agreement with multiple clauses."
        lang = TextPreprocessor.detect_language(text)
        self.assertEqual(lang, 'en')
    
    def test_extract_section_numbers(self):
        """Test section number extraction"""
        text = """
        1. Introduction
        1.1 Purpose
        2. Terms and Conditions
        """
        sections = TextPreprocessor.extract_section_numbers(text)
        self.assertGreater(len(sections), 0)


class TestContractClassifier(unittest.TestCase):
    """Test contract classification"""
    
    def test_employment_classification(self):
        """Test employment contract classification"""
        text = """
        EMPLOYMENT AGREEMENT
        This agreement is between Employer and Employee.
        Employee's salary is Rs. 50,000 per month.
        Employee will work 48 hours per week.
        Benefits include health insurance and annual leave.
        """
        contract_type, confidence = ContractClassifier.classify(text)
        self.assertEqual(contract_type, ContractType.EMPLOYMENT)
        self.assertGreater(confidence, 0.5)
    
    def test_vendor_classification(self):
        """Test vendor contract classification"""
        text = """
        VENDOR AGREEMENT
        Vendor will supply goods as per purchase order.
        Quality must meet specified standards.
        Payment terms are 30 days from invoice date.
        Delivery schedule as per agreement.
        """
        contract_type, confidence = ContractClassifier.classify(text)
        self.assertEqual(contract_type, ContractType.VENDOR)
        self.assertGreater(confidence, 0.5)
    
    def test_service_classification(self):
        """Test service contract classification"""
        text = """
        SERVICE AGREEMENT
        Service Provider will deliver services as per scope of work.
        Payment is Rs. 1,00,000 for the project.
        Timeline is 3 months from start date.
        Deliverables include final report and support.
        """
        contract_type, confidence = ContractClassifier.classify(text)
        self.assertEqual(contract_type, ContractType.SERVICE)
        self.assertGreater(confidence, 0.3)


class TestRiskAssessment(unittest.TestCase):
    """Test risk assessment functions"""
    
    def test_high_risk_detection(self):
        """Test high-risk clause detection"""
        from src.core.risk_assessor import RiskAssessor
        
        text = "The Company may terminate this agreement without cause at any time."
        risk_level, score, reason = RiskAssessor.assess_clause_risk(text)
        self.assertGreaterEqual(score, 40)
    
    def test_low_risk_detection(self):
        """Test low-risk clause detection"""
        from src.core.risk_assessor import RiskAssessor
        
        text = "Both parties agree to perform their obligations under this agreement."
        risk_level, score, reason = RiskAssessor.assess_clause_risk(text)
        self.assertLess(score, 50)


class TestNER(unittest.TestCase):
    """Test Named Entity Recognition"""
    
    def test_extract_parties(self):
        """Test party extraction"""
        from src.core.ner_processor import NERProcessor
        
        text = "This agreement is between ABC Corporation and XYZ Services Ltd."
        parties = NERProcessor.extract_parties(text)
        self.assertGreater(len(parties), 0)


if __name__ == '__main__':
    unittest.main()
