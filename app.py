import streamlit as st
import os
from dotenv import load_dotenv
from src.video_info import GetVideo
from src.model import Model
from src.prompt import Prompt
from src.misc import Misc
from src.timestamp_formatter import TimestampFormatter
from src.copy_module_edit import ModuleEditor
from src.rag_chain import RAGChain
from st_copy_to_clipboard import st_copy_to_clipboard


# ── Caching wrappers ────────────────────────────────────────────────────────
# BUG FIX: GetVideo methods now RAISE exceptions, so these wrappers correctly
# return None on failure instead of forwarding error strings to the model.

@st.cache_data(show_spinner=False)
def get_transcript_cached(url):
    try:
        return GetVideo.transcript(url)
    except Exception as e:
        return None, str(e)        # (None, reason) tuple on failure


@st.cache_data(show_spinner=False)
def get_transcript_time_cached(url):
    try:
        return GetVideo.transcript_time(url)
    except Exception as e:
        return None, str(e)


def _unpack_transcript(result):
    """Return (transcript_str_or_None, error_str_or_None)."""
    if isinstance(result, tuple):
        return result[0], result[1]
    return result, None


# ── Main app ────────────────────────────────────────────────────────────────

class AIVideoSummarizer:

    def __init__(self):
        load_dotenv()

        # Video mode state
        self.youtube_url = None
        self.video_id = None
        self.video_title = None
        self.video_transcript = None
        self.video_transcript_time = None
        self.summary = None
        self.time_stamps = None
        self.transcript = None

        # PDF mode state
        self.pdf_file = None
        self.pdf_processor = None
        self.pdf_summary = None
        self.pdf_qa_answer = None

        self.model_name = None
        self.gemini_model_type = "gemini-2.5-flash"
        self.openai_model_type = "gpt-4o-mini"   # BUG FIX: gpt-5-nano doesn't exist

        self.model_env_checker = []

    # ── Styles ──────────────────────────────────────────────────────────────

    def _inject_styles(self):
        st.markdown("""
        <style>
        /* ── Typography ── */
        .main-title {
            text-align: center;
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 6px;
            letter-spacing: -1px;
        }
        .sub-title {
            text-align: center;
            font-size: 16px;
            opacity: 0.6;
            margin-bottom: 32px;
            font-weight: 400;
        }

        /* ── Cards ── */
        .card {
            padding: 22px;
            border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.08);
            background: rgba(255,255,255,0.03);
            margin-bottom: 16px;
        }

        /* ── Video title ── */
        .video-title {
            font-size: 20px;
            font-weight: 700;
            line-height: 1.4;
            margin-bottom: 12px;
        }

        /* ── Section headers ── */
        .section-header {
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            opacity: 0.5;
            margin-bottom: 8px;
        }

        /* ── Output box ── */
        .output-box {
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 12px;
            padding: 20px;
            background: rgba(102, 126, 234, 0.05);
            margin-top: 12px;
        }

        /* ── PDF Info Box ── */
        .pdf-info {
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: 12px;
            padding: 16px;
            background: rgba(245, 158, 11, 0.05);
            margin-top: 12px;
            margin-bottom: 12px;
        }

        .pdf-info-item {
            font-size: 14px;
            margin-bottom: 6px;
        }

        /* ── Badges ── */
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            background: rgba(102,126,234,0.15);
            color: #a78bfa;
            margin-bottom: 8px;
        }

        /* ── Error / warning ── */
        .err-box {
            background: rgba(239,68,68,0.08);
            border: 1px solid rgba(239,68,68,0.3);
            border-radius: 10px;
            padding: 14px 18px;
            color: #fca5a5;
            font-size: 14px;
        }

        /* ── Streamlit overrides ── */
        div[data-testid="stRadio"] label { font-size: 14px; }
        div[data-testid="stSelectbox"] label { font-size: 13px; font-weight: 600; }
        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .stButton > button:hover { transform: translateY(-1px); }
        div.stDownloadButton > button {
            border-radius: 10px;
            font-weight: 600;
        }
        </style>
        """, unsafe_allow_html=True)

    # ── Header ───────────────────────────────────────────────────────────────

    def header(self):
        self._inject_styles()
        st.markdown('<div class="main-title">🎬 AI Content Summarizer</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sub-title">Generate AI summaries, timestamps, transcripts from YouTube videos or PDF documents</div>',
            unsafe_allow_html=True,
        )

    # ── Sidebar / left panel ─────────────────────────────────────────────────

    def get_youtube_info(self):
        st.markdown('<div class="section-header">YouTube Link</div>', unsafe_allow_html=True)
        self.youtube_url = st.text_input(
            "Paste video URL",
            placeholder="https://youtube.com/watch?v=...",
            label_visibility="collapsed",
        )

        # Detect available models from env
        if os.getenv("GOOGLE_GEMINI_API_KEY"):
            self.model_env_checker.append("Gemini")
        if os.getenv("OPENAI_API_KEY"):
            self.model_env_checker.append("OpenAI")

        st.markdown("---")
        st.markdown('<div class="section-header">AI Model</div>', unsafe_allow_html=True)

        if not self.model_env_checker:
            st.warning("No API keys found in `.env`. Add `GOOGLE_GEMINI_API_KEY` or `OPENAI_API_KEY`.", icon="⚠️")
            st.stop()

        self.model_name = st.selectbox("Provider", self.model_env_checker, label_visibility="collapsed")

        if self.model_name == "Gemini":
            gemini_models = [
                "gemini-2.5-flash",
                "gemini-2.5-flash-lite",
                "gemini-3-flash-preview",
                "gemini-2.0-flash",
                "gemini-3.1-flash-lite",
                "Custom",
            ]
            selected = st.selectbox("Gemini Model", gemini_models)
            if selected == "Custom":
                self.gemini_model_type = st.text_input("Model name", placeholder="e.g. gemini-2.5-pro")
            else:
                self.gemini_model_type = selected

            if not self.gemini_model_type:
                st.warning("Enter a Gemini model name to continue.")
                st.stop()

        elif self.model_name == "OpenAI":
            openai_models = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "Custom"]
            selected = st.selectbox("OpenAI Model", openai_models)
            if selected == "Custom":
                self.openai_model_type = st.text_input("Model name", placeholder="e.g. gpt-4o")
            else:
                self.openai_model_type = selected

        # ── Video preview ────────────────────────────────────────────────────
        if self.youtube_url:
            self.video_id = GetVideo.Id(self.youtube_url)

            if self.video_id is None:
                st.error("❌ Invalid YouTube URL — please check the link.", icon="🔗")
                st.stop()

            st.markdown("---")
            with st.spinner("Loading video info…"):
                self.video_title = GetVideo.title(self.youtube_url)

            st.markdown(f'<div class="video-title">{self.video_title}</div>', unsafe_allow_html=True)
            st.video(self.youtube_url)

    # ── PDF Mode: Upload and Processing ──────────────────────────────────────

    def get_pdf_info(self):
        st.markdown('<div class="section-header">PDF Upload</div>', unsafe_allow_html=True)
        self.pdf_file = st.file_uploader(
            "Upload a PDF document",
            type="pdf",
            label_visibility="collapsed",
        )

        # Detect available models from env
        if os.getenv("GOOGLE_GEMINI_API_KEY"):
            if "Gemini" not in self.model_env_checker:
                self.model_env_checker.append("Gemini")
        if os.getenv("OPENAI_API_KEY"):
            if "OpenAI" not in self.model_env_checker:
                self.model_env_checker.append("OpenAI")

        st.markdown("---")
        st.markdown('<div class="section-header">AI Model</div>', unsafe_allow_html=True)

        if not self.model_env_checker:
            st.warning("No API keys found in `.env`. Add `GOOGLE_GEMINI_API_KEY` or `OPENAI_API_KEY`.", icon="⚠️")
            st.stop()

        self.model_name = st.selectbox("Provider", self.model_env_checker, label_visibility="collapsed", key="pdf_model")

        if self.model_name == "Gemini":
            gemini_models = [
                "gemini-2.5-flash",
                "gemini-2.5-flash-lite",
                "gemini-3-flash-preview",
                "gemini-2.0-flash",
                "gemini-3.1-flash-lite",
                "Custom",
            ]
            selected = st.selectbox("Gemini Model", gemini_models, key="pdf_gemini")
            if selected == "Custom":
                self.gemini_model_type = st.text_input("Model name", placeholder="e.g. gemini-2.5-pro", key="pdf_gemini_custom")
            else:
                self.gemini_model_type = selected

            if not self.gemini_model_type:
                st.warning("Enter a Gemini model name to continue.")
                st.stop()

        elif self.model_name == "OpenAI":
            openai_models = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "Custom"]
            selected = st.selectbox("OpenAI Model", openai_models, key="pdf_openai")
            if selected == "Custom":
                self.openai_model_type = st.text_input("Model name", placeholder="e.g. gpt-4o", key="pdf_openai_custom")
            else:
                self.openai_model_type = selected

        # ── PDF info display ─────────────────────────────────────────────────
        if self.pdf_file:
            st.markdown("---")
            pdf_name = self.pdf_file.name
            pdf_size_mb = self.pdf_file.size / (1024 * 1024)
            
            st.markdown(f'<div class="pdf-info"><div class="pdf-info-item"><strong>📄 File:</strong> {pdf_name}</div><div class="pdf-info-item"><strong>📊 Size:</strong> {pdf_size_mb:.2f} MB</div></div>', unsafe_allow_html=True)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _run_model(self, transcript, prompt, extra=""):
        """Calls the selected model and returns the response string."""
        if self.model_name == "Gemini":
            return Model.google_gemini(
                transcript=transcript,
                prompt=prompt,
                extra=extra,
                model_type=self.gemini_model_type,
            )
        return Model.openai_gpt(
            transcript=transcript,
            prompt=prompt,
            extra=extra,
            model_type=self.openai_model_type,
        )

    def _show_copy_download(self, text, filename):
        """Renders copy + download buttons side by side."""
        col1, col2 = st.columns(2)
        with col1:
            st_copy_to_clipboard(text, key=filename)
        with col2:
            st.download_button("⬇️ Download", text, file_name=filename, use_container_width=True)

    # ── Generate Summary ─────────────────────────────────────────────────────

    def generate_summary(self, loader_msg):
        if st.button("✨ Generate Summary", use_container_width=True, disabled=not self.youtube_url):

            with st.status(loader_msg, expanded=True) as status:

                status.update(label="📥 Fetching transcript…", state="running")
                raw = get_transcript_cached(self.youtube_url)
                transcript, err = _unpack_transcript(raw)

                # BUG FIX: surface transcript errors to user instead of silently
                # sending error text to the model (which caused hallucinated summaries)
                if not transcript:
                    status.update(label="Transcript fetch failed.", state="error")
                    st.error(
                        f"❌ Could not fetch transcript for this video.\n\n**Reason:** {err or 'Unknown error'}\n\n"
                        "Make sure the video has subtitles / captions enabled.",
                        icon="📋",
                    )
                    return

                status.update(label="🤖 Generating AI summary…", state="running")
                self.summary = self._run_model(transcript, Prompt.prompt1())
                status.update(label="✅ Summary ready!", state="complete")

            st.markdown("---")
            st.markdown("## 📄 Summary")
            st.markdown('<div class="output-box">', unsafe_allow_html=True)
            st.write(self.summary)
            st.markdown("</div>", unsafe_allow_html=True)
            self._show_copy_download(self.summary, f"{self.video_title}_summary.txt")

    # ── Generate Timestamps ──────────────────────────────────────────────────

    def generate_time_stamps(self, loader_msg):
        if st.button("⏱ Generate Timestamps", use_container_width=True, disabled=not self.youtube_url):

            with st.status(loader_msg, expanded=True) as status:

                status.update(label="📥 Fetching timed transcript…", state="running")
                raw = get_transcript_time_cached(self.youtube_url)
                transcript, err = _unpack_transcript(raw)

                if not transcript:
                    status.update(label="Transcript fetch failed.", state="error")
                    st.error(
                        f"❌ Could not fetch transcript.\n\n**Reason:** {err or 'Unknown error'}",
                        icon="📋",
                    )
                    return

                status.update(label="🤖 Generating timestamps…", state="running")
                youtube_url_full = f"https://youtube.com/watch?v={self.video_id}"
                self.time_stamps = self._run_model(
                    transcript,
                    Prompt.prompt1(ID="timestamp"),
                    extra=youtube_url_full,
                )
                status.update(label="✅ Timestamps ready!", state="complete")

            st.markdown("---")
            st.markdown("## ⏰ Timestamps")
            st.markdown(self.time_stamps)

            cp_text = TimestampFormatter.format(self.time_stamps)
            self._show_copy_download(cp_text, f"{self.video_title}_timestamps.txt")

    # ── Get Transcript ───────────────────────────────────────────────────────

    def generate_transcript(self, loader_msg):
        if st.button("📜 Get Transcript", use_container_width=True, disabled=not self.youtube_url):

            with st.status(loader_msg, expanded=True) as status:

                status.update(label="📥 Fetching transcript…", state="running")
                raw = get_transcript_cached(self.youtube_url)
                transcript, err = _unpack_transcript(raw)

                if not transcript:
                    status.update(label="Transcript fetch failed.", state="error")
                    st.error(
                        f"❌ Could not fetch transcript.\n\n**Reason:** {err or 'Unknown error'}",
                        icon="📋",
                    )
                    return

                self.transcript = transcript
                status.update(label="✅ Transcript ready!", state="complete")

            st.markdown("---")
            st.markdown("## 📜 Transcript")

            # BUG FIX: was calling download_button with potentially None transcript
            self._show_copy_download(self.transcript, f"{self.video_title}_transcript.txt")
            st.text_area("Full Transcript", self.transcript, height=420, label_visibility="collapsed")

    # ── PDF Mode: Generate Summary ───────────────────────────────────────────

    def generate_pdf_summary(self, loader_msg):
        if st.button("✨ Generate Summary", use_container_width=True, disabled=not self.pdf_file, key="pdf_summary_btn"):

            with st.status(loader_msg, expanded=True) as status:

                status.update(label="📥 Processing PDF…", state="running")
                rag_chain = RAGChain(
                    model_name=self.model_name,
                    gemini_model=self.gemini_model_type,
                    openai_model=self.openai_model_type,
                )

                result = rag_chain.initialize_with_pdf(self.pdf_file, self.pdf_file.name)

                if not result["success"]:
                    status.update(label="PDF processing failed.", state="error")
                    st.error(f"❌ Error: {result['error']}", icon="📋")
                    return

                status.update(label="🤖 Generating AI summary…", state="running")
                self.pdf_summary = rag_chain.generate_pdf_summary(summary_type="comprehensive")
                status.update(label="✅ Summary ready!", state="complete")

            st.markdown("---")
            st.markdown("## 📄 PDF Summary")
            st.markdown('<div class="output-box">', unsafe_allow_html=True)
            st.write(self.pdf_summary)
            st.markdown("</div>", unsafe_allow_html=True)
            self._show_copy_download(self.pdf_summary, f"{self.pdf_file.name}_summary.txt")

    # ── PDF Mode: Q&A ────────────────────────────────────────────────────────

    def pdf_question_answering(self):
        if not self.pdf_file:
            st.info("Upload a PDF to enable Q&A", icon="ℹ️")
            return

        st.markdown('<div class="section-header">Ask a Question</div>', unsafe_allow_html=True)
        user_question = st.text_input(
            "Ask something about the PDF",
            placeholder="What is the main topic of this document?",
            label_visibility="collapsed",
        )

        if st.button("❓ Get Answer", use_container_width=True):
            with st.status("Processing question…", expanded=True) as status:

                status.update(label="📥 Processing PDF…", state="running")
                rag_chain = RAGChain(
                    model_name=self.model_name,
                    gemini_model=self.gemini_model_type,
                    openai_model=self.openai_model_type,
                )

                result = rag_chain.initialize_with_pdf(self.pdf_file, self.pdf_file.name)

                if not result["success"]:
                    status.update(label="PDF processing failed.", state="error")
                    st.error(f"❌ Error: {result['error']}", icon="📋")
                    return

                status.update(label="🤖 Finding answer…", state="running")
                self.pdf_qa_answer = rag_chain.answer_question(user_question)
                status.update(label="✅ Answer ready!", state="complete")

            st.markdown("---")
            st.markdown("## 💬 Answer")
            st.markdown('<div class="output-box">', unsafe_allow_html=True)
            st.write(self.pdf_qa_answer)
            st.markdown("</div>", unsafe_allow_html=True)

    # ── Main entry ───────────────────────────────────────────────────────────

    def run(self):
        st.set_page_config(
            page_title="AI Content Summarizer",
            page_icon="🎬",
            layout="wide",
        )

        try:
            editor = ModuleEditor("st_copy_to_clipboard")
            editor.modify_frontend_files()
        except Exception:
            pass   # Don't crash if the module isn't installed

        n, loader = Misc.loaderx()

        self.header()

        # ── Mode Selection ───────────────────────────────────────────────────
        mode = st.radio(
            "Choose Mode",
            ["📺 YouTube Video", "📄 PDF Document"],
            horizontal=True,
            label_visibility="collapsed",
        )

        st.divider()

        # ── YouTube Video Mode ───────────────────────────────────────────────
        if mode == "📺 YouTube Video":
            left, right = st.columns([1, 1.3], gap="large")

            with left:
                self.get_youtube_info()

            with right:
                st.markdown("### ⚡ Generate")

                video_mode = st.radio(
                    "Output type",
                    [":rainbow[**AI Summary**]", ":rainbow[**AI Timestamps**]", "**Transcript**"],
                    horizontal=True,
                    label_visibility="collapsed",
                )

                st.divider()

                if video_mode == ":rainbow[**AI Summary**]":
                    self.generate_summary(loader[n])
                elif video_mode == ":rainbow[**AI Timestamps**]":
                    self.generate_time_stamps(loader[n])
                else:
                    self.generate_transcript(loader[0])

        # ── PDF Document Mode ────────────────────────────────────────────────
        else:
            left, right = st.columns([1, 1.3], gap="large")

            with left:
                self.get_pdf_info()

            with right:
                st.markdown("### ⚡ Generate")

                pdf_mode = st.radio(
                    "PDF Feature",
                    ["✨ **Summary**", "❓ **Q&A**"],
                    horizontal=True,
                    label_visibility="collapsed",
                )

                st.divider()

                if pdf_mode == "✨ **Summary**":
                    self.generate_pdf_summary(loader[n])
                else:
                    self.pdf_question_answering()

        st.divider()
        st.write(Misc.footer(), unsafe_allow_html=True)


if __name__ == "__main__":
    app = AIVideoSummarizer()
    app.run()