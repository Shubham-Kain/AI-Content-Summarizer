<h1 align="center">
  <br>
  <a href="https://github.com/siddharthsky/AI-Video-Summarizer"><img src="https://i.imgur.com/Jk1wxO3.png" alt="AI Content Summarizer" width="200"></a>
  <br>
   🎥 AI Content Summarizer - Video & PDF Edition
  <br>
</h1>

<h4 align="center">Harnessing the Power of LLMs for Enhanced Content Understanding</h4>

<p align="center">
  <a href="https://github.com/siddharthsky/AI-Video-Summarizer/issues"><img src="https://img.shields.io/github/issues/siddharthsky/google-gemini-yt-video-summarizer-AI-p"></a> 
  <a href="https://github.com/siddharthsky/AI-Video-Summarizer/stargazers"><img src="https://img.shields.io/github/stars/siddharthsky/google-gemini-yt-video-summarizer-AI-p"></a>
  <a href="https://github.com/siddharthsky/AI-Video-Summarizer/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg">
  </a>
</p>

<p align="center">
  <a href="#overview-">Overview</a> •
  <a href="#features-">Features</a> •
  <a href="#getting-started-">Getting Started</a> •
  <a href="#contributing">Contributing</a> 
</p>

<p align="center">
  <a href="https://github.com/siddharthsky/AI-Video-Summarizer"><img src="https://github.com/siddharthsky/AI-Video-Summarizer/blob/main/research/demo4.gif" alt="Usage Demo"></a>
</p>




## Overview 📝

AI Content Summarizer is a comprehensive tool for extracting insights from multiple content types. Originally designed for YouTube videos, it now includes **RAG (Retrieval-Augmented Generation)** capabilities for PDF document analysis. This application leverages advanced LLMs (Google Gemini and OpenAI GPT) to provide intelligent summarization, timestamp generation, and Q&A functionality.


## Features ✨

### 📺 YouTube Video Features
- Automatic extraction of key insights and timestamps from YouTube videos
- Utilizes youtube-transcript-api for getting transcripts/subtitles from YouTube videos
- Generate comprehensive summaries in seconds
- Extract timestamped chapters for easy navigation
- Download full transcripts

### 📄 PDF Document Features (NEW!)
- **RAG-Powered PDF Processing**: Upload PDFs and get intelligent summaries using Retrieval-Augmented Generation
- **Smart Summarization**: Automatic extraction of key points and main concepts
- **Question Answering**: Ask questions about PDF content and get accurate answers based on document context
- **Vector Database Integration**: Uses Chroma DB for semantic search and context retrieval
- **Multi-Model Support**: Works with both Gemini and OpenAI models

### 🤖 General Features
- Option for users to select AI models: *Gemini 2.5 Flash*, *Gemini 3*, *GPT-4o*, and more
- Clean, intuitive Streamlit UI with dark theme
- Copy and download functionality for all outputs
- Real-time processing status updates

## Getting Started 🚀

### Prerequisites

- Python 3.10+
- LLM Model API Keys [[🔑]](https://github.com/siddharthsky/AI-Video-Summarizer/tree/main?tab=readme-ov-file#get-api-keys)

### Installation & Setup

1. Clone the repository:
```
git clone https://github.com/siddharthsky/AI-Video-Summarizer.git
```

2. Navigate to the project directory:
```
cd AI-Video-Summarizer
```

3. Create a virtual environment (optional but recommended):
```
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

4. Install dependencies:
```
pip install -r requirements.txt
```

5. Create a ".env" file in the project root and add your API keys:
```
GOOGLE_GEMINI_API_KEY="Your-Gemini-Key-Here"
OPENAI_API_KEY="Your-OpenAI-Key-Here"
```

### Get API Keys:

- [Google Gemini API key](https://makersuite.google.com/app/apikey) 🔑 
   
- [OpenAI API key](https://platform.openai.com/signup) 🔑 

### Run the Application

```
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Usage

### Video Summarization Mode
1. Select "📺 YouTube Video" mode from the top menu
2. Paste a YouTube video URL
3. Choose your AI model (Gemini or OpenAI)
4. Select the action:
   - **AI Summary**: Get a concise summary of the video
   - **AI Timestamps**: Extract chapter breakdowns with timestamps
   - **Transcript**: Download the full video transcript

### PDF Analysis Mode (RAG-Powered)
1. Select "📄 PDF Document" mode from the top menu
2. Upload a PDF file
3. Choose your AI model
4. Select the action:
   - **Summary**: Get an AI-generated summary of the PDF content
   - **Q&A**: Ask questions about the PDF and get context-aware answers

## Architecture

### New Components for PDF Processing

#### `src/pdf_processor.py`
- Handles PDF text extraction using PyPDF
- Creates vector embeddings using Sentence Transformers
- Manages Chroma vector database for semantic search
- Retrieves relevant context for RAG queries

#### `src/rag_chain.py`
- Orchestrates the RAG pipeline for PDF summarization and Q&A
- Integrates with both Gemini and OpenAI models
- Manages context retrieval and prompt engineering
- Provides specialized prompts for different tasks

## Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **LLMs**: Google Gemini API, OpenAI GPT API
- **Video Processing**: youtube-transcript-api
- **PDF Processing**: PyPDF
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Database**: Chroma DB
- **RAG Framework**: LangChain
- **Environment**: Python-dotenv

## Contributing

Contributions are welcome from the community! Whether it's feedback, suggestions, or code improvements, your input is valuable. 

## Acknowledgments

- [Google Gemini](https://ai.google.dev/)
- [OpenAI GPT](https://help.openai.com/en/) 
- [LangChain](https://www.langchain.com/)
- [Chroma DB](https://www.trychroma.com/)
- [Krish Naik](https://www.youtube.com/user/krishnaik06)
