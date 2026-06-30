from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ExtractIQ",
    page_icon="🔍",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

/* ── Base reset ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0A0A0F !important;
    color: #E8E6F0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none; }
.block-container { max-width: 780px !important; padding: 2.5rem 1.5rem 4rem !important; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2.5rem;
    border-bottom: 1px solid #1E1E2E;
    margin-bottom: 2.5rem;
}
.hero-badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #7C6AF7;
    background: rgba(124, 106, 247, 0.1);
    border: 1px solid rgba(124, 106, 247, 0.25);
    border-radius: 100px;
    padding: 0.3rem 0.9rem;
    margin-bottom: 1.1rem;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin: 0 0 0.6rem;
    background: linear-gradient(135deg, #E8E6F0 0%, #7C6AF7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 0.95rem;
    color: #6B6880;
    font-weight: 400;
    letter-spacing: 0.01em;
}

/* ── Textarea label ── */
.input-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #7C6AF7;
    margin-bottom: 0.5rem;
}

/* ── Streamlit textarea override ── */
textarea {
    background-color: #111118 !important;
    border: 1px solid #2A2A3E !important;
    border-radius: 10px !important;
    color: #E8E6F0 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.93rem !important;
    line-height: 1.6 !important;
    padding: 1rem !important;
    transition: border-color 0.2s ease !important;
    resize: vertical !important;
}
textarea:focus {
    border-color: #7C6AF7 !important;
    box-shadow: 0 0 0 3px rgba(124, 106, 247, 0.12) !important;
    outline: none !important;
}

/* ── Button ── */
[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #7C6AF7, #5A4FD0) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
    transition: opacity 0.2s ease, transform 0.15s ease !important;
    margin-top: 0.75rem !important;
}
[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Results card ── */
.results-wrapper {
    margin-top: 2.5rem;
    border-top: 1px solid #1E1E2E;
    padding-top: 2rem;
}
.results-heading {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #7C6AF7;
    margin-bottom: 1.2rem;
}
.result-section {
    background: #111118;
    border: 1px solid #1E1E2E;
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    margin-bottom: 0.85rem;
    transition: border-color 0.2s;
}
.result-section:hover { border-color: #2E2A4E; }
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #7C6AF7;
    margin-bottom: 0.45rem;
}
.section-content {
    font-size: 0.93rem;
    line-height: 1.65;
    color: #C8C5D8;
    white-space: pre-wrap;
}
.section-content.summary {
    color: #E8E6F0;
    font-weight: 500;
    font-size: 0.96rem;
}
.not-mentioned {
    color: #3E3C52;
    font-style: italic;
    font-size: 0.88rem;
}

/* ── Spinner override ── */
[data-testid="stSpinner"] {
    color: #7C6AF7 !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid #1A1A28;
    font-size: 0.78rem;
    color: #3A3850;
    font-family: 'Space Mono', monospace;
}
</style>
""", unsafe_allow_html=True)

# ── Model + Prompt (cached) ───────────────────────────────────────────────────
@st.cache_resource
def get_model():
    return init_chat_model(
        "openai/gpt-oss-120b:free",
        model_provider="openai",
        max_tokens=500,
    )

@st.cache_resource
def get_prompt():
    return ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are an information extraction system.

Analyze the provided text and return concise results:

Main Topic: max 1 sentence
Key Entities: max 5 items
Important Facts: max 5 items
Numbers/Dates: max 3 items
Action Items: max 3 items
Risks: max 3 items
Summary: max 75 words

Rules:
- Keep only high-value information.
- Eliminate redundancy.
- Preserve factual accuracy.
- Use bullet points where appropriate.
- If a section is missing, write "Not mentioned".
- Do not invent information.
- Base all outputs strictly on the provided text.
"""
        ),
        (
            "human",
            "Extract information from the following text:\n\n{text}"
        ),
    ])

# ── Helpers ───────────────────────────────────────────────────────────────────
SECTION_KEYS = [
    ("Main Topic", "main-topic"),
    ("Key Entities", "key-entities"),
    ("Important Facts", "important-facts"),
    ("Numbers/Dates Mentioned", "numbers-dates"),
    ("Action Items", "action-items"),
    ("Risks/Issues", "risks-issues"),
    ("Final Summary", "final-summary"),
]

def parse_sections(raw: str) -> dict:
    """Split the model output into its 7 labelled sections."""
    import re
    sections = {}
    headers = [k for k, _ in SECTION_KEYS]
    pattern = r"(?:^|\n)\s*(?:\d+\.\s*)?(" + "|".join(re.escape(h) for h in headers) + r")\s*[:\-]?\s*"
    parts = re.split(pattern, raw, flags=re.IGNORECASE)

    current = None
    for part in parts:
        matched = next((h for h in headers if h.lower() == part.strip().lower()), None)
        if matched:
            current = matched
        elif current:
            sections[current] = part.strip()
            current = None

    # Fallback: if parsing fails, dump everything under summary
    if not sections:
        sections["Final Summary"] = raw.strip()
    return sections

def render_results(raw: str):
    sections = parse_sections(raw)
    st.markdown('<div class="results-wrapper">', unsafe_allow_html=True)
    st.markdown('<p class="results-heading">Extraction Results</p>', unsafe_allow_html=True)

    for label, _ in SECTION_KEYS:
        content = sections.get(label, "Not mentioned").strip()
        is_summary = label == "Final Summary"
        not_mentioned = content.lower() in ("not mentioned", "", "n/a", "none")

        content_class = "section-content summary" if is_summary else "section-content"
        if not_mentioned:
            content_class += " not-mentioned"

        st.markdown(f"""
        <div class="result-section">
            <div class="section-label">{label}</div>
            <div class="{content_class}">{content}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">AI · Information Extraction</div>
    <h1 class="hero-title">ExtractIQ</h1>
    <p class="hero-sub">Drop any text. Get structured intelligence back in seconds.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="input-label">Your Text</p>', unsafe_allow_html=True)

user_text = st.text_area(
    label="",
    placeholder="Paste an article, meeting notes, report, email — anything you want analysed…",
    height=220,
    label_visibility="collapsed",
)

run = st.button("Extract Information →")

if run:
    if not user_text.strip():
        st.warning("Paste some text first — the box above is waiting.")
    else:
        model = get_model()
        prompt = get_prompt()
        with st.spinner("Extracting…"):
            chain_input = prompt.invoke({"text": user_text})
            response = model.invoke(chain_input)
        render_results(response.content)

st.markdown('<div class="footer">ExtractIQ · powered by Gemma</div>', unsafe_allow_html=True)