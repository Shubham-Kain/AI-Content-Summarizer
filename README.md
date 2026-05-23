# AI Content Summarizer

AI Content Summarizer helps you turn long-form video and document content into concise, searchable knowledge. The project extracts text, creates embeddings, stores them locally in ChromaDB, and delivers summaries and question-answering across videos, audio files, and documents.

## Overview

This project is designed for users who need to quickly understand and explore long-form content without reading or watching everything. It supports:

- Transcription of local videos and audio sources
- Text extraction from documents
- Vector embeddings generation for semantic search
- Timestamped summaries for audio/video content
- Natural-language Q&A on video, audio, and document content

## Tech Stack

- Python 3.8+ / 3.13
- Streamlit for the demo UI (`app.py`)
- ChromaDB for local vector storage and retrieval
- OpenAI-compatible LLMs or other supported models for summarization and Q&A
- Speech-to-text processing for audio/video transcription
- Document parsing and text extraction utilities

## Setup

1. Clone the repository.
2. Create and activate a virtual environment:

```powershell
python -m venv myenv
myenv\Scripts\activate
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Run the app:

```powershell
streamlit run app.py
```

5. (Optional) Add API keys to a `.env` file if using external language models.

## Key Features

- **Video transcription**: Convert spoken content into text with timestamps.
- **Document summarization**: Extract and summarize text from PDF and document sources.
- **Semantic embeddings**: Build vector representations for efficient content search.
- **ChromaDB-backed storage**: Save and reuse embeddings locally for fast retrieval.
- **Timestamped summaries**: Generate concise summaries linked to audio/video segments.
- **Interactive Q&A**: Ask natural-language questions about videos, audio, or documents.

## Advantages

- **Save time**: Understand long content without consuming it fully.
- **Better discovery**: Find relevant facts and sections quickly with semantic search.
- **Multi-format support**: Work with video, audio, and documents in the same pipeline.
- **Reusable corpus**: Stored embeddings make your content searchable across sessions.
- **Flexible insights**: Use summaries, transcripts, and answers to explore content rapidly.
- **Local-first workflow**: Keep data and retrieval local with ChromaDB for efficiency and privacy.

## Project Structure

- `app.py` — main entry point and demo user interface
- `src/` — core modules for transcription, embeddings, RAG flow, document parsing, and formatting
- `chroma_db/` — local ChromaDB storage and database files
- `requirements.txt` — Python dependencies

## Notes

- Requires Python 3.8 or newer
- Configure any external model API keys in a `.env` file if needed
- `LICENSE` contains the project license information


