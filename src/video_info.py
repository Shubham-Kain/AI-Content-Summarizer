from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
import requests
import re


class GetVideo:

    @staticmethod
    def Id(link):
        """Extracts the video ID from a YouTube video link."""
        pattern = r"(?:v=|youtu\.be/)([0-9A-Za-z_-]{11})"
        match = re.search(pattern, link)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def title(link):
       """Gets the title of a YouTube video via the oEmbed API (reliable on cloud/server IPs)."""
       video_id = GetVideo.Id(link)
       if not video_id:
           return "Unknown Title"
       try:
          oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
          r = requests.get(oembed_url, timeout=10)
          r.raise_for_status()
          return r.json().get("title", "Unknown Title")
       except Exception:
        # Fallback: try the old scrape method (works if oEmbed is ever unavailable)
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(link, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            title_tag = soup.find("meta", itemprop="name")
            if title_tag and title_tag.get("content"):
                return title_tag["content"]
            og_title = soup.find("meta", property="og:title")
            if og_title and og_title.get("content"):
                return og_title["content"]
        except Exception:
            pass
        return "Unknown Title"

    @staticmethod
    def transcript(link):
        """
        Gets the plain transcript of a YouTube video.
        RAISES exceptions so the caching wrapper can return None properly.
        """
        video_id = GetVideo.Id(link)
        if not video_id:
            raise ValueError("Invalid YouTube link — could not extract video ID.")

        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        # Try manual English first, then fall back to any auto-generated
        try:
            transcript = transcript_list.find_transcript(["en","hi"])
        except Exception:
            try:
                transcript = transcript_list.find_generated_transcript(["en","hi"])
            except Exception:
                # Last resort: grab the first available transcript
                available = list(transcript_list)
                if not available:
                    raise RuntimeError("No transcript available for this video.")
                transcript = available[0]

        transcript_data = transcript.fetch()
        final_transcript = " ".join(snippet.text for snippet in transcript_data)

        if not final_transcript.strip():
            raise RuntimeError("Transcript is empty.")

        return final_transcript

    @staticmethod
    def transcript_time(link):
        """
        Gets transcript with timestamps.
        RAISES exceptions so the caching wrapper can return None properly.
        """
        video_id = GetVideo.Id(link)
        if not video_id:
            raise ValueError("Invalid YouTube link — could not extract video ID.")

        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        # BUG FIX: was missing fallback to auto-generated transcript
        try:
            transcript = transcript_list.find_transcript(["en","hi"])
        except Exception:
            try:
                transcript = transcript_list.find_generated_transcript(["en","hi"])
            except Exception:
                available = list(transcript_list)
                if not available:
                    raise RuntimeError("No transcript available for this video.")
                transcript = available[0]

        transcript_data = transcript.fetch()

        final_transcript = ""
        for snippet in transcript_data:
            seconds = int(snippet.start)
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            sec = seconds % 60
            timestamp = f"{hours:02d}:{minutes:02d}:{sec:02d}"
            final_transcript += f"{snippet.text} (time:{timestamp}) "

        if not final_transcript.strip():
            raise RuntimeError("Transcript is empty.")

        return final_transcript