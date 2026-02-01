# API Documentation

## Contract Analysis & Risk Assessment Bot - API Reference

### Core Modules

#### 1. ContractAnalysisEngine
Main orchestrator for contract analysis.

```python
from src.contract_engine import ContractAnalysisEngine

# Initialize engine
engine = ContractAnalysisEngine(use_llm=True, llm_provider="claude")

# Analyze contract
analysis = engine.analyze_contract(
    file_path="path/to/contract.pdf",
    contract_type=None  # Auto-detect or specify
)
```

**Returns**: `ContractAnalysis` object

---

### Data Models

#### ContractAnalysis
Complete contract analysis result.

```python
class ContractAnalysis(BaseModel):
    contract_id: str
    metadata: ContractMetadata
    summary: str
    clauses: List[Clause]
    composite_risk_score: float  # 0-100
    composite_risk_level: RiskLevel  # LOW, MEDIUM, HIGH
    key_risks: List[str]
    compliance_issues: List[str]
    unfavorable_clauses: List[str]
    recommendations: List[str]
    audit_trail_id: str
    analysis_timestamp: datetime
```

#### Clause
Individual contract clause with analysis.

```python
class Clause(BaseModel):
    clause_id: str
    title: Optional[str]
    text: str
    category: ClauseCategory  # OBLIGATION, RIGHT, PENALTY, etc.
    risk_level: RiskLevel  # LOW, MEDIUM, HIGH
    risk_score: float  # 0-100
    reason_for_risk: Optional[str]
    plain_language_explanation: str
    suggested_alternative: Optional[str]
    entities: List[NamedEntity]
    is_unfavorable: bool
    compliance_flags: List[str]
```

#### RiskLevel
```python
class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
```

#### ClauseCategory
```python
class ClauseCategory(str, Enum):
    OBLIGATION = "obligation"
    RIGHT = "right"
    PROHIBITION = "prohibition"
    PENALTY = "penalty"
    INDEMNITY = "indemnity"
    TERMINATION = "termination"
    ARBITRATION = "arbitration"
    CONFIDENTIALITY = "confidentiality"
    IP_OWNERSHIP = "ip_ownership"
    OTHER = "other"
```

---

### Module APIs

#### FileProcessor
Handle file extraction and processing.

```python
from src.utils.file_processor import FileProcessor

# Extract text from file
text, file_type = FileProcessor.extract_text("contract.pdf")

# Get file information
file_info = FileProcessor.get_file_info("contract.pdf")
# Returns: {
#     'file_name': str,
#     'file_path': str,
#     'file_size': int,
#     'file_type': str,
#     'created_at': float,
#     'modified_at': float
# }
```

**Supported Formats**: `.pdf`, `.docx`, `.doc`, `.txt`

---

#### TextPreprocessor
Text preprocessing and analysis utilities.

```python
from src.utils.text_preprocessor import TextPreprocessor

# Clean and normalize text
cleaned = TextPreprocessor.clean_text(text)

# Extract sentences
sentences = TextPreprocessor.extract_sentences(text)

# Extract words
words = TextPreprocessor.extract_words(text, remove_stopwords=True)

# Detect language
lang = TextPreprocessor.detect_language(text)  # Returns 'en' or 'hi'

# Extract section numbers
sections = TextPreprocessor.extract_section_numbers(text)

# Extract key terms
key_terms = TextPreprocessor.extract_key_terms(text, num_terms=10)
```

---

#### ContractClassifier
Classify contract types based on content.

```python
from src.core.contract_classifier import ContractClassifier

# Classify contract
contract_type, confidence = ContractClassifier.classify(text)

# Get classification with reasoning
result = ContractClassifier.classify_with_reasoning(text)
# Returns: {
#     'contract_type': str,
#     'confidence': float,
#     'matched_keywords': List[str],
#     'reasoning': str
# }
```

**Contract Types**: EMPLOYMENT, VENDOR, LEASE, PARTNERSHIP, SERVICE, OTHER

---

#### NERProcessor
Named Entity Recognition and extraction.

```python
from src.core.ner_processor import NERProcessor

# Extract all entities
entities = NERProcessor.extract_entities(text)

# Extract parties
parties = NERProcessor.extract_parties(text)

# Extract specific information
info = NERProcessor.extract_specific_info(text)
# Returns: {
#     'parties': List[str],
#     'dates': List[str],
#     'amounts': List[str],
#     'jurisdictions': List[str],
#     'entities': List[NamedEntity]
# }
```

---

#### ClauseExtractor
Extract and analyze contract clauses.

```python
from src.core.clause_extractor import ClauseExtractor

# Extract all clauses
clauses = ClauseExtractor.extract_clauses(text)
```

Returns: `List[Clause]`

---

#### RiskAssessor
Assess contract risks.

```python
from src.core.risk_assessor import RiskAssessor

# Assess single clause risk
risk_level, score, reason = RiskAssessor.assess_clause_risk(
    clause_text,
    clause_category=ClauseCategory.PENALTY
)

# Identify unfavorable clauses
unfavorable_ids = RiskAssessor.identify_unfavorable_clauses(clauses)

# Calculate composite risk
composite_score, risk_level = RiskAssessor.calculate_composite_risk(clauses)

# Get recommendations
recommendations = RiskAssessor.get_risk_recommendations(clauses)
```

