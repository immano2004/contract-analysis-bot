# Contract Analysis & Risk Assessment Bot - Development Guidelines

## Project Overview
Building a sophisticated GenAI-powered legal assistant for analyzing contracts, identifying risks, and providing actionable advice in plain language for Indian SMEs.

## Technology Stack
- **Backend**: Python 3.9+
- **LLM**: Claude 3 (Anthropic) or GPT-4
- **NLP**: spaCy, NLTK
- **UI**: Streamlit
- **Storage**: Local files, JSON-based audit logs
- **File Processing**: PyPDF2, python-docx

## Key Features to Implement
1. Contract classification (5 types)
2. Clause extraction & NER
3. Risk scoring (clause & composite level)
4. Multilingual support (English + Hindi)
5. Plain-language explanations
6. Unfavorable clause detection
7. Renegotiation suggestions
8. PDF export functionality
9. Audit trails
10. Contract templates

## Code Organization
- `src/core/`: Core NLP and analysis modules
- `src/utils/`: Helper functions and utilities
- `src/models/`: Data structures and Pydantic models
- `data/`: Storage for audit logs and templates
- `templates/`: Standard contract templates
- `tests/`: Unit tests

## Development Standards
- Use Pydantic for data validation
- Implement comprehensive error handling
- Add docstrings to all functions
- Create unit tests for core functionality
- Follow PEP 8 style guidelines
- Log all analysis operations for audit trail

## Integration Points
- Claude/GPT-4 for legal reasoning
- spaCy for NER and entity linking
- NLTK for text preprocessing
- Streamlit for UI rendering
- File processors for PDF/DOCX/TXT

## Notes
- No external legal data APIs allowed
- Maintain user confidentiality
- Keep responses in simple business language
- Support both English and Hindi contracts
- Generate audit trails for all operations
