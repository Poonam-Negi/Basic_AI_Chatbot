from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
import streamlit as st

load_dotenv()

st.set_page_config(page_title="AI Chat ✦", page_icon="✦", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&family=DM+Serif+Display:ital@0;1&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #FAF7F4 !important;
    font-family: 'DM Sans', sans-serif !important;
    color: #2E2822 !important;
}
[data-testid="stMainBlockContainer"] {
    max-width: 700px !important;
    padding: 2rem 1.5rem 2rem !important;
}
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] {
    display: none !important;
    visibility: hidden !important;
}

/* kill the fade/blur overlay during reruns */
[data-testid="stAppViewContainer"]::before,
.stApp > iframe,
div[data-stale="true"],
[data-testid="stSpinner"],
.element-container iframe { opacity: 1 !important; }

div[data-stale="true"] * { opacity: 1 !important; filter: none !important; }

.stApp [data-stale="true"] {
    opacity: 1 !important;
    pointer-events: none;
}
.masthead {
    text-align: center;
    padding: 1.6rem 0 1.2rem;
    border-bottom: 1px solid #E4DBCF;
    margin-bottom: 1.4rem;
}
.masthead h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    font-weight: 400;
    color: #2E2822;
    margin: 0 0 .3rem;
}
.masthead p {
    font-size: .78rem;
    color: #B8A99A;
    letter-spacing: .07em;
    text-transform: uppercase;
    margin: 0;
}
.chat-wrap { display: flex; flex-direction: column; gap: .9rem; margin-bottom: 1.2rem; }
.msg { display: flex; gap: .6rem; align-items: flex-start; }
.msg.user { flex-direction: row-reverse; }
.avatar {
    width: 30px; height: 30px;
    border-radius: 50%;
    background: #EDD9CF;
    display: flex; align-items: center; justify-content: center;
    font-size: .85rem; flex-shrink: 0;
}
.msg.user .avatar { background: #EFE8E1; }
.bubble {
    max-width: 75%;
    padding: .7rem .95rem;
    border-radius: 16px;
    font-size: .89rem;
    line-height: 1.55;
}
.msg.bot .bubble {
    background: #FFFFFF;
    border: 1px solid #E4DBCF;
    border-top-left-radius: 4px;
}
.msg.user .bubble {
    background: #EFE8E1;
    border-top-right-radius: 4px;
}
.empty-state {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
    color: #B8A99A;
}
.empty-state .orb { font-size: 2.2rem; margin-bottom: .6rem; opacity: .65; }
.empty-state p { font-size: .85rem; margin: 0; }
[data-testid="stTextInput"] input {
    background: #FFFFFF !important;
    border: 1.5px solid #E4DBCF !important;
    border-radius: 999px !important;
    padding: .6rem 1.2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .88rem !important;
    color: #2E2822 !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #C4856A !important;
    box-shadow: 0 0 0 3px #EDD9CF !important;
}
[data-testid="stFormSubmitButton"] > button {
    background: #C4856A !important;
    color: #fff !important;
    border: none !important;
    border-radius: 999px !important;
    padding: .55rem 1.4rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .88rem !important;
    font-weight: 500 !important;
    width: 100% !important;
}
[data-testid="stFormSubmitButton"] > button:hover { background: #b5735a !important; }
[data-testid="stButton"] > button {
    border-radius: 999px !important;
    border: 1.5px solid #E4DBCF !important;
    background: #F3EEE8 !important;
    color: #B8A99A !important;
    font-size: .8rem !important;
    padding: .38rem .5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all .15s !important;
}
[data-testid="stButton"] > button:hover {
    border-color: #C4856A !important;
    color: #C4856A !important;
}
/* hide "Press Enter to submit form" */
div[data-testid="stForm"] small,
div[data-testid="InputInstructions"],
[data-testid="stTextInput"] ~ small,
.st-emotion-cache-1gulkj5,
p.st-emotion-cache-1gulkj5 { display: none !important; visibility: hidden !important; }

/* remove red focus border — keep our custom terracotta glow only */
[data-testid="stTextInput"] input:focus,
[data-testid="stTextInput"] input:active,
[data-testid="stTextInput"] input:focus-visible {
    border-color: #C4856A !important;
    box-shadow: 0 0 0 3px #EDD9CF !important;
    outline: none !important;
}
[data-testid="stTextInput"] > div:focus-within {
    border-color: transparent !important;
    box-shadow: none !important;
    outline: none !important;
}
.divider { border: none; border-top: 1px solid #E4DBCF; margin: 1.2rem 0; }
.typing-bubble { display: flex; gap: .6rem; align-items: flex-start; margin: .4rem 0 .8rem; }
.typing-bubble .avatar {
    width: 30px; height: 30px; border-radius: 50%;
    background: #EDD9CF;
    display: flex; align-items: center; justify-content: center;
    font-size: .85rem; flex-shrink: 0;
}
.typing-bubble .bubble {
    background: #FFFFFF;
    border: 1px solid #E4DBCF;
    border-radius: 16px; border-top-left-radius: 4px;
    padding: .75rem 1rem;
    display: flex; gap: 5px; align-items: center;
}
.dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #C4856A; opacity: 0.4;
    animation: blink 1.2s infinite ease-in-out;
}
.dot:nth-child(2) { animation-delay: .2s; }
.dot:nth-child(3) { animation-delay: .4s; }
@keyframes blink {
    0%,80%,100% { opacity: .4; transform: scale(1); }
    40%          { opacity: 1;  transform: scale(1.3); }
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "messages"  not in st.session_state: st.session_state.messages  = []
if "mode"      not in st.session_state: st.session_state.mode      = "Helpful"
if "thinking"  not in st.session_state: st.session_state.thinking  = False
if "pending"   not in st.session_state: st.session_state.pending   = None

MODES = {
    "Funny":   ("You are a funny AI assistant.", "😄"),
    "Angry":   ("You are an angry AI assistant who responds rudely.", "😡"),
    "Sad":     ("You are a sad AI assistant who sounds melancholic.", "😢"),
    "Helpful": ("You are a helpful AI assistant.", "🤖"),
}

@st.cache_resource
def get_model():
    return init_chat_model("google/gemma-4-26b-a4b-it", model_provider="openai", max_tokens=50)

model = get_model()

# ── If we're in "thinking" state, call the API NOW before rendering ────────────
if st.session_state.thinking and st.session_state.pending:
    sys_prompt, _ = MODES[st.session_state.mode]
    lc_msgs = [SystemMessage(content=sys_prompt)]
    for m in st.session_state.messages:
        if m["role"] == "user":
            lc_msgs.append(HumanMessage(content=m["content"]))
        else:
            lc_msgs.append(AIMessage(content=m["content"]))
    try:
        response = model.invoke(lc_msgs)
        st.session_state.messages.append({"role": "assistant", "content": response.content})
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"⚠️ Error: {e}"})
    st.session_state.thinking = False
    st.session_state.pending  = None
    st.rerun()

# ── Masthead ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
  <h1>✦ AI Chat</h1>
  <p>choose your vibe &amp; start talking</p>
</div>
""", unsafe_allow_html=True)

# ── Mode buttons ───────────────────────────────────────────────────────────────
cols = st.columns(4)
for i, col in enumerate(cols):
    with col:
        m = list(MODES.keys())[i]
        _, emoji = MODES[m]
        if st.button(f"{emoji} {m}", key=f"mode_{m}", use_container_width=True):
            if st.session_state.mode != m:
                st.session_state.mode     = m
                st.session_state.messages = []
                st.session_state.thinking = False
                st.session_state.pending  = None
                st.rerun()

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Chat history ───────────────────────────────────────────────────────────────
_, bot_emoji = MODES[st.session_state.mode]

if not st.session_state.messages and not st.session_state.thinking:
    st.markdown(f"""
    <div class="empty-state">
      <div class="orb">{bot_emoji}</div>
      <p>Say something to get started…</p>
    </div>
    """, unsafe_allow_html=True)
else:
    html = '<div class="chat-wrap">'
    for m in st.session_state.messages:
        if m["role"] == "user":
            html += f'<div class="msg user"><div class="avatar">🙂</div><div class="bubble">{m["content"]}</div></div>'
        else:
            html += f'<div class="msg bot"><div class="avatar">{bot_emoji}</div><div class="bubble">{m["content"]}</div></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

# ── Typing indicator (shown between chat and input bar) ───────────────────────
if st.session_state.thinking:
    st.markdown(f"""
    <div class="typing-bubble">
      <div class="avatar">{bot_emoji}</div>
      <div class="bubble">
        <div class="dot"></div><div class="dot"></div><div class="dot"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Input form ────────────────────────────────────────────────────────────────
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("msg", placeholder="Type a message…", label_visibility="collapsed")
    with col2:
        submitted = st.form_submit_button("Send")

if submitted and user_input.strip() and not st.session_state.thinking:
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    st.session_state.thinking = True
    st.session_state.pending  = user_input.strip()
    st.rerun()   # ← rerun #1: shows user message + typing bubble immediately
                 #   rerun #2 happens after API call completes at the top