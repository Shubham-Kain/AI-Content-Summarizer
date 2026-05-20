# YouTube Video Q&A Feature

## Overview
The YouTube Video Q&A feature allows users to ask questions about YouTube video content. The system uses the video transcript and AI to provide accurate, context-aware answers based on what's discussed in the video.

## How It Works

### Architecture
1. **Transcript Extraction**: Video transcript is fetched from YouTube
2. **Question Processing**: User enters a question about the video
3. **RAG Pipeline**: Uses RAGChain's `answer_video_question()` method to:
   - Pass the transcript and question to the AI model
   - Include specialized prompts for video Q&A
   - Generate contextual answer
4. **Answer Display**: Show answer with copy/download functionality

### User Flow
1. Enter YouTube URL
2. Select "❓ Q&A" from video mode options
3. Generate transcript first (auto-generated or manual)
4. Type your question in the text field
5. Click "❓ Get Answer"
6. View the answer and download/copy as needed

## Technical Implementation

### New Components

#### 1. Prompt Template (src/prompt.py)
Added `video_qa` ID to the Prompt class:
```python
elif ID == "video_qa":
    prompt_text = """
You are a helpful video assistant that answers questions based on provided video transcript content.

TASK
Answer the user's question using ONLY the information from the provided video transcript.

RULES
- Answer based exclusively on the video transcript content
- If the answer is not found in the transcript, clearly state: "This information is not covered in the video."
- Provide clear, concise answers
- Use simple language
- Include relevant quotes or timestamps from the transcript when helpful
- Be accurate and truthful

STYLE
- Professional and helpful
- Conversational but informative
- Direct and easy to understand
"""
```

#### 2. RAGChain Method (src/rag_chain.py)
Implemented `answer_video_question()` method:
- Takes transcript and question as parameters
- Uses the `video_qa` prompt template
- Returns AI-generated answer based on transcript
- Includes error handling for missing transcripts

```python
def answer_video_question(self, transcript: str, question: str) -> str:
    """
    Answer a question about a YouTube video using its transcript.
    
    Args:
        transcript: Video transcript text
        question: User's question about the video
        
    Returns:
        Answer based on video transcript
    """
```

#### 3. UI Component (app.py)
Added `video_question_answering()` method:
- Modified video_mode radio button to include "❓ **Q&A**" option
- Checks if transcript is available before enabling Q&A
- Shows text input for user questions
- Displays answer with copy/download options
- Includes proper error handling and status updates

```python
def video_question_answering(self, loader_msg):
    """Answer questions about YouTube video content using transcript."""
```

## Features

### Input Handling
- ✅ Validates that transcript is available
- ✅ Checks for empty questions
- ✅ Shows helpful error messages

### Output Features
- ✅ Displays answers in formatted output box
- ✅ Copy to clipboard functionality
- ✅ Download answer as text file
- ✅ Session-based state management

### Error Handling
- ✅ Missing transcript warning
- ✅ Empty question validation
- ✅ API/model errors caught and displayed
- ✅ Graceful fallbacks

## Usage Examples

### Example 1: Technical Video Q&A
- **Video**: Python tutorial
- **Question**: "What are the main libraries discussed in this video?"
- **Answer**: AI extracts and summarizes library mentions from transcript

### Example 2: Educational Content
- **Video**: History lecture
- **Question**: "What were the key dates mentioned?"
- **Answer**: AI identifies and lists all important dates from transcript

### Example 3: Business/Conference Talk
- **Video**: Product launch presentation
- **Question**: "What are the main features of the new product?"
- **Answer**: AI summarizes product features mentioned in the talk

## Advantages

1. **Accurate**: Answers based on actual video content, not speculation
2. **Fast**: Instant answers without watching entire video
3. **Flexible**: Ask multiple questions about the same video
4. **Transparent**: Shows context from transcript
5. **Convenient**: No need to manually search transcript

## Limitations

1. **Depends on transcripts**: Works best with videos that have accurate transcripts
2. **Not all languages**: Depends on YouTube's subtitle availability
3. **Context length**: Very long videos might need transcript truncation (handled by AI model)
4. **No timestamps**: Current implementation doesn't highlight when answers occur in video

## Future Enhancements

1. **Timestamp Integration**: Return timestamp ranges for answers
2. **Multi-turn Q&A**: Continue conversation about video
3. **Summary + Q&A**: Pre-generate summary, then allow Q&A
4. **Source Citations**: Show exact quote from transcript for answers
5. **Speaker Detection**: Identify which speaker said what

## Troubleshooting

### Q: "Generate transcript first to enable Q&A"
**A**: Click on "**Transcript**" option first to fetch and display the transcript before asking questions.

### Q: Getting irrelevant answers
**A**: Make sure your question is specific and related to video content. Rephrase for clarity.

### Q: Transcript not available
**A**: Some videos don't have transcripts. Try a different video or check if closed captions are available.

### Q: Long wait times
**A**: Depending on AI model and transcript length, responses may take 10-30 seconds.

## Related Features

- **PDF Q&A**: Similar feature for PDF documents
- **Video Summary**: AI-generated summaries of video content
- **Timestamps**: Key moments extracted from videos
- **Transcript Export**: Download raw transcripts

## Version Info
- **Feature Added**: Current Release
- **Status**: Fully Implemented
- **Tested With**: Multiple YouTube video types
