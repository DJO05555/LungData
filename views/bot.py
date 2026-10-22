import os
from html import escape
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from openai import APIConnectionError, APIError, OpenAI, RateLimitError
from dotenv import load_dotenv

from knowledge import SUGGESTIONS
from utils import ICONS, footer, gap, html, icon

CONTEXT_FILE = Path(__file__).parent.parent / "assets" / "lung_cancer_dashboard_interpretation.md"
load_dotenv(CONTEXT_FILE.parent.parent / ".env")
DEFAULT_MODEL = "openai/gpt-oss-120b"
SYSTEM_INSTRUCTIONS = (
    "You are the LungData Assistant for a student big-data project about a synthetic lung-cancer patient dataset. "
    "Answer ONLY using the context below. If the answer is not in the context, say you don't know and suggest what to check. "
    "Quote numbers exactly as written in the context and never invent statistics. Keep answers short (under 120 words) and plain. "
    "The data is synthetic; you are not a medical professional and must not give medical advice. "
    "If asked something unrelated to the project, politely redirect to the dataset, cleaning, or findings."
)


@st.cache_data(show_spinner=False)
def load_context():
    return CONTEXT_FILE.read_text(encoding="utf-8")


SYSTEM_PROMPT = f"{SYSTEM_INSTRUCTIONS}\n\nCONTEXT:\n{load_context()}"


def setting(name, default=""):
    value = os.getenv(name)
    if value:
        return value
    try:
        return st.secrets.get(name, default)
    except (FileNotFoundError, KeyError):
        return default


def ask_llm(history):
    base_url = setting("LLM_BASE_URL")
    api_key = setting("LLM_API_KEY")
    model = setting("LLM_MODEL", DEFAULT_MODEL)
    if not base_url or not api_key:
        return "The chat service is not configured yet. Add LLM_BASE_URL and LLM_API_KEY to your environment or Streamlit secrets."

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend({"role": item["role"], "content": item["content"]} for item in history[-10:])
    try:
        response = OpenAI(base_url=base_url, api_key=api_key).chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=400,
            extra_body={"reasoning_effort": "low"},
        )
        answer = response.choices[0].message.content
        return answer or "I couldn't generate an answer. Please try asking again."
    except RateLimitError:
        return "The chat service is busy right now. Please wait a moment and try again."
    except APIConnectionError:
        return "I couldn't reach the chat service. Please check the connection and try again."
    except APIError:
        return "The chat service couldn't answer right now. Please try again shortly."


AI_AVATAR = '''<svg viewBox="0 0 36 36" aria-hidden="true"><defs><linearGradient id="a" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#2dd4bf"/><stop offset="1" stop-color="#0f766e"/></linearGradient></defs><circle cx="18" cy="18" r="17" fill="url(#a)"/><g fill="none" stroke="white" stroke-opacity=".92" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8v8l-3 2.5M18 16l3 2.5"/><path d="M15 14c-4 .3-6.3 4.6-5.8 8.4.4 2.9 3.2 3.7 5.1 2.2 1.8-1.4 1.2-5.5.7-8.6Z"/><path d="M21 14c4 .3 6.3 4.6 5.8 8.4-.4 2.9-3.2 3.7-5.1 2.2-1.8-1.4-1.2-5.5-.7-8.6Z"/></g></svg>'''
USER_AVATAR = '''<svg viewBox="0 0 36 36" aria-hidden="true"><circle cx="18" cy="18" r="17" fill="#39434b"/><g fill="none" stroke="white" stroke-opacity=".8" stroke-width="1.5" stroke-linecap="round"><circle cx="18" cy="14" r="4"/><path d="M10.5 27c.8-4 3.7-6.5 7.5-6.5s6.7 2.5 7.5 6.5"/></g></svg>'''


def message_html(role, content):
    avatar = AI_AVATAR if role == "assistant" else USER_AVATAR
    safe_content = escape(content).replace("\n", "<br>")
    return (f'<div class="chat-row {role}"><div class="chat-avatar">{avatar}</div>'
            f'<div class="chat-bubble">{safe_content}</div></div>')


gap(1.5)
with st.container(key="bot_info_grid"):
    ask_col, know_col = st.columns(2, gap="medium")
    with ask_col:
        with st.container(key="panel_ask"):
            html('<div class="h3" style="margin-top:0">What you can ask</div>'
                 f'<div class="ask"><div class="ico">{icon(ICONS["database"], color="#14B8A6")}</div><div><b>The dataset</b>'
                 '<span>(columns, size, how it was generated)</span></div></div>'
                 f'<div class="ask"><div class="ico">{icon(ICONS["check"], color="#14B8A6")}</div><div><b>The cleaning</b>'
                 '<span>(what was wrong and how we fixed it)</span></div></div>'
                 f'<div class="ask"><div class="ico">{icon(ICONS["chart"], color="#14B8A6")}</div><div><b>The findings</b>'
                 '<span>(risk factors and patterns)</span></div></div>')
    with know_col:
        with st.container(key="panel_know"):
            html('<div class="h3" style="margin-top:0">Good to know</div>'
                 '<div class="good">Built on our project&#39;s data documentation</div>'
                 '<div class="good">Synthetic data, no real patients</div>'
                 '<div class="good">Not medical advice</div>')

gap(1.5)
with st.container(key="panel_chat"):
    title_col, new_col = st.columns([5, 1], vertical_alignment="center")
    with title_col:
        html('<div class="panel-head"><div><div class="t">LungData Assistant</div><div class="s">Online</div></div></div>')
    with new_col:
        if st.button("New chat", key="new_chat"):
            st.session_state.chat = []
            st.rerun()

    st.session_state.setdefault("chat", [])
    chip = None
    if not st.session_state.chat:
        html('<div class="muted small" style="margin-top:.25rem;font-weight:600;letter-spacing:.06em;'
             'text-transform:uppercase">Suggested queries</div>')
        with st.container(key="chips"):
            cols = st.columns(2)
            for i, question in enumerate(SUGGESTIONS):
                if cols[i % 2].button(question, key=f"chip{i}"):
                    chip = question

    prompt = chip or st.chat_input("Ask a question about the dataset…")
    html('<div class="disclaimer">AI can make mistakes. Synthetic data, not medical advice.</div>')

    if prompt:
        if len(st.session_state.chat) > 18:
            st.info("This chat has reached its 20-message limit. Start a new session to ask more questions.")
        else:
            st.session_state.chat.append({"role": "user", "content": prompt})
            with st.spinner("LungData Assistant is typing..."):
                answer = ask_llm(st.session_state.chat)
            st.session_state.chat.append({"role": "assistant", "content": answer})
            st.rerun()

    with st.container(key="chat_messages", height=540, border=False):
        for message in st.session_state.chat:
            html(message_html(message["role"], message["content"]))
        html('<div id="chat-bottom"></div>')
    components.html('''<script>
        const messages = window.parent.document.querySelector('[class*="st-key-chat_messages"]');
        if (messages) messages.scrollTo({top: messages.scrollHeight, behavior: 'smooth'});
    </script>''', height=0)

gap(2)
with st.container(key="panel_cta"):
    text_col, messy_col, clean_col = st.columns([3, 1, 1], vertical_alignment="center")
    with text_col:
        html('<div class="h3" style="margin-top:0">Want to see the data yourself?</div>'
             '<div class="muted">Explore both the corrupted source and our verified pipeline outputs.</div>')
    with messy_col.container(key="cta_ghost"):
        st.page_link("views/messy.py", label="Messy dataset")
    with clean_col.container(key="cta_primary"):
        st.page_link("views/clean.py", label="Cleaned dataset")

footer()
