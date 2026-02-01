# Contract Analysis & Risk Assessment Bot

A sophisticated GenAI-powered legal assistant designed to help small and medium business owners understand complex contracts, identify potential legal risks, and receive actionable advice in plain language.

## 📋 Key Features

### Core Legal NLP Tasks
- **Contract Type Classification**: Automatically identifies contract types (employment, vendor, lease, partnership, service)
- **Clause & Sub-Clause Extraction**: Extracts and structures contract clauses
- **Named Entity Recognition**: Identifies parties, dates, jurisdiction, liabilities, and amounts
- **Obligation vs. Right vs. Prohibition Identification**: Categorizes contract terms
- **Risk & Compliance Detection**: Identifies unfavorable terms and compliance issues
- **Ambiguity Detection**: Flags unclear or problematic language
- **Clause Similarity Matching**: Matches against standard templates

### Risk Assessment Capabilities
- **Clause-level Risk Scoring**: Low/Medium/High risk evaluation per clause
- **Composite Risk Score**: Contract-level risk assessment
- **Identification of Key Risk Areas**:
  - Penalty clauses
  - Indemnity clauses
  - Unilateral termination rights
  - Arbitration & jurisdiction terms
  - Auto-renewal & lock-in periods
  - Non-compete & IP transfer clauses

### User-Facing Outputs
- Simplified contract summaries
- Clause-by-clause plain-language explanations
- Unfavorable clause highlights
- Suggested renegotiation alternatives
- Standardized SME-friendly contract templates
- PDF export for legal review
- Audit trails for all analyses

## 📊 Data Handling

### Input File Formats
- PDF (text-based)
- DOC/DOCX
- Plain Text (.txt)

### Data Dimensions Extracted
- Parties and signatories
- Financial amounts and payment terms
- Obligations & liabilities
- Deliverables & performance metrics
- Timeline/duration
- Termination conditions
- Jurisdiction & governing law
- Rights & ownership (especially IP)
- Confidentiality & NDAs

### Multilingual Support
- English contract parsing
- Hindi contract parsing
- Hindi→English internal normalization for NLP tasks
- Output summaries in simple business English

## 🛠️ Technology Stack

### Backend
- **LLM**: Claude 3 (Anthropic) for legal reasoning
- **NLP**: Python with spaCy and NLTK for preprocessing
- **UI**: Streamlit for interactive interface
- **Storage**: Local file & JSON-based audit logs

### Libraries
- `spacy`: Advanced NLP and entity recognition
- `nltk`: Natural language toolkit for text processing
- `langchain`: LLM integration and chaining
- `python-docx`: DOCX file processing
- `PyPDF2`: PDF text extraction
- `pandas`: Data manipulation
- `pydantic`: Data validation

## 📁 Project Structure

```
contract-analysis-bot/
├── src/
│   ├── core/                    # Core analysis modules
│   │   ├── contract_classifier.py
│   │   ├── clause_extractor.py
│   │   ├── ner_processor.py
│   │   ├── risk_assessor.py
│   │   └── compliance_checker.py
│   ├── utils/                   # Utility functions
│   │   ├── file_processor.py
│   │   ├── text_preprocessor.py
│   │   ├── multilingual_handler.py
│   │   └── export_handler.py
│   ├── models/                  # Data models
│   │   ├── contract_models.py
│   │   ├── risk_models.py
│   │   └── clause_models.py
│   └── llm/                     # LLM integration
│       ├── claude_integration.py
│       └── prompt_templates.py
├── data/                        # Data storage
│   ├── audit_logs/
│   ├── templates/
│   └── knowledge_base/
├── templates/                   # Contract templates
├── tests/                       # Unit tests
├── app.py                       # Main Streamlit app
├── requirements.txt             # Python dependencies
└── README.md
```

## 🚀 Getting Started

### Installation

1. Clone the repository:
```bash
cd "Contract Analysis & Risk Assessment Bot"
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download required NLP models:
```bash
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt stopwords wordnet
```

5. Set up environment variables:
Create a `.env` file in the project root:
```
ANTHROPIC_API_KEY=your_api_key_here
```

### Running the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 📖 Usage Guide

### 1. Upload a Contract
- Navigate to the upload section
- Select PDF, DOCX, or TXT file
- The system automatically detects the file type

### 2. Select Contract Type (Optional)
- Auto-detection is available
- Manually specify if needed (Employment, Vendor, Lease, Partnership, Service)

### 3. Choose Language
- English or Hindi
- System handles multilingual contracts

### 4. View Analysis Results
- **Overview**: Contract summary and metadata
- **Risk Assessment**: Composite and clause-level risk scores
- **Clause Analysis**: Detailed explanation of each clause
- **Unfavorable Terms**: Highlighted risky clauses with explanations
- **Recommendations**: Suggested negotiation alternatives
- **Compliance Check**: Indian law compliance verification

### 5. Export Results
- Generate PDF report
- Download JSON audit trail
- Save to knowledge base

## 🔍 Core Components

### Contract Classifier
Automatically identifies contract type using NLP patterns and keywords.

### Clause Extractor
Extracts individual clauses and their relationships using spaCy and rule-based patterns.

### Named Entity Recognition (NER)
Identifies:
- Parties involved
- Dates and timelines
- Financial amounts
- Jurisdiction information
- Liabilities and penalties

### Risk Assessor
Evaluates risk at clause and contract level based on:
- Penalty severity
- Indemnity obligations
- Termination rights
- Lock-in periods
- IP transfer clauses

### Compliance Checker
Validates contract terms against Indian legal standards:
- Labor laws (for employment contracts)
- Contract law principles
- Industry-specific regulations

### Multilingual Handler
- Hindi→English translation for NLP processing
- Maintains context and technical terms
- Provides output in user's preferred language

## 🔐 Security & Compliance

- Local file processing (no cloud storage)
- Comprehensive audit trails
- Confidentiality maintained through file cleanup
- No external legal data dependencies

## 📝 License

This project is designed for SMEs in India and follows the requirements specified.

## 👥 Support

For issues or questions, please refer to the documentation or contact support.

---

**Note**: This bot is designed to provide guidance and analysis only. For critical legal decisions, consultation with a qualified legal professional is recommended.
