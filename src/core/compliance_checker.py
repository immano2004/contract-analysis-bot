"""
Compliance checker for Indian legal standards
"""
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class ComplianceChecker:
    """Check contract compliance with Indian laws"""
    
    # Indian law compliance indicators
    COMPLIANCE_RULES = {
        'employment': {
            'minimum_wage': 'Contract should specify minimum wage as per state minimum wage act',
            'working_hours': 'Working hours should comply with Factories Act (max 48 hours/week)',
            'overtime_pay': 'Overtime compensation should be at 2x regular rate',
            'leave_policy': 'At least 20 days annual leave as per law',
            'gratuity': 'Gratuity clause for employees with 5+ years service',
            'pf_esi': 'Provident Fund and ESI contributions if applicable',
        },
        'vendor': {
            'quality_standards': 'Quality standards should be clearly defined',
            'payment_terms': 'Payment terms should be reasonable (typically 30-60 days)',
            'dispute_resolution': 'Should have dispute resolution mechanism',
            'termination_notice': 'Should provide reasonable notice period for termination',
        },
        'lease': {
            'rent_increase': 'Rent increase clause should be reasonable and periodic',
            'maintenance_responsibility': 'Landlord responsibility for major repairs',
            'security_deposit': 'Security deposit should not exceed 10 months rent',
            'lease_duration': 'Minimum lease period recommendations',
            'eviction_notice': 'Notice period for eviction should be 30-90 days',
        },
        'partnership': {
            'profit_distribution': 'Profit distribution should match equity contributions',
            'decision_making': 'Decision-making process should be clear',
            'partner_withdrawal': 'Clear procedure for partner exit',
            'dispute_resolution': 'Arbitration clause for partner disputes',
        },
        'service': {
            'scope_clarity': 'Scope of services should be clearly defined',
            'payment_terms': 'Payment should be linked to deliverables',
            'warranty_period': 'Reasonable warranty period for services',
            'liability_limits': 'Liability should be reasonable and mutual',
        }
    }
    
    @staticmethod
    def check_compliance(contract_text: str, contract_type: str) -> Dict[str, List[str]]:
        """
        Check contract compliance with Indian laws
        
        Args:
            contract_text: Contract text
            contract_type: Type of contract
            
        Returns:
            Dictionary with compliance status
        """
        text_lower = contract_text.lower()
        compliance_status = {
            'compliant': [],
            'warnings': [],
            'violations': []
        }
        
        if contract_type not in ComplianceChecker.COMPLIANCE_RULES:
            return compliance_status
        
        rules = ComplianceChecker.COMPLIANCE_RULES[contract_type]
        
        for rule_id, rule_description in rules.items():
            # Check if rule is mentioned in contract
            keywords = rule_id.replace('_', ' ').split()
            found = any(keyword in text_lower for keyword in keywords)
            
            if found:
                compliance_status['compliant'].append(rule_description)
            else:
                compliance_status['warnings'].append(f"Missing: {rule_description}")
        
        return compliance_status
    
    @staticmethod
    def check_Indian_specific_requirements(contract_text: str) -> List[str]:
        """
        Check for Indian-specific legal requirements
        
        Args:
            contract_text: Contract text
            
        Returns:
            List of issues found
        """
        issues = []
        text_lower = contract_text.lower()
        
        # Check for proper jurisdiction clauses
        if 'jurisdiction' not in text_lower and 'indian law' not in text_lower:
            issues.append("⚠️ No clear Indian jurisdiction clause found")
        
        # Check for GST provisions (if applicable)
        if 'gst' not in text_lower and 'goods and services' not in text_lower:
            issues.append("⚠️ No GST clause found (may be required for service contracts)")
        
        # Check for RBI compliance (for financial contracts)
        if 'finance' in text_lower or 'loan' in text_lower:
            if 'rbi' not in text_lower:
                issues.append("⚠️ May need RBI compliance clause")
        
        # Check for data protection (Indian DPDP Act)
        if 'data' in text_lower or 'personal information' in text_lower:
            if 'data protection' not in text_lower and 'confidential' not in text_lower:
                issues.append("⚠️ May need data protection compliance clause")
        
        return issues
