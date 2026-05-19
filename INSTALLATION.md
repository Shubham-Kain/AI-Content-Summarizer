# 📦 Installation Guide - AI Content Summarizer

## Quick Start

### Option 1: Using Batch Script (Windows)
```bash
cd d:\AI-Video-Summarizer
install_dependencies.bat
```

### Option 2: Using Python Script (All Platforms)
```bash
cd d:\AI-Video-Summarizer
python install_deps.py
```

### Option 3: Manual Installation
```bash
cd d:\AI-Video-Summarizer
pip install -r requirements.txt
```

---

## Complete Installation Steps

### Step 1: Prerequisites
- Python 3.10+ installed
- pip package manager
- 500 MB free disk space (for dependencies + models)
- Internet connection

### Step 2: Clone/Navigate to Project
```bash
cd d:\AI-Video-Summarizer
```

### Step 3: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv myenv

# Activate virtual environment
# On Windows:
myenv\Scripts\activate
# On macOS/Linux:
source myenv/bin/activate
```

### Step 4: Install Dependencies

#### Method A - One Command
```bash
pip install -r requirements.txt
```

#### Method B - Using Provided Scripts
```bash
# Windows (Batch)
install_dependencies.bat

# All platforms (Python)
python install_deps.py
```

#### Method C - Install Groups Separately
```bash
# Core dependencies
pip install streamlit google-genai openai python-dotenv

# Video processing
pip install youtube-transcript-api beautifulsoup4 strip-markdown

# UI enhancement
pip install st-copy-to-clipboard

# PDF + RAG dependencies
pip install langchain langchain-community chromadb pypdf sentence-transformers
```

### Step 5: Verify Installation
```bash
python -c "import streamlit, langchain, chromadb, pypdf; print('✅ All dependencies installed successfully!')"
```

### Step 6: Configure API Keys
Create a `.env` file in the project root:
```
GOOGLE_GEMINI_API_KEY="your-gemini-api-key-here"
OPENAI_API_KEY="your-openai-api-key-here"
```

Get API Keys:
- [Google Gemini](https://makersuite.google.com/app/apikey)
- [OpenAI](https://platform.openai.com/api-keys)

### Step 7: Run the Application
```bash
streamlit run app.py
```

The app will open at: `http://localhost:8501`

---

## Dependencies Breakdown

### Core UI & Framework
- **streamlit**: Web interface framework
- **st-copy-to-clipboard**: Copy button functionality

### LLM Integration
- **google-genai**: Google Gemini API
- **openai**: OpenAI GPT API
- **langchain**: RAG framework
- **langchain-community**: Community integrations

### Video Processing
- **youtube-transcript-api**: Extract YouTube transcripts
- **beautifulsoup4**: HTML parsing
- **strip-markdown**: Markdown processing

### PDF & RAG
- **pypdf**: PDF text extraction
- **chromadb**: Vector database for embeddings
- **sentence-transformers**: Text embedding model

### Utilities
- **python-dotenv**: Environment variable management

---

## Troubleshooting

### Issue: "pip: command not found"
**Solution**: Python pip not installed. Install Python 3.10+ from python.org

### Issue: "Module not found" errors
**Solution**: Ensure virtual environment is activated and pip install completed successfully
```bash
pip list  # Check installed packages
```

### Issue: "CUDA not available" warnings (for sentence-transformers)
**Solution**: Normal warning - CPU version will be used. No action needed.

### Issue: Permission denied (Linux/Mac)
**Solution**: Use sudo or create virtual environment
```bash
python3 -m venv myenv
source myenv/bin/activate
```

### Issue: Network timeout during installation
**Solution**: Retry or use a different PyPI mirror
```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### Issue: Disk space warning
**Solution**: Ensure 500+ MB free space, or clear cache
```bash
pip cache purge
```

---

## Verification Checklist

After installation, verify:
- [ ] `pip list` shows all packages from requirements.txt
- [ ] `python -c "import streamlit"` works
- [ ] `python -c "import langchain"` works
- [ ] `python -c "import chromadb"` works
- [ ] `python -c "from sentence_transformers import SentenceTransformer"` works
- [ ] `.env` file exists with API keys
- [ ] `streamlit run app.py` launches the application

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.10 | 3.11+ |
| RAM | 4 GB | 8 GB |
| Disk Space | 500 MB | 1 GB |
| Internet | 50 Mbps | 100+ Mbps |
| OS | Windows 10+ / Linux / macOS | Latest LTS |

---

## Next Steps After Installation

1. ✅ Dependencies installed
2. 📝 Create `.env` with API keys
3. 🚀 Run: `streamlit run app.py`
4. 🌐 Open: `http://localhost:8501`
5. 📺 Test Video Mode: Paste YouTube URL
6. 📄 Test PDF Mode: Upload a PDF document

---

## Support

If you encounter issues:
1. Check that all commands completed without errors
2. Verify Python version: `python --version` (should be 3.10+)
3. Check pip version: `pip --version`
4. Try reinstalling in a fresh virtual environment
5. Check the application logs for detailed error messages

---

## Updates & Maintenance

To update dependencies later:
```bash
pip install -r requirements.txt --upgrade
```

To create a requirements file from current environment:
```bash
pip freeze > requirements_current.txt
```
