"""
Example Usage Patterns
Demonstrates how to use the Contract Analysis Bot programmatically
"""

# Example 1: Basic Contract Analysis
# ===================================
def example_basic_analysis():
    """Analyze a contract using the main engine"""
    from src.contract_engine import ContractAnalysisEngine
    
    # Initialize engine
    engine = ContractAnalysisEngine(use_llm=True, llm_provider="claude")
    
    # Analyze contract
    analysis = engine.analyze_contract("path/to/employment_contract.pdf")
    
    # Print results
    print(f"Contract Type: {analysis.metadata.contract_type.value}")
    print(f"Composite Risk Score: {analysis.composite_risk_score}/100")
    print(f"Risk Level: {analysis.composite_risk_level.value}")
    print(f"\nSummary:\n{analysis.summary}")
    
    # Print key risks
    if analysis.key_risks:
        print("\nKey Risks:")
        for risk in analysis.key_risks:
            print(f"  • {risk}")
    
    # Print recommendations
    if analysis.recommendations:
        print("\nRecommendations:")
        for rec in analysis.recommendations:
            print(f"  ✓ {rec}")


# Example 2: Detailed Clause Analysis
# ====================================
def example_detailed_clause_analysis():
    """Analyze individual clauses in detail"""
    from src.contract_engine import ContractAnalysisEngine
    
    engine = ContractAnalysisEngine()
    analysis = engine.analyze_contract("vendor_contract.pdf")
    
    # Filter high-risk clauses
    high_risk_clauses = [c for c in analysis.clauses if c.risk_level.value == "high"]
    
    print(f"Found {len(high_risk_clauses)} high-risk clauses:\n")
    
    for clause in high_risk_clauses:
        print(f"Clause: {clause.title or clause.clause_id}")
        print(f"Category: {clause.category.value}")
        print(f"Risk Score: {clause.risk_score}/100")
        print(f"Reason: {clause.reason_for_risk}")
        print(f"Explanation: {clause.plain_language_explanation}")
        
        if clause.suggested_alternative:
            print(f"Suggested Alternative: {clause.suggested_alternative}")
        print("\n" + "-"*50 + "\n")


# Example 3: Extract Contract Information
# ========================================
def example_extract_information():
    """Extract key information from contract"""
    from src.utils.file_processor import FileProcessor
    from src.utils.text_preprocessor import TextPreprocessor
    from src.core.ner_processor import NERProcessor
    
    # Extract text
    text, file_type = FileProcessor.extract_text("partnership_deed.pdf")
    
    # Preprocess
    text = TextPreprocessor.clean_text(text)
    
    # Extract information
    info = NERProcessor.extract_specific_info(text)
    
    print("Extracted Information:")
    print(f"Parties: {', '.join(info['parties'])}")
    print(f"Dates: {', '.join(info['dates'])}")
    print(f"Amounts: {', '.join(info['amounts'])}")
    print(f"Jurisdictions: {', '.join(info['jurisdictions'])}")


# Example 4: Compliance Check
# ============================
def example_compliance_check():
    """Check compliance with Indian laws"""
    from src.utils.file_processor import FileProcessor
    from src.utils.text_preprocessor import TextPreprocessor
    from src.core.contract_classifier import ContractClassifier
    from src.core.compliance_checker import ComplianceChecker
    
    # Extract and classify
    text, _ = FileProcessor.extract_text("employment_agreement.pdf")
    text = TextPreprocessor.clean_text(text)
    contract_type, _ = ContractClassifier.classify(text)
    
    # Check compliance
    compliance = ComplianceChecker.check_compliance(text, contract_type.value)
    indian_issues = ComplianceChecker.check_Indian_specific_requirements(text)
    
    print("Compliance Status:")
    print(f"\nCompliant Items: {len(compliance['compliant'])}")
    for item in compliance['compliant']:
        print(f"  ✓ {item}")
    
    print(f"\nWarnings: {len(compliance['warnings'])}")
    for warning in compliance['warnings']:
        print(f"  ⚠️  {warning}")
    
    if indian_issues:
        print(f"\nIndian-Specific Issues: {len(indian_issues)}")
        for issue in indian_issues:
            print(f"  ⚠️  {issue}")


# Example 5: Risk Scoring
# =======================
def example_risk_scoring():
    """Detailed risk scoring analysis"""
    from src.contract_engine import ContractAnalysisEngine
    
    engine = ContractAnalysisEngine()
    analysis = engine.analyze_contract("lease_agreement.pdf")
    
    # Group clauses by risk level
    risk_breakdown = {
        'low': [],
        'medium': [],
        'high': []
    }
    
    for clause in analysis.clauses:
        risk_breakdown[clause.risk_level.value].append(clause)
    
    # Print summary
    print("Risk Score Breakdown:")
    print(f"Total Clauses: {len(analysis.clauses)}")
    print(f"Low Risk: {len(risk_breakdown['low'])} ({len(risk_breakdown['low'])/len(analysis.clauses)*100:.1f}%)")
    print(f"Medium Risk: {len(risk_breakdown['medium'])} ({len(risk_breakdown['medium'])/len(analysis.clauses)*100:.1f}%)")
    print(f"High Risk: {len(risk_breakdown['high'])} ({len(risk_breakdown['high'])/len(analysis.clauses)*100:.1f}%)")
    print(f"\nComposite Risk Score: {analysis.composite_risk_score}/100")
    print(f"Composite Risk Level: {analysis.composite_risk_level.value.upper()}")


