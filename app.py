import hashlib
import fitz
import streamlit as st

from modules.preprocessing import clean_text, split_into_sentences
from modules.text_chunker import create_chunks
from modules.summarizer import summarize_text
from modules.keyphrase_extractor import extract_keyphrases
from modules.question_generator import generate_questions


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="PaperCraft AI | Learning Workspace",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# PREMIUM DASHBOARD THEME
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #080c18;
        --panel: #11182b;
        --panel-2: #151e34;
        --border: rgba(154, 166, 195, .16);
        --purple: #8b5cf6;
        --purple-light: #b6a0ff;
        --cyan: #67e8f9;
        --text: #f3f4ff;
        --muted: #9aa7c4;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        color: var(--text);
        background:
            radial-gradient(ellipse at 12% 0%, rgba(91, 57, 177, .22), transparent 32%),
            radial-gradient(ellipse at 100% 18%, rgba(14, 116, 144, .12), transparent 28%),
            var(--bg);
    }

    [data-testid="stHeader"] {
        background: rgba(8, 12, 24, .82);
        backdrop-filter: blur(14px);
    }

    [data-testid="stAppViewContainer"] { background: transparent; }

    .block-container {
        max-width: 1500px;
        padding-top: 1.7rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0e1425 0%, #0b1020 100%);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] > div:first-child { padding-top: 1.25rem; }

    h1, h2, h3, h4 {
        color: var(--text) !important;
        font-family: 'Manrope', sans-serif;
        letter-spacing: -.035em;
    }

    p, li, label, .stMarkdown { color: #d5dcf1; }
    [data-testid="stCaptionContainer"] { color: var(--muted) !important; }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 3px 2px 20px;
    }

    .brand-icon {
        width: 48px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 15px;
        background: linear-gradient(135deg, #a78bfa, #6845e8);
        box-shadow: 0 8px 28px rgba(139, 92, 246, .32);
        font-size: 24px;
    }

    .brand-name {
        color: #fff;
        font-family: 'Manrope', sans-serif;
        font-size: 1.12rem;
        font-weight: 800;
        line-height: 1.2;
    }

    .brand-subtitle {
        color: #8998ba;
        font-size: .68rem;
        letter-spacing: .14em;
        margin-top: 5px;
    }

    .sidebar-label {
        color: #8492b4;
        font-size: .68rem;
        font-weight: 800;
        letter-spacing: .15em;
        text-transform: uppercase;
        margin: 18px 0 8px;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: clamp(26px, 4vw, 48px);
        border: 1px solid rgba(167, 139, 250, .25);
        border-radius: 26px;
        margin-bottom: 25px;
        background:
            radial-gradient(circle at 88% 12%, rgba(139, 92, 246, .25), transparent 34%),
            radial-gradient(circle at 100% 100%, rgba(34, 211, 238, .08), transparent 35%),
            linear-gradient(135deg, rgba(24, 27, 55, .98), rgba(16, 24, 43, .98) 68%, rgba(12, 32, 47, .98));
        box-shadow: 0 20px 65px rgba(0, 0, 0, .22);
        animation: fadeUp .55s ease-out both;
    }

    .hero:after {
        content: "✦";
        position: absolute;
        right: 7%;
        top: 18%;
        color: rgba(196, 181, 253, .18);
        font-size: clamp(90px, 12vw, 180px);
        line-height: 1;
        pointer-events: none;
    }

    .hero-eyebrow {
        color: #c4b5fd;
        font-size: .73rem;
        font-weight: 800;
        letter-spacing: .17em;
        text-transform: uppercase;
        margin-bottom: 15px;
    }

    .hero-title {
        color: #fff;
        font-family: 'Manrope', sans-serif;
        font-size: clamp(2rem, 4.2vw, 3.25rem);
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -.055em;
        max-width: 800px;
        margin-bottom: 16px;
        position: relative;
        z-index: 1;
    }

    .hero-description {
        color: #b0bdd8;
        font-size: 1rem;
        line-height: 1.75;
        max-width: 700px;
        margin: 0;
        position: relative;
        z-index: 1;
    }

    .eyebrow {
        color: #b6a0ff;
        font-size: .7rem;
        font-weight: 800;
        letter-spacing: .16em;
        text-transform: uppercase;
        margin-bottom: 7px;
    }

    .section-subtitle {
        color: #98a7c8;
        font-size: .92rem;
        margin-top: -5px;
        margin-bottom: 18px;
    }

    .metric-card {
        background: linear-gradient(145deg, rgba(24, 34, 58, .96), rgba(16, 24, 42, .96));
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 19px 20px;
        min-height: 138px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, .12);
        transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;
        animation: fadeUp .5s ease-out both;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(167, 139, 250, .48);
        box-shadow: 0 14px 35px rgba(80, 48, 160, .13);
    }

    .metric-icon { font-size: 1.35rem; margin-bottom: 12px; }
    .metric-label {
        color: #95a3c3;
        font-size: .72rem;
        font-weight: 800;
        letter-spacing: .1em;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #f7f7ff;
        font-family: 'Manrope', sans-serif;
        font-size: clamp(1.55rem, 2.5vw, 2.1rem);
        line-height: 1.05;
        font-weight: 800;
    }

    .upload-panel {
        background: linear-gradient(145deg, rgba(20, 29, 50, .88), rgba(15, 22, 39, .88));
        border: 1px solid rgba(139, 92, 246, .35);
        border-radius: 19px;
        padding: 19px 20px 8px;
        margin: 14px 0 18px;
    }

    .status-pill {
        display: inline-block;
        border: 1px solid rgba(52, 211, 153, .28);
        color: #6ee7b7;
        background: rgba(16, 185, 129, .08);
        border-radius: 999px;
        padding: 6px 11px;
        font-size: .75rem;
        font-weight: 700;
    }

    .stButton > button, .stDownloadButton > button {
        border-radius: 11px;
        min-height: 43px;
        font-weight: 700;
        transition: all .2s ease;
        border: 1px solid rgba(154, 166, 195, .24);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #8b5cf6, #6945df);
        color: #fff;
        border: 1px solid rgba(196, 181, 253, .6);
        box-shadow: 0 7px 22px rgba(139, 92, 246, .2);
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #a78bfa, #7c5cf0);
        border-color: #c4b5fd;
        transform: translateY(-1px);
        box-shadow: 0 10px 26px rgba(139, 92, 246, .28);
    }

    .stDownloadButton > button {
        background: #1a2540;
        color: #e4ddff;
        border-color: rgba(139, 92, 246, .35);
    }

    .stDownloadButton > button:hover {
        background: #29254b;
        color: white;
        border-color: #a78bfa;
    }

    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        background: #10192c !important;
        color: #edf0ff !important;
        border: 1px solid #34415f !important;
        border-radius: 10px !important;
    }

    [data-baseweb="select"] > div {
        background: #10192c;
        border-color: #34415f;
        border-radius: 10px;
        color: #edf0ff;
    }

    [data-testid="stFileUploader"] {
        background: rgba(20, 29, 50, .6);
        border: 1px dashed rgba(167, 139, 250, .6);
        border-radius: 15px;
        padding: 10px;
    }
    [data-testid="stFileUploader"] section { background: transparent; }

    [data-testid="stTabs"] [role="tablist"] {
        gap: 8px;
        border-bottom: 1px solid var(--border);
    }

    [data-testid="stTabs"] button[role="tab"] {
        background: transparent;
        border-radius: 11px 11px 0 0;
        padding: 12px 15px;
        color: #9aa7c4;
        font-weight: 700;
    }

    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        color: #d7c9ff;
        background: rgba(139, 92, 246, .12);
        border-bottom: 2px solid #a78bfa;
    }

    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #8b5cf6, #67e8f9);
    }

    [data-testid="stExpander"] {
        background: rgba(17, 26, 45, .72);
        border: 1px solid var(--border);
        border-radius: 12px;
    }

    [data-testid="stAlert"] { border-radius: 12px; }

    .result-card {
        background: linear-gradient(145deg, rgba(22, 31, 53, .9), rgba(16, 23, 40, .9));
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 16px 18px;
        margin: 8px 0;
    }

    .footer {
        color: #7180a1;
        text-align: center;
        font-size: .78rem;
        padding: 18px 0 5px;
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(9px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @media (max-width: 768px) {
        .block-container { padding: 1rem 1rem 2rem; }
        .hero { padding: 25px; border-radius: 19px; }
        .metric-card { padding: 15px; min-height: 115px; }
        .hero:after { right: 2%; top: 5%; font-size: 85px; }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: .01ms !important;
            transition-duration: .01ms !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================
defaults = {
    "summaries": [],
    "keyphrases": [],
    "questions": [],
    "document_name": "",
    "document_signature": None,
    "cleaned_text": "",
    "chunks": [],
    "page_count": 0,
    "active_workspace": "Overview",
}
for key, default in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown(
        """
        <div class="brand-row">
            <div class="brand-icon">📚</div>
            <div>
                <div class="brand-name">PaperCraft AI</div>
                <div class="brand-subtitle">INTELLIGENT LEARNING SPACE</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown('<div class="sidebar-label">Workspace</div>', unsafe_allow_html=True)

    page = st.radio(
        "Navigate workspace",
        [
            "Overview",
            "Document analysis",
            "AI summaries",
            "Keyphrase extraction",
            "Question generation",
            "Paper studio",
        ],
        label_visibility="collapsed",
        key="active_workspace",
    )

    st.divider()
    st.markdown('<div class="sidebar-label">Your workflow</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="color:#9aa7c4;line-height:2.05;font-size:.86rem;">
        <div>① &nbsp; Upload a textbook PDF</div>
        <div>② &nbsp; Analyze and summarize</div>
        <div>③ &nbsp; Generate practice questions</div>
        <div>④ &nbsp; Prepare your question paper</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.caption("Built with Python, Streamlit & NLP")


# =========================================================
# HERO
# =========================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-eyebrow">✦ YOUR AI-POWERED STUDY ASSISTANT</div>
        <div class="hero-title">Turn knowledge into questions.</div>
        <p class="hero-description">
            Transform textbook PDFs into concise summaries, important concepts,
            practice questions and a ready-to-preview question paper — all in one workspace.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# PDF UPLOAD AND PROCESSING
# =========================================================
top_left, top_right = st.columns([1.7, 1], gap="large")
with top_left:
    st.markdown('<div class="eyebrow">START YOUR WORKSPACE</div>', unsafe_allow_html=True)
    st.markdown("### Upload your learning material")
    st.markdown(
        '<div class="section-subtitle">Choose a text-based PDF to begin analyzing your textbook.</div>',
        unsafe_allow_html=True,
    )
with top_right:
    if st.session_state["document_name"]:
        st.markdown(
            f'<div style="text-align:right;padding-top:16px;"><span class="status-pill">● Document loaded</span></div>',
            unsafe_allow_html=True,
        )

st.markdown('<div class="upload-panel">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Drop your textbook PDF here or browse files",
    type=["pdf"],
    help="Use a PDF with selectable text. Scanned PDFs may need OCR.",
)
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file is not None:
    pdf_bytes = uploaded_file.getvalue()
    document_signature = (
        uploaded_file.name,
        len(pdf_bytes),
        hashlib.md5(pdf_bytes).hexdigest(),
    )

    if document_signature != st.session_state["document_signature"]:
        for key in ["summaries", "keyphrases", "questions"]:
            st.session_state[key] = []

        try:
            with st.spinner("Reading your textbook and preparing the workspace..."):
                document = fitz.open(stream=pdf_bytes, filetype="pdf")
                try:
                    extracted_parts = [page.get_text() for page in document]
                    page_count = len(document)
                finally:
                    document.close()

                extracted_text = "\n".join(extracted_parts)
                if extracted_text.strip():
                    cleaned_text = clean_text(extracted_text)
                    sentences = split_into_sentences(cleaned_text)
                    chunks = create_chunks(sentences, max_words=180)
                else:
                    cleaned_text = ""
                    chunks = []

            st.session_state["document_signature"] = document_signature
            st.session_state["document_name"] = uploaded_file.name
            st.session_state["cleaned_text"] = cleaned_text
            st.session_state["chunks"] = chunks
            st.session_state["page_count"] = page_count

        except Exception as exc:
            st.error(f"Unable to process this PDF: {exc}")
            st.stop()

elif not st.session_state["document_name"]:
    st.info("📂 Upload a textbook PDF to unlock your learning workspace.")

# Use processed document from session state so navigation between sections works.
cleaned_text = st.session_state["cleaned_text"]
chunks = st.session_state["chunks"]
has_document = bool(cleaned_text.strip())

if has_document:
    word_count = len(cleaned_text.split())
    metrics = st.columns(4)
    metric_data = [
        ("📄", "PDF PAGES", st.session_state["page_count"]),
        ("✍️", "WORD COUNT", f"{word_count:,}"),
        ("🧩", "TEXT SEGMENTS", len(chunks)),
        ("❓", "QUESTIONS CREATED", len(st.session_state["questions"])),
    ]
    for col, (icon, label, value) in zip(metrics, metric_data):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-icon">{icon}</div>
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("")
    st.success(f"Ready to work with **{st.session_state['document_name']}**")

    with st.expander("View extracted text and processing details"):
        st.markdown("#### Cleaned textbook content")
        st.text_area(
            "Preprocessed content",
            value=cleaned_text,
            height=220,
            disabled=True,
            label_visibility="collapsed",
        )
        st.markdown(f"#### Text segments ({len(chunks)})")
        for i, chunk in enumerate(chunks, start=1):
            with st.expander(f"Segment {i}"):
                st.write(chunk)

    if not chunks:
        st.warning("No usable text segments were created from this PDF.")
elif uploaded_file is not None:
    st.error(
        "No selectable text was found in this PDF. If it contains scanned pages, OCR will be needed."
    )


# =========================================================
# OVERVIEW PAGE
# =========================================================
if page == "Overview":
    st.markdown("---")
    st.markdown('<div class="eyebrow">YOUR AI TOOLKIT</div>', unsafe_allow_html=True)
    st.markdown("### Everything you need to study smarter")
    st.markdown(
        '<div class="section-subtitle">Choose a workspace from the sidebar to get started.</div>',
        unsafe_allow_html=True,
    )
    cards = st.columns(2, gap="large")
    overview_cards = [
        ("📄", "Document analysis", "Extract text, review document statistics and inspect text segments."),
        ("📝", "AI summaries", "Condense textbook sections into easier-to-review notes."),
        ("🔑", "Keyphrase extraction", "Find important terms and concepts in the material."),
        ("❓", "Question generation", "Build a practice question bank from the uploaded textbook."),
    ]
    for col, (icon, title, description) in zip([cards[0], cards[1], cards[0], cards[1]], overview_cards):
        with col:
            st.markdown(
                f"""
                <div class="result-card" style="min-height:125px;">
                    <div style="font-size:1.5rem;margin-bottom:8px;">{icon}</div>
                    <div style="font-size:1.03rem;font-weight:800;color:#f4f3ff;margin-bottom:6px;">{title}</div>
                    <div style="font-size:.88rem;line-height:1.6;color:#9aa7c4;">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    if not has_document:
        st.markdown(
            """
            <div class="result-card">
                <div class="eyebrow">READY WHEN YOU ARE</div>
                <h3 style="margin:6px 0 8px;">Your next question starts with a page.</h3>
                <div style="color:#9aa7c4;">Upload a textbook PDF above to see document insights and create learning materials.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# DOCUMENT ANALYSIS PAGE
# =========================================================
elif page == "Document analysis":
    st.markdown('<div class="eyebrow">DOCUMENT INTELLIGENCE</div>', unsafe_allow_html=True)
    st.markdown("### Document analysis")
    st.markdown('<div class="section-subtitle">Inspect the extracted and preprocessed text from your textbook.</div>', unsafe_allow_html=True)
    if has_document:
        st.write(f"**File:** {st.session_state['document_name']}")
        st.write(f"**Pages:** {st.session_state['page_count']}  ·  **Words:** {len(cleaned_text.split()):,}  ·  **Segments:** {len(chunks)}")
        st.text_area("Extracted and cleaned text", value=cleaned_text, height=350, disabled=True)
        st.download_button(
            "⬇️ Download extracted text",
            data=cleaned_text,
            file_name="extracted_text.txt",
            mime="text/plain",
            use_container_width=False,
        )
    else:
        st.info("Upload a PDF above to analyze its contents.")


# =========================================================
# AI SUMMARIES PAGE
# =========================================================
elif page == "AI summaries":
    st.markdown('<div class="eyebrow">QUICK REVISION</div>', unsafe_allow_html=True)
    st.markdown("### AI-generated summaries")
    st.markdown('<div class="section-subtitle">Extract the main ideas from each textbook segment.</div>', unsafe_allow_html=True)

    if not has_document:
        st.info("Upload a PDF above before generating summaries.")
    else:
        if st.button("✨ Generate summaries", type="primary", use_container_width=True):
            summaries = []
            if not chunks:
                st.warning("No text segments are available.")
            else:
                progress = st.progress(0)
                status = st.empty()
                try:
                    for i, chunk in enumerate(chunks):
                        status.caption(f"Summarizing segment {i + 1} of {len(chunks)}...")
                        summary = summarize_text(chunk)
                        if summary:
                            summaries.append(summary)
                        progress.progress((i + 1) / len(chunks))
                    st.session_state["summaries"] = summaries
                except Exception as exc:
                    st.error(f"Summary generation failed: {exc}")
                finally:
                    status.empty()
                    progress.empty()

                if st.session_state["summaries"]:
                    st.success("Summaries generated successfully.")
                else:
                    st.warning("No summaries were returned. Check your summarizer module.")

        summaries = st.session_state["summaries"]
        if summaries:
            st.caption(f"{len(summaries)} summaries available")
            for i, summary in enumerate(summaries, start=1):
                with st.container(border=True):
                    st.markdown(f"**Summary {i:02d}**")
                    st.write(summary)
            summary_text = "\n\n".join(
                f"Summary {i}\n{summary}" for i, summary in enumerate(summaries, start=1)
            )
            st.download_button(
                "⬇️ Download summaries",
                data=summary_text,
                file_name="textbook_summaries.txt",
                mime="text/plain",
            )
        else:
            st.info("Generate summaries to see the key ideas from your textbook.")


# =========================================================
# KEYPHRASE EXTRACTION PAGE
# =========================================================
elif page == "Keyphrase extraction":
    st.markdown('<div class="eyebrow">IMPORTANT CONCEPTS</div>', unsafe_allow_html=True)
    st.markdown("### Keyphrase extraction")
    st.markdown('<div class="section-subtitle">Discover important concepts and terms from your textbook.</div>', unsafe_allow_html=True)

    if not has_document:
        st.info("Upload a PDF above before extracting keyphrases.")
    else:
        top_n = st.slider("Keyphrases to extract per segment", 3, 10, 5)
        if st.button("🔑 Extract keyphrases", type="primary", use_container_width=True):
            all_keyphrases = []
            progress = st.progress(0)
            try:
                for i, chunk in enumerate(chunks):
                    phrases = extract_keyphrases(chunk, top_n=top_n)
                    all_keyphrases.extend(phrases)
                    progress.progress((i + 1) / max(len(chunks), 1))

                unique_phrases = {}
                for item in all_keyphrases:
                    phrase = item.get("phrase", "").strip()
                    if phrase and phrase.lower() not in unique_phrases:
                        unique_phrases[phrase.lower()] = item
                st.session_state["keyphrases"] = list(unique_phrases.values())
                st.success("Keyphrase extraction completed.")
            except Exception as exc:
                st.error(f"Keyphrase extraction failed: {exc}")
            finally:
                progress.empty()

        keyphrases = st.session_state["keyphrases"]
        if keyphrases:
            st.caption(f"{len(keyphrases)} unique keyphrases found")
            columns = st.columns(2)
            for i, item in enumerate(keyphrases):
                with columns[i % 2]:
                    with st.container(border=True):
                        st.markdown(f"**🔑 {item.get('phrase', 'Untitled phrase')}**")
                        score = item.get("score", "N/A")
                        if isinstance(score, (int, float)):
                            st.caption(f"Relevance score: {score:.3f}")
                        else:
                            st.caption(f"Relevance score: {score}")
            st.download_button(
                "⬇️ Download keyphrases",
                data="\n".join(item.get("phrase", "") for item in keyphrases),
                file_name="important_keyphrases.txt",
                mime="text/plain",
            )
        else:
            st.info("Extract keyphrases to discover important textbook concepts.")


# =========================================================
# QUESTION GENERATION PAGE
# =========================================================
elif page == "Question generation":
    st.markdown('<div class="eyebrow">PRACTICE MAKES PROGRESS</div>', unsafe_allow_html=True)
    st.markdown("### Question generation")
    st.markdown('<div class="section-subtitle">Build a practice question bank from your learning material.</div>', unsafe_allow_html=True)

    if not has_document:
        st.info("Upload a PDF above before generating questions.")
    else:
        number_of_questions = st.slider("Questions per text segment", 1, 5, 3)
        if st.button("✨ Generate questions", type="primary", use_container_width=True):
            all_questions = []
            progress = st.progress(0)
            try:
                for i, chunk in enumerate(chunks):
                    generated = generate_questions(chunk, max_questions=number_of_questions)
                    all_questions.extend(generated)
                    progress.progress((i + 1) / max(len(chunks), 1))

                unique_questions = []
                seen_questions = set()
                for question in all_questions:
                    normalized = question.strip().lower()
                    if normalized and normalized not in seen_questions:
                        seen_questions.add(normalized)
                        unique_questions.append(question.strip())
                st.session_state["questions"] = unique_questions
                st.success(f"Generated {len(unique_questions)} unique questions.")
            except Exception as exc:
                st.error(f"Question generation failed: {exc}")
            finally:
                progress.empty()

        questions = st.session_state["questions"]
        if questions:
            st.caption(f"{len(questions)} questions in your question bank")
            for i, question in enumerate(questions, start=1):
                with st.container(border=True):
                    st.markdown(f"**Q{i:02d}.** {question}")
            st.download_button(
                "⬇️ Download questions",
                data="\n".join(f"Q{i}. {q}" for i, q in enumerate(questions, start=1)),
                file_name="generated_questions.txt",
                mime="text/plain",
            )
        else:
            st.info("Generate questions to start building your question bank.")


# =========================================================
# QUESTION PAPER STUDIO
# =========================================================
elif page == "Paper studio":
    st.markdown('<div class="eyebrow">READY-TO-PRINT EXAM DESIGN</div>', unsafe_allow_html=True)
    st.markdown("### Question paper studio")
    st.markdown('<div class="section-subtitle">Customize the exam details and preview your question paper.</div>', unsafe_allow_html=True)

    left, right = st.columns([1, 1.2], gap="large")
    with left:
        st.markdown("#### Exam settings")
        subject = st.text_input("Subject name", placeholder="e.g. Natural Language Processing", key="paper_subject")
        exam_title = st.text_input("Examination title", value="Model Question Paper", key="paper_title")
        duration = st.selectbox("Examination duration", ["1 Hour", "2 Hours", "3 Hours"], key="paper_duration")
        marks_per_question = st.number_input("Marks per question", min_value=1, max_value=20, value=2, key="paper_marks")
        instructions = st.text_area("Exam instructions", value="Answer all questions.", height=100, key="paper_instructions")

    questions = st.session_state["questions"]
    with right:
        st.markdown("#### Live paper preview")
        if questions:
            total_marks = len(questions) * marks_per_question
            with st.container(border=True):
                st.markdown(
                    f'<div class="eyebrow">{exam_title}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(f"## {subject or 'Subject not specified'}")
                st.caption(f"Duration: {duration}  ·  Total marks: {total_marks}")
                st.divider()
                st.markdown("**Instructions**")
                st.write(instructions or "No instructions provided.")
                st.divider()
                for i, question in enumerate(questions, start=1):
                    st.markdown(f"**{i}.** {question}  \n*[{marks_per_question} marks]*")

            paper_text = (
                f"{exam_title}\n"
                f"Subject: {subject or 'Subject not specified'}\n"
                f"Duration: {duration}\n"
                f"Total marks: {total_marks}\n\n"
                f"Instructions: {instructions}\n\n"
                + "\n".join(
                    f"{i}. {question} ({marks_per_question} marks)"
                    for i, question in enumerate(questions, start=1)
                )
            )
            st.download_button(
                "⬇️ Download question paper",
                data=paper_text,
                file_name="question_paper.txt",
                mime="text/plain",
                type="primary",
                use_container_width=True,
            )
        else:
            st.info("Generate questions in the Question generation section to preview a paper.")


# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.markdown(
    """
    <div class="footer">
        📚 PaperCraft AI · Intelligent Question Paper Generation<br>
        Designed for focused learning with Python, Streamlit and NLP
    </div>
    """,
    unsafe_allow_html=True,
)
