import streamlit as st

from utils import GITHUB_URL, LUNG_SVG, STATS, TEAM, footer, gap, html, stat

# ---------- Hero ----------
gap(3)
left, right = st.columns([7, 5], vertical_alignment="center", gap="large")
with left:
    html('<div class="eyebrow">Big Data Project · Group 5</div>')
    html('<div class="h1">From <span class="hl">messy data</span> to clear answers</div>')
    html('<div class="lead">We generated <span class="hl">5 million</span> synthetic lung-cancer patient records, '
         'made them <span class="hl">messy on purpose</span>, cleaned them, and built dashboards and an AI assistant on top.</div>')
    gap(1)
    b1, b2, _ = st.columns([1.5, 1, 1.5])
    with b1.container(key="cta_primary"):
        st.page_link("views/clean.py", label="Explore the dashboards →")
    with b2.container(key="cta_ghost"):
        st.page_link("views/bot.py", label="Ask the AI", icon="💬")
with right:
    html(f'<div class="heroart">{LUNG_SVG}</div>')

# ---------- Stats strip ----------
gap(3)
items = [
    (STATS["records"], "Patient records"),
    (STATS["columns"], "Columns"),
    (STATS["raw_missing_rows"], "Rows with missing values (raw data)"),
    (STATS["positive_rate"], "Positive diagnosis rate"),
]
for col, (value, caption) in zip(st.columns(4), items):
    with col:
        stat(value, caption)

# ---------- Explore ----------
gap(4)
html('<div class="h2">Explore the project</div>')
gap(1)


def explore(col, key, icon, title, text, link):
    with col:
        with st.container(key=f"card_{key}"):
            html(f'<div class="ico24">{icon}</div><div class="h3">{title}</div><p class="muted">{text}</p>')
            gap(0.5)
            link()


row1, row2 = st.columns(2), st.columns(2)
explore(row1[0], "synth", "🗄️", "Realistic Synthetic Dataset",
        "5 million records generated from published reference distributions. See the sources and the code.",
        lambda: html(f'<a class="lnk" href="{GITHUB_URL}" target="_blank">View GitHub repo →</a>'))
explore(row1[1], "messy", "⚠️", "Messy Dataset",
        "See the raw data and everything wrong with it.",
        lambda: st.page_link("views/messy.py", label="View messy dashboard →"))
explore(row2[0], "clean", "✅", "Cleaned Dataset",
        "See what the data looks like after cleaning.",
        lambda: st.page_link("views/clean.py", label="View cleaned dashboard →"))
explore(row2[1], "ai", "🤖", "AI Assistant",
        "Ask questions about the data in plain language.",
        lambda: st.page_link("views/bot.py", label="Chat with the AI →"))

# ---------- About ----------
gap(4)
html('<div class="h2">About the dataset</div>')
gap(1)
html('<div class="card about"><div>'
     '<div class="row">🛡️ <b>Synthetic:</b> no real patients, not medical advice</div>'
     '<div class="row">💻 <b>Purpose:</b> practice big-data cleaning and analysis</div>'
     '<div class="row">🗄️ <b>Scale:</b> <span class="hl">5 million</span> rows across 14 columns</div>'
     '</div><div class="chips"><span>Python</span><span>Parquet</span><span>Power BI</span></div></div>')

# ---------- Team ----------
gap(4)
html('<div class="h2">The team</div>')
gap(1)
for col, (initials, name, role) in zip(st.columns(len(TEAM)), TEAM):
    with col:
        html(f'<div class="card member"><div class="av">{initials}</div><b>{name}</b><span>{role}</span></div>')

footer()