# Example 6: Export Analysis
# ==========================
def example_export_analysis():
    """Export analysis to various formats"""
    import json
    from src.contract_engine import ContractAnalysisEngine
    from src.utils.export_handler import ExportHandler
    
    engine = ContractAnalysisEngine()
    analysis = engine.analyze_contract("service_contract.pdf")
    
    # Convert to dictionary for export
    analysis_dict = analysis.model_dump()
    
    # Export to JSON
    json_path = ExportHandler.export_to_json(analysis_dict, "contract_analysis.json")
    print(f"Exported to JSON: {json_path}")
    
    # Export to PDF (requires reportlab)
    try:
        pdf_path = ExportHandler.export_to_pdf(analysis_dict, "contract_analysis.pdf")
        print(f"Exported to PDF: {pdf_path}")
    except ImportError:
        print("PDF export requires reportlab: pip install reportlab")
    
    # Export to DOCX
    try:
        docx_path = ExportHandler.export_to_docx(analysis_dict, "contract_analysis.docx")
        print(f"Exported to DOCX: {docx_path}")
    except Exception as e:
        print(f"DOCX export error: {e}")


# Example 7: Multilingual Analysis
# ================================
def example_multilingual_analysis():
    """Analyze multilingual contracts"""
    from src.utils.file_processor import FileProcessor
    from src.utils.text_preprocessor import TextPreprocessor
    from src.utils.multilingual_handler import MultilingualHandler
    
    # Extract text
    text, _ = FileProcessor.extract_text("hindi_contract.pdf")
    
    # Detect language
    language = MultilingualHandler.detect_language(text)
    print(f"Detected Language: {language}")
    
    if language == 'hi':
        print("Hindi contract detected. Processing...")
        # The system will handle Hindi text appropriately
    
    # For analysis, you can still use the main engine
    from src.contract_engine import ContractAnalysisEngine
    engine = ContractAnalysisEngine()
    analysis = engine.analyze_contract("hindi_contract.pdf")
    print(f"Contract Type: {analysis.metadata.contract_type.value}")


# Example 8: Batch Processing
# ============================
def example_batch_processing():
    """Process multiple contracts"""
    import os
    from src.contract_engine import ContractAnalysisEngine
    
    engine = ContractAnalysisEngine()
    
    # Process all contracts in a directory
    contract_dir = "contracts/"
    results = []
    
    for filename in os.listdir(contract_dir):
        if filename.endswith(('.pdf', '.docx', '.txt')):
            file_path = os.path.join(contract_dir, filename)
            
            try:
                print(f"Analyzing {filename}...")
                analysis = engine.analyze_contract(file_path)
                results.append({
                    'file': filename,
                    'type': analysis.metadata.contract_type.value,
                    'risk_score': analysis.composite_risk_score,
                    'risk_level': analysis.composite_risk_level.value
                })
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    # Print summary
    print("\nBatch Analysis Summary:")
    print(f"Total contracts: {len(results)}")
    
    avg_risk = sum(r['risk_score'] for r in results) / len(results)
    print(f"Average Risk Score: {avg_risk:.1f}/100")
    
    for result in results:
        print(f"  {result['file']}: {result['type']} - Risk {result['risk_score']:.1f} ({result['risk_level']})")


# Example 9: Custom Risk Assessment
# ==================================
def example_custom_risk_assessment():
    """Create custom risk assessment"""
    from src.core.clause_extractor import ClauseExtractor
    from src.core.risk_assessor import RiskAssessor
    
    # Sample clause text
    clause_text = """
    The Employee may be terminated by the Company without cause at any time
    without notice or severance pay. This termination is unconditional and
    absolute at the sole discretion of the Company.
    """
    
    # Assess risk
    risk_level, score, reason = RiskAssessor.assess_clause_risk(clause_text)
    
    print(f"Risk Assessment Results:")
    print(f"Text: {clause_text[:100]}...")
    print(f"Risk Level: {risk_level.value.upper()}")
    print(f"Risk Score: {score}/100")
    print(f"Reason: {reason}")


# Example 10: Integration with Audit Trail
# ========================================
def example_audit_trail():
    """Track analysis with audit trail"""
    import json
    from datetime import datetime
    from src.contract_engine import ContractAnalysisEngine
    from src.models.contract_models import AuditLogEntry
    
    engine = ContractAnalysisEngine()
    analysis = engine.analyze_contract("contract.pdf")
    
    # Create audit log entry
    audit_entry = AuditLogEntry(
        log_id=analysis.audit_trail_id,
        contract_id=analysis.contract_id,
        action="contract_analyzed",
        timestamp=datetime.now(),
        details={
            'file_name': analysis.metadata.file_name,
            'contract_type': analysis.metadata.contract_type.value,
            'risk_score': analysis.composite_risk_score,
            'clauses_found': len(analysis.clauses)
        },
        status="success"
    )
    
    # Save audit trail
    import os
    os.makedirs('audit_logs', exist_ok=True)
    
    with open('audit_logs/audit_trail.json', 'a') as f:
        f.write(json.dumps(audit_entry.model_dump(), indent=2, default=str) + '\n')
    
    print(f"Audit log saved: {audit_entry.log_id}")


if __name__ == "__main__":
    """
    Run examples (uncomment the one you want to try)
    """
    
    # Uncomment to run examples:
    # example_basic_analysis()
    # example_detailed_clause_analysis()
    # example_extract_information()
    # example_compliance_check()
    # example_risk_scoring()
    # example_export_analysis()
    # example_multilingual_analysis()
    # example_batch_processing()
    # example_custom_risk_assessment()
    # example_audit_trail()
    
    print("Uncomment example functions to run them")
    print("See this file for detailed usage patterns")
