# Text Simplifier & Translator

A production-style Streamlit application that simplifies complex text and translates it into multiple languages while preserving meaning and technical accuracy.

---

# Features

- Text simplification using AI
- Translation into multiple languages
- PDF, DOCX, TXT support
- OCR support for scanned images
- Glossary consistency
- Readability scoring
- Batch-safe chunk processing
- TXT and DOCX export
- Editable outputs
- Streamlit UI
- OpenAI and Gemini support

---

# Project Structure

text_simplifier_translator/

├── app.py  
├── requirements.txt  
├── .env.example  
├── README.md  

├── utils/  
│ ├── extractor.py  
│ ├── ocr_utils.py  
│ ├── llm_utils.py  
│ ├── translator_utils.py  
│ ├── export_utils.py  
│ └── helpers.py  

└── sample_outputs/  
└── demo_output.txt  

---

# Setup Instructions

## 1. Clone the Project

```bash
git clone <your_repo_url>
cd text_simplifier_translator