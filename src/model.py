import os
from dotenv import load_dotenv
from google import genai


class Model:

    @staticmethod
    def _validate_transcript(transcript: str) -> str | None:
        """Returns None if transcript is missing/invalid, else the transcript."""
        if not transcript or not isinstance(transcript, str):
            return None
        stripped = transcript.strip()
        if not stripped:
            return None
        return stripped

    @staticmethod
    def google_gemini(transcript, prompt, extra="", model_type="gemini-2.5-flash"):
        load_dotenv()

        # BUG FIX: validate transcript BEFORE sending to model
        clean_transcript = Model._validate_transcript(transcript)
        if clean_transcript is None:
            return "⚠️ No transcript was found for this video. Cannot generate a summary."

        try:
            client = genai.Client(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

            # BUG FIX: added clear separator so transcript doesn't bleed into prompt
            full_content = (
                f"{prompt}\n\n"
                f"{extra}\n\n"
                f"--- TRANSCRIPT START ---\n{clean_transcript}\n--- TRANSCRIPT END ---"
            )

            response = client.models.generate_content(
                model=model_type,
                contents=full_content,
            )
            return response.text

        except Exception as e:
            # BUG FIX: was returning a tuple (error_str, str(e)) — now returns plain string
            return f"⚠️ Gemini API error: {str(e)}"

    