import streamlit as st

from knowledge import GREETING, SUGGESTIONS, SYSTEM_PROMPT, local_reply
from utils import footer, gap, html

MODEL = "claude-haiku-4-5-20251001"   # only used if you add an API key


def llm_available():
    try:
        return bool(st.secrets["ANTHROPIC_API_KEY"])
    except Exception:
        return False


def ask_llm(history):
    import anthropic

    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    msgs = [{"role": m["role"], "content": m["content"]} for m in history]
    while msgs and msgs[0]["role"] != "user":
        msgs.pop(0)
    resp = client.messages.create(model=MODEL, max_tokens=500, system=SYSTEM_PROMPT, messages=msgs)
    return resp.content[0].text


def get_answer(question, history):
    if llm_available():
        try:
            return ask_llm(history)
        except Exception:
            pass
    return local_reply(question)


gap(3)
left, right = st.columns([2, 1], gap="large")

with left:
    with st.container(key="panel_chat"):
        html('<div class="panel-head"><div class="ico">🤖</div>'
             '<div><div class="t">LungData Assistant</div><div class="s">● Online</div></div>'
             '</div>')

        st.session_state.setdefault("chat", [{"role": "assistant", "content": GREETING}])
        history = st.container()

        html('<div class="muted small" style="margin-top:1rem;font-weight:600;letter-spacing:.06em;'
             'text-transform:uppercase">Suggested queries</div>')
        chip = None
        with st.container(key="chips"):
            cols = st.columns(2)
            for i, q in enumerate(SUGGESTIONS):
                if cols[i % 2].button(q, key=f"chip{i}"):
                    chip = q

        prompt = st.chat_input("Ask a question about the dataset…") or chip
        html('<div class="disclaimer">AI can make mistakes. Synthetic data, not medical advice.</div>')

        if prompt:
            st.session_state.chat.append({"role": "user", "content": prompt})
            with st.spinner("Thinking..."):
                answer = get_answer(prompt, st.session_state.chat)
            st.session_state.chat.append({"role": "assistant", "content": answer})

        with history:
            for m in st.session_state.chat:
                with st.chat_message(m["role"], avatar="🤖" if m["role"] == "assistant" else None):
                    st.markdown(m["content"])

with right:
    with st.container(key="panel_ask"):
        html('<div class="h3" style="margin-top:0">What you can ask</div>'
             '<div class="ask"><div class="ico">🗄️</div><div><b>The dataset</b>'
             '<span>(columns, size, how it was generated)</span></div></div>'
             '<div class="ask"><div class="ico">🪄</div><div><b>The cleaning</b>'
             '<span>(what was wrong and how we fixed it)</span></div></div>'
             '<div class="ask"><div class="ico">📈</div><div><b>The findings</b>'
             '<span>(risk factors and patterns)</span></div></div>')
    with st.container(key="panel_know"):
        html('<div class="h3" style="margin-top:0">Good to know</div>'
             '<div class="good">Built on our project&#39;s data documentation</div>'
             '<div class="good">Synthetic data, no real patients</div>'
             '<div class="good">Not medical advice</div>')

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