---

#### ComplianceChecker
Check compliance with Indian laws.

```python
from src.core.compliance_checker import ComplianceChecker

# Check compliance
compliance = ComplianceChecker.check_compliance(text, contract_type)
# Returns: {
#     'compliant': List[str],
#     'warnings': List[str],
#     'violations': List[str]
# }

# Check Indian-specific requirements
issues = ComplianceChecker.check_Indian_specific_requirements(text)
```

---

#### LLMIntegration
LLM-powered analysis.

```python
from src.core.llm_integration import LLMIntegration

# Initialize LLM
llm = LLMIntegration(provider="claude")

# Generate summary
summary = llm.generate_summary(contract_text, contract_type)

# Generate plain language explanation
explanation = llm.generate_plain_language_explanation(
    clause_text,
    clause_category
)

# Get renegotiation suggestions
suggestions = llm.generate_renegotiation_suggestions(
    clause_text,
    risk_level
)

# Check compliance
concerns = llm.check_compliance(clause_text, contract_type)
```

---

#### ExportHandler
Export analysis results.

```python
from src.utils.export_handler import ExportHandler

# Export to JSON
json_path = ExportHandler.export_to_json(analysis_dict, "output.json")

# Export to PDF
pdf_path = ExportHandler.export_to_pdf(analysis_dict, "output.pdf")

# Export to DOCX
docx_path = ExportHandler.export_to_docx(analysis_dict, "output.docx")
```

---

#### MultilingualHandler
Handle multilingual contracts.

```python
from src.utils.multilingual_handler import MultilingualHandler

# Detect language
lang = MultilingualHandler.detect_language(text)

# Translate Hindi to English
english_text = MultilingualHandler.translate_hindi_to_english(text)

# Normalize contract text
normalized_text, language = MultilingualHandler.normalize_contract_text(text)
```

---

### Usage Examples

#### Example 1: Complete Contract Analysis
```python
from src.contract_engine import ContractAnalysisEngine

# Initialize engine
engine = ContractAnalysisEngine(use_llm=True, llm_provider="claude")

# Analyze contract
analysis = engine.analyze_contract("employment_contract.pdf")

# Access results
print(f"Contract Type: {analysis.metadata.contract_type.value}")
print(f"Risk Score: {analysis.composite_risk_score}/100")
print(f"Risk Level: {analysis.composite_risk_level.value}")
print(f"Summary: {analysis.summary}")

# Review clauses
for clause in analysis.clauses:
    print(f"\nClause: {clause.title}")
    print(f"Risk: {clause.risk_level.value}")
    print(f"Explanation: {clause.plain_language_explanation}")

# Get recommendations
for rec in analysis.recommendations:
    print(f"• {rec}")
```

#### Example 2: Extract and Analyze Clauses
```python
from src.utils.file_processor import FileProcessor
from src.utils.text_preprocessor import TextPreprocessor
from src.core.clause_extractor import ClauseExtractor
from src.core.risk_assessor import RiskAssessor

# Extract text
text, _ = FileProcessor.extract_text("contract.pdf")

# Preprocess
text = TextPreprocessor.clean_text(text)

# Extract clauses
clauses = ClauseExtractor.extract_clauses(text)

# Assess risks
for clause in clauses:
    print(f"Clause: {clause.title}")
    print(f"Risk Score: {clause.risk_score}/100")
    print(f"Reason: {clause.reason_for_risk}")
```

#### Example 3: Extract Key Information
```python
from src.core.ner_processor import NERProcessor

# Extract all information
info = NERProcessor.extract_specific_info(text)

print(f"Parties: {', '.join(info['parties'])}")
print(f"Dates: {', '.join(info['dates'])}")
print(f"Amounts: {', '.join(info['amounts'])}")
print(f"Jurisdiction: {', '.join(info['jurisdictions'])}")
```

---

### Error Handling

All modules include comprehensive error handling:

```python
try:
    analysis = engine.analyze_contract("contract.pdf")
except FileNotFoundError:
    print("Contract file not found")
except ValueError as e:
    print(f"Invalid file format: {e}")
except Exception as e:
    print(f"Analysis error: {e}")
```

---

### Performance Notes

- **File Size**: Supports files up to 50MB
- **Processing Time**: 
  - Simple contracts: 5-10 seconds
  - Complex contracts: 15-30 seconds
- **Maximum Clauses**: Default limit is 100 clauses per contract
- **Memory**: ~200-300MB for large contract analysis

---

### Best Practices

1. **Always preprocess text** before analysis
2. **Handle exceptions** properly in production
3. **Use audit trails** for compliance tracking
4. **Validate inputs** before processing
5. **Cache results** for repeated analysis
6. **Monitor API usage** when using LLM providers
7. **Test with various contract types**
8. **Regular updates** of NLP models

---

For more information, see [README.md](README.md) and [SETUP_GUIDE.md](SETUP_GUIDE.md)
