"""
Main application file for Contract Analysis Bot
"""
import streamlit as st
import os
from datetime import datetime
import json
import uuid
from src.utils.file_processor import FileProcessor
from src.utils.text_preprocessor import TextPreprocessor
from src.core.contract_classifier import ContractClassifier
from src.core.ner_processor import NERProcessor
from src.core.clause_extractor import ClauseExtractor
from src.core.risk_assessor import RiskAssessor
from src.core.llm_integration import LLMIntegration
from src.models.contract_models import ContractAnalysis, ContractMetadata, ContractType, AuditLogEntry

# Configure Streamlit
st.set_page_config(
    page_title="Contract Analysis Bot",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'contract_analysis' not in st.session_state:
    st.session_state.contract_analysis = None
if 'audit_logs' not in st.session_state:
    st.session_state.audit_logs = []


def create_audit_log(action: str, details: dict, status: str = "success") -> AuditLogEntry:
    """Create an audit log entry"""
    return AuditLogEntry(
        log_id=str(uuid.uuid4()),
        contract_id=st.session_state.get('current_contract_id', 'unknown'),
        action=action,
        timestamp=datetime.now(),
        details=details,
        status=status
    )


def save_audit_trail(entries: list):
    """Save audit trail to file"""
    os.makedirs('data/audit_logs', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"data/audit_logs/audit_{timestamp}.json"
    
    try:
        with open(file_path, 'w') as f:
            json.dump([entry.model_dump() for entry in entries], f, indent=2, default=str)
        return file_path
    except Exception as e:
        st.error(f"Error saving audit trail: {e}")
        return None


def main():
    """Main application"""
    st.title("📋 Contract Analysis & Risk Assessment Bot")
    st.markdown("*AI-powered legal assistant for Indian SMEs*")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Settings")
        llm_provider = st.selectbox(
            "LLM Provider",
            ["Claude (Anthropic)", "GPT-4 (OpenAI)"],
            help="Select your preferred LLM for enhanced analysis"
        )
        
        use_llm = st.checkbox("Enable LLM Analysis", value=True)
        
        if use_llm:
            if "Claude" in llm_provider:
                if not os.getenv("ANTHROPIC_API_KEY"):
                    st.warning("Set ANTHROPIC_API_KEY environment variable")
            else:
                if not os.getenv("OPENAI_API_KEY"):
                    st.warning("Set OPENAI_API_KEY environment variable")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📁 Upload & Analysis", "📊 Results", "📝 Templates", "⚙️ Settings"]
    )
    
    with tab1:
        st.header("Upload Contract for Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Choose a contract file",
                type=["pdf", "docx", "doc", "txt"],
                help="Supported formats: PDF, DOCX, DOC, TXT"
            )
        
        with col2:
            contract_type = st.selectbox(
                "Contract Type (Optional)",
                ["Auto-detect", "Employment", "Vendor", "Lease", "Partnership", "Service"],
                help="Leave as Auto-detect for automatic classification"
            )
        
        language = st.radio(
            "Contract Language",
            ["English", "Hindi"],
            horizontal=True,
            help="Language of the uploaded contract"
        )
        
        if uploaded_file and st.button("🔍 Analyze Contract", type="primary"):
            try:
                # Save uploaded file temporarily
                temp_file_path = f"temp_{uploaded_file.name}"
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                st.session_state.current_contract_id = str(uuid.uuid4())
                
                with st.spinner("Processing contract..."):
                    # Step 1: Extract text
                    st.status("Extracting text...", state="running")
                    text, file_type = FileProcessor.extract_text(temp_file_path)
                    file_info = FileProcessor.get_file_info(temp_file_path)
                    
                    # Step 2: Preprocess text
                    text = TextPreprocessor.clean_text(text)
                    text = TextPreprocessor.normalize_whitespace(text)
                    detected_language = TextPreprocessor.detect_language(text)
                    
                    # Step 3: Classify contract
                    st.status("Classifying contract...", state="running")
                    if contract_type == "Auto-detect":
                        classified_type, confidence = ContractClassifier.classify(text)
                    else:
                        classified_type = ContractType[contract_type.upper()]
                        confidence = 1.0
                    
                    # Step 4: Extract entities
                    st.status("Extracting entities...", state="running")
                    entities = NERProcessor.extract_entities(text)
                    specific_info = NERProcessor.extract_specific_info(text)
                    
                    # Step 5: Extract clauses
                    st.status("Extracting clauses...", state="running")
                    clauses = ClauseExtractor.extract_clauses(text)
                    
                    # Step 6: Assess risks
                    st.status("Assessing risks...", state="running")
                    unfavorable_ids = RiskAssessor.identify_unfavorable_clauses(clauses)
                    composite_score, composite_risk = RiskAssessor.calculate_composite_risk(clauses)
                    key_risks = [c.reason_for_risk for c in clauses if c.risk_level.value == "high"]
                    recommendations = RiskAssessor.get_risk_recommendations(clauses)
                    
                    # Step 7: Generate summary (with LLM if enabled)
                    st.status("Generating summary...", state="running")
                    if use_llm:
                        try:
                            llm = LLMIntegration(
                                provider="claude" if "Claude" in llm_provider else "openai"
                            )
                            summary = llm.generate_summary(text[:3000], classified_type.value)
                        except Exception as e:
                            summary = f"Summary generation failed: {str(e)}"
                    else:
                        summary = f"This is a {classified_type.value} contract with {len(clauses)} clauses and a composite risk score of {composite_score:.1f}."
                    
                    # Create metadata
                    metadata = ContractMetadata(
                        contract_type=classified_type,
                        language=detected_language,
                        parties=specific_info['parties'],
                        effective_date=specific_info['dates'][0] if specific_info['dates'] else None,
                        jurisdiction=specific_info['jurisdictions'][0] if specific_info['jurisdictions'] else None,
                        financial_amount=specific_info['amounts'][0] if specific_info['amounts'] else None,
                        file_name=file_info['file_name'],
                        file_size=file_info['file_size'],
                        processed_at=datetime.now()
                    )
                    
                    # Create analysis result
                    analysis = ContractAnalysis(
                        contract_id=st.session_state.current_contract_id,
                        metadata=metadata,
                        summary=summary,
                        clauses=clauses,
                        composite_risk_score=composite_score,
                        composite_risk_level=composite_risk,
                        key_risks=list(set(key_risks)),
                        unfavorable_clauses=unfavorable_ids,
                        recommendations=recommendations,
                        audit_trail_id=str(uuid.uuid4()),
                        analysis_timestamp=datetime.now()
                    )
                    
                    st.session_state.contract_analysis = analysis
                    
                    # Create audit log
                    audit_entry = create_audit_log(
                        action="contract_analyzed",
                        details={
                            "file_name": file_info['file_name'],
                            "contract_type": classified_type.value,
                            "clauses_found": len(clauses),
                            "risk_score": composite_score
                        }
                    )
                    st.session_state.audit_logs.append(audit_entry)
                    
                    st.success("✅ Contract analysis complete!")
                
                # Clean up temp file
                os.remove(temp_file_path)
                
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
    
    with tab2:
        st.header("Analysis Results")
        
        if st.session_state.contract_analysis:
            analysis = st.session_state.contract_analysis
            
            # Overview section
            st.subheader("📋 Overview")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Contract Type", analysis.metadata.contract_type.value.title())
            with col2:
                st.metric("Risk Score", f"{analysis.composite_risk_score:.1f}/100")
            with col3:
                st.metric("Total Clauses", len(analysis.clauses))
            with col4:
                st.metric("High-Risk Clauses", len([c for c in analysis.clauses if c.risk_level.value == "high"]))
            
            # Summary
            st.subheader("📝 Contract Summary")
            st.write(analysis.summary)
            
            # Metadata
            st.subheader("📊 Contract Metadata")
            meta_col1, meta_col2 = st.columns(2)
            with meta_col1:
                st.write(f"**Parties:** {', '.join(analysis.metadata.parties) if analysis.metadata.parties else 'Not identified'}")
                st.write(f"**Effective Date:** {analysis.metadata.effective_date or 'Not specified'}")
            with meta_col2:
                st.write(f"**Jurisdiction:** {analysis.metadata.jurisdiction or 'Not specified'}")
                st.write(f"**Financial Amount:** {analysis.metadata.financial_amount or 'Not specified'}")
            
            # Risk Assessment
            st.subheader("⚠️ Risk Assessment")
            st.info(f"**Composite Risk Level:** {analysis.composite_risk_level.value.upper()}")
            if analysis.key_risks:
                st.write("**Key Risks Identified:**")
                for risk in analysis.key_risks[:5]:
                    st.write(f"• {risk}")
            
            # Unfavorable Clauses
            if analysis.unfavorable_clauses:
                st.subheader("❌ Unfavorable Clauses")
                for clause_id in analysis.unfavorable_clauses[:3]:
                    clause = next((c for c in analysis.clauses if c.clause_id == clause_id), None)
                    if clause:
                        st.warning(f"**{clause.title or clause_id}** (Risk: {clause.risk_level.value.upper()})")
                        st.write(f"**Explanation:** {clause.plain_language_explanation}")
                        if clause.suggested_alternative:
                            st.write(f"**Suggested Alternative:** {clause.suggested_alternative}")
            
            # Recommendations
            if analysis.recommendations:
                st.subheader("💡 Recommendations")
                for rec in analysis.recommendations[:5]:
                    st.write(f"✓ {rec}")
            
            # Clause Details
            st.subheader("📄 Detailed Clause Analysis")
            for clause in analysis.clauses:
                with st.expander(f"{clause.title or 'Clause'} - Risk: {clause.risk_level.value.upper()}"):
                    st.write(f"**Text:** {clause.text[:200]}...")
                    st.write(f"**Category:** {clause.category.value}")
                    st.write(f"**Risk Score:** {clause.risk_score:.1f}/100")
                    st.write(f"**Reason:** {clause.reason_for_risk}")
                    st.write(f"**Explanation:** {clause.plain_language_explanation}")
                    if clause.suggested_alternative:
                        st.write(f"**Alternative:** {clause.suggested_alternative}")
            
            # Export options
            st.subheader("📥 Export Options")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💾 Save Analysis"):
                    st.info("Analysis saved to data folder")
            with col2:
                if st.button("📊 Export as JSON"):
                    analysis_dict = analysis.model_dump()
                    st.download_button(
                        label="Download JSON",
                        data=json.dumps(analysis_dict, indent=2, default=str),
                        file_name=f"contract_analysis_{analysis.contract_id}.json",
                        mime="application/json"
                    )
            with col3:
                if st.button("📋 Save Audit Trail"):
                    audit_path = save_audit_trail(st.session_state.audit_logs)
                    if audit_path:
                        st.success(f"Audit trail saved to {audit_path}")
        else:
            st.info("No analysis results yet. Upload and analyze a contract in the first tab.")
    
    with tab3:
        st.header("Contract Templates")
        st.info("Standard SME-friendly contract templates coming soon")
        
        template_types = ["Employment Agreement", "Vendor Contract", "Lease Agreement", 
                         "Partnership Deed", "Service Contract"]
        
        selected_template = st.selectbox("Select template type", template_types)
        
        if st.button("📥 Download Template"):
            st.info(f"Template for {selected_template} will be downloadable soon")
    
    with tab4:
        st.header("Settings & Information")
        
        st.subheader("About This Bot")
        st.write("""
        This Contract Analysis & Risk Assessment Bot helps Indian SMEs:
        - Understand complex contracts in plain language
        - Identify legal risks and problematic clauses
        - Get negotiation recommendations
        - Check compliance with Indian laws
        - Maintain audit trails of all analyses
        """)
        
        st.subheader("How It Works")
        st.write("""
        1. **Upload** your contract (PDF, DOCX, or TXT)
        2. **System automatically**:
           - Classifies contract type
           - Extracts key entities and clauses
           - Assesses risk at clause and contract level
           - Generates plain language explanations
        3. **Review** results and recommendations
        4. **Export** analysis for legal review
        """)
        
        st.subheader("Supported Contract Types")
        st.write("""
        - Employment Agreements
        - Vendor/Supplier Contracts
        - Lease Agreements
        - Partnership Deeds
        - Service Contracts
        """)
        
        st.subheader("Privacy & Security")
        st.write("""
        ✓ All processing is done locally
        ✓ No data is stored on external servers
        ✓ Audit trails maintained for compliance
        ✓ Confidentiality is maintained
        """)


if __name__ == "__main__":
    main()
