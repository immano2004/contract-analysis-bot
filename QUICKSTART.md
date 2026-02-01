# 🚀 Getting Started with Contract Analysis Bot

## ⚡ Quick Start (5 minutes)

### Step 1: Setup Environment
```bash
# Navigate to project directory
cd "Contract Analysis & Risk Assessment Bot"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Download NLP models
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt stopwords wordnet
```

### Step 3: Configure API Keys
```bash
# Copy environment template
copy .env.example .env  # On Windows
cp .env.example .env   # On macOS/Linux

# Edit .env file and add your API keys:
# ANTHROPIC_API_KEY=your_anthropic_key_here
# OPENAI_API_KEY=your_openai_key_here (optional)
```

### Step 4: Run Application
```bash
streamlit run app.py
```

Visit: `http://localhost:8501`

---

## 📚 Documentation Overview

### For Beginners
1. **[README.md](README.md)** - Feature overview and capabilities
2. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed installation instructions
3. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete project information

### For Developers
1. **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Full API reference
2. **[EXAMPLES.py](EXAMPLES.py)** - 10 usage examples
3. **[src/](src/)** - Source code with docstrings

### For System Administrators
1. **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Deployment instructions
2. **[requirements.txt](requirements.txt)** - Python dependencies
3. **[.env.example](.env.example)** - Configuration template

---

## 🎯 Common Tasks

### Upload and Analyze a Contract

1. Open the application at `http://localhost:8501`
2. Go to **"Upload & Analysis"** tab
3. Click **"Choose a contract file"**
4. Select PDF, DOCX, or TXT file
5. (Optional) Select contract type or leave as "Auto-detect"
6. Click **"🔍 Analyze Contract"**
7. Wait for analysis to complete
8. Review results in **"Results"** tab

### Export Analysis Results

```python
# In the Results tab:
# 1. Click "💾 Save Analysis" to save locally
# 2. Click "📊 Export as JSON" for data export
# 3. Click "📋 Save Audit Trail" for compliance records
```

### Use as Python Library

```python
from src.contract_engine import ContractAnalysisEngine

# Initialize
engine = ContractAnalysisEngine(use_llm=True)

# Analyze contract
analysis = engine.analyze_contract("path/to/contract.pdf")

# Access results
print(f"Risk Score: {analysis.composite_risk_score}/100")
print(f"Type: {analysis.metadata.contract_type.value}")
```

---

## 🔍 Understanding the Analysis

### Risk Levels

| Level | Score | What It Means |
|-------|-------|---------------|
| 🟢 LOW | 0-39 | Standard terms, minor concerns |
| 🟡 MEDIUM | 40-69 | Moderate risks, review recommended |
| 🔴 HIGH | 70-100 | Significant risks, legal review critical |

### Key Outputs

- **Contract Summary**: 2-3 sentence overview
- **Risk Score**: 0-100 composite score
- **Clause Analysis**: Category, risk level, explanation
- **Key Risks**: Identified problem areas
- **Recommendations**: Negotiation suggestions
- **Compliance Issues**: Indian law violations

### Example Analysis

```
Contract: Employment Agreement
Type: Employment
Risk Score: 65/100 (MEDIUM)

High-Risk Clauses Found:
❌ Unilateral Termination Rights
   - Company can terminate without cause
   - Suggested: Require mutual consent

❌ Unlimited Liability
   - No cap on indemnification
   - Suggested: Limit to annual compensation

Key Recommendations:
✓ Negotiate termination notice period (30-60 days)
✓ Add liability cap clause
✓ Clarify severance pay obligations
```

---

## 🛠️ Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'spacy'"
**Solution:**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Issue: API Key Error
**Solution:**
1. Verify `.env` file exists
2. Check API keys are correctly formatted
3. Confirm keys are valid and have proper permissions
4. For Claude: Get key from https://console.anthropic.com
5. For OpenAI: Get key from https://platform.openai.com/account/api-keys

### Issue: Application Crashes on Large PDF
**Solution:**
1. Try converting PDF to text first
2. Split large contracts into parts
3. Ensure PDF is not password protected
4. Verify PDF contains selectable text (not scanned image)

