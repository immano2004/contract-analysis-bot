# SETUP_GUIDE.md

# Contract Analysis & Risk Assessment Bot - Setup Guide

## 📋 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- API keys for Claude (Anthropic) or GPT-4 (OpenAI)

### Installation Steps

#### 1. Clone and Navigate
```bash
cd "Contract Analysis & Risk Assessment Bot"
```

#### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

#### 4. Download NLP Models
```bash
# Download spaCy English model
python -m spacy download en_core_web_sm

# Download NLTK data
python -m nltk.downloader punkt stopwords wordnet averaged_perceptron_tagger
```

#### 5. Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys:
# - ANTHROPIC_API_KEY=your_key_here (if using Claude)
# - OPENAI_API_KEY=your_key_here (if using GPT-4)
```

#### 6. Run the Application
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 🧪 Testing

### Run Unit Tests
```bash
pytest tests/test_modules.py -v
```

### Run with Coverage
```bash
pytest tests/test_modules.py --cov=src --cov-report=html
```

## 📁 Project Structure

```
contract-analysis-bot/
├── app.py                          # Main Streamlit application
├── src/
│   ├── contract_engine.py          # Main orchestrator
│   ├── core/
│   │   ├── contract_classifier.py  # Contract type classification
│   │   ├── clause_extractor.py     # Clause extraction and analysis
│   │   ├── ner_processor.py        # Named entity recognition
│   │   ├── risk_assessor.py        # Risk assessment
│   │   ├── compliance_checker.py   # Indian law compliance
│   │   └── llm_integration.py      # LLM integration
│   ├── utils/
│   │   ├── file_processor.py       # File handling
│   │   ├── text_preprocessor.py    # Text preprocessing
│   │   ├── multilingual_handler.py # Hindi/English support
│   │   └── export_handler.py       # Export functionality
│   └── models/
│       └── contract_models.py      # Pydantic models
├── templates/
│   └── sample_templates.py         # Contract templates
├── data/
│   ├── audit_logs/                 # Audit trail storage
│   └── templates/                  # User templates
├── tests/
│   └── test_modules.py             # Unit tests
├── requirements.txt                # Core dependencies
├── requirements-dev.txt            # Development dependencies
├── README.md                       # Project documentation
└── .env.example                    # Environment variables template
```

## 🚀 Using the Application

### 1. Upload a Contract
- Navigate to "Upload & Analysis" tab
- Click "Choose a contract file"
- Supported formats: PDF, DOCX, DOC, TXT

### 2. Configure Analysis Options
- **Contract Type**: Select or auto-detect
- **Language**: Choose English or Hindi
- **LLM Provider**: Choose Claude or GPT-4 (requires API key)

### 3. Analyze
- Click "Analyze Contract"
- System will process and analyze the contract

### 4. Review Results
- View contract summary
- Check risk assessment
- Review unfavorable clauses
- Read recommendations

### 5. Export
- Save analysis as JSON
- Generate PDF report
- Download audit trail

## 🔐 Security & Privacy

- All processing is local (no cloud uploads)
- Temporary files are deleted after processing
- Audit trails are maintained for compliance
- No data is stored on external servers

## 🛠️ Troubleshooting

### Issue: "No module named 'src'"
**Solution**: Make sure you're running from the project root directory

### Issue: spaCy model not found
**Solution**: Run `python -m spacy download en_core_web_sm`

### Issue: LLM API key errors
**Solution**: Verify API keys in `.env` file and ensure they're valid

### Issue: PDF extraction not working
**Solution**: Ensure PDF is text-based (not scanned image). PyPDF2 doesn't support image PDFs.

## 📞 Support

For issues or questions:
1. Check the README.md for detailed documentation
2. Review logs in `data/audit_logs/`
3. Run unit tests to verify installation

## 📚 Additional Features

### Planned Enhancements
- [ ] Support for more contract types
- [ ] Enhanced Hindi language support
- [ ] Contract template marketplace
- [ ] Batch analysis capability
- [ ] Integration with e-signature platforms
- [ ] Real-time collaboration features
- [ ] Advanced analytics dashboard
- [ ] Machine learning for risk prediction

### Extension Points
- Add custom compliance rules
- Create organization-specific templates
- Implement additional LLM providers
- Add custom risk scoring logic

## 📝 License & Usage

This project is designed for Indian SMEs and follows all regulatory requirements.

---

**Happy analyzing! 📋✅**