### Issue: Slow Performance
**Solution:**
- Reduce contract file size
- Disable LLM analysis temporarily
- Check system resources (RAM, CPU)
- Use a simpler contract for testing

---

## 📖 Feature Guide

### Contract Type Detection
Automatically identifies:
- Employment Agreements
- Vendor Contracts
- Lease Agreements
- Partnership Deeds
- Service Contracts

### Risk Assessment Categories
- **Liability Clauses**: Unlimited or excessive liability
- **Termination Rights**: Unilateral or unfair termination
- **Penalty Clauses**: Excessive penalties or liquidated damages
- **IP Clauses**: Unfavorable intellectual property terms
- **Non-Compete**: Restrictive non-compete clauses

### Compliance Checks
- Employment law compliance
- Vendor contract standards
- Lease legal requirements
- Partnership agreement rules
- Service contract standards

### Export Options
- **JSON**: Machine-readable format for integration
- **PDF**: Professional report for sharing
- **Audit Trail**: Compliance tracking

---

## 🔐 Privacy & Security

✅ **Local Processing**: All data stays on your machine
✅ **No Cloud Upload**: Contracts are never sent to external servers
✅ **Temporary Files**: Deleted after processing
✅ **Confidentiality**: No data logging or storage
✅ **Audit Trail**: Track all analyses locally

---

## 💡 Tips & Best Practices

### For Best Results:

1. **Use Clear PDFs**: Prefer text-based PDFs over scanned images
2. **Complete Contracts**: Upload entire contracts, not fragments
3. **Standard Format**: Contracts in standard legal format work best
4. **Review Carefully**: Always review AI analysis with human judgment
5. **Consult Lawyers**: For critical clauses, consult legal professionals
6. **Export Records**: Keep audit trails for compliance

### Common Use Cases:

**For Employees:**
- Review employment offers before signing
- Understand terms and conditions
- Identify unfavorable clauses

**For Businesses:**
- Screen vendor contracts before signing
- Assess partnership agreements
- Review service contracts
- Compliance verification

**For Legal Professionals:**
- Speed up contract review process
- Identify high-risk areas quickly
- Generate audit trails
- Create contract templates

---

## 🎓 Learning Path

### Beginner
1. Read [README.md](README.md)
2. Run through "Getting Started" section
3. Upload a sample contract
4. Review results tab

### Intermediate
1. Read [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
2. Run examples from [EXAMPLES.py](EXAMPLES.py)
3. Try Python scripting
4. Export and analyze results

### Advanced
1. Study [src/](src/) implementation
2. Customize compliance rules
3. Extend with new modules
4. Deploy to production

---

## 📞 Getting Help

### Documentation
- Full README: [README.md](README.md)
- Setup guide: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- API docs: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- Examples: [EXAMPLES.py](EXAMPLES.py)

### Source Code
All modules include docstrings. Key files:
- [src/contract_engine.py](src/contract_engine.py) - Main orchestrator
- [src/core/](src/core/) - Analysis modules
- [src/utils/](src/utils/) - Utility functions

### Support Resources
- Check error messages carefully
- Review logs in `data/audit_logs/`
- Consult API documentation
- Review source code comments

---

## 🔄 Next Steps

After setup:

1. ✅ **Verify Installation**: Run the application
2. ✅ **Test with Sample**: Try with a test contract
3. ✅ **Review Results**: Understand the output format
4. ✅ **Customize Settings**: Adjust LLM provider, language
5. ✅ **Export Reports**: Try different export formats
6. ✅ **Integrate**: Use as library in your application
7. ✅ **Extend**: Add custom rules and templates

---

## 📊 System Requirements

- **Python**: 3.9 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 2GB for dependencies and models
- **Internet**: Only for LLM API calls (if enabled)
- **Browser**: Modern browser for Streamlit UI

---

## 🚀 Ready to Begin!

```bash
# Quick start commands:
cd "Contract Analysis & Risk Assessment Bot"
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
```

Open browser to: **http://localhost:8501**

---

**Happy analyzing! 📋✨**

For detailed information, see [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
