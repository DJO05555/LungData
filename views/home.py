from base64 import b64encode
from pathlib import Path

import streamlit as st

from utils import GITHUB_URL, LUNG_SVG, STATS, TEAM, footer, gap, html, stat


def asset_uri(name):
    image = Path(__file__).parent.parent / "assets" / name
    return f"data:image/png;base64,{b64encode(image.read_bytes()).decode()}"


def icon(paths):
    return f'<svg class="line-icon" viewBox="0 0 24 24" aria-hidden="true">{paths}</svg>'


ICONS = {
    "dataset": icon('<ellipse cx="12" cy="5" rx="7" ry="3"/><path d="M5 5v7c0 1.7 3.1 3 7 3s7-1.3 7-3V5"/><path d="M5 12v7c0 1.7 3.1 3 7 3s7-1.3 7-3v-7"/>'),
    "warning": icon('<path d="M12 4 3.8 19h16.4L12 4Z"/><path d="M12 9v4"/><path d="M12 16.5h.01"/>'),
    "check": icon('<path d="m5 12 4.2 4.2L19 6.5"/>'),
    "message": icon('<path d="M20 11.5a7.5 7.5 0 0 1-8 7.5 8.7 8.7 0 0 1-3.8-.9L4 19l1.1-3.3A7 7 0 0 1 4 12a7.5 7.5 0 0 1 8-7.5 7.5 7.5 0 0 1 8 7Z"/>'),
    "shield": icon('<path d="M12 3.5 19 6v5.6c0 4.3-2.9 7.3-7 8.9-4.1-1.6-7-4.6-7-8.9V6l7-2.5Z"/><path d="m9 12 2 2 4-4"/>'),
    "code": icon('<path d="m9 7-5 5 5 5M15 7l5 5-5 5M14 4l-4 16"/>'),
    "scale": icon('<ellipse cx="12" cy="5" rx="7" ry="3"/><path d="M5 5v7c0 1.7 3.1 3 7 3s7-1.3 7-3V5"/><path d="M5 12v7c0 1.7 3.1 3 7 3s7-1.3 7-3v-7"/>'),
}

PYTHON = asset_uri("python.png")
PARQUET = asset_uri("parquet.png")
POWER_BI = asset_uri("power-bi.png")


# ---------- Hero ----------
gap(3)
left, right = st.columns([7, 5], vertical_alignment="center", gap="large")
with left:
    html('<div class="eyebrow">Big Data Project · Group 5</div>')
    html('<div class="h1">From <span class="hl">messy data</span> to clear answers</div>')
    html('<div class="lead">We generated <span class="hl">10 million</span> synthetic lung-cancer patient records, '
         'made them <span class="hl">messy on purpose</span>, cleaned them, and built dashboards and an AI assistant on top.</div>')
    gap(1)
    b1, b2, _ = st.columns([1.5, 1, 1.5])
    with b1.container(key="cta_primary"):
        st.page_link("views/clean.py", label="Explore the dashboards →")
    with b2.container(key="cta_ghost"):
        st.page_link("views/bot.py", label="Ask the AI")
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


def explore(col, key, icon_markup, title, text, link):
    with col:
        with st.container(key=f"card_{key}"):
            html(f'<div class="ico24">{icon_markup}</div><div class="h3">{title}</div><p class="muted">{text}</p>')
            link()


with st.container(key="explore_grid"):
    row1 = st.columns(2, gap="medium")
    explore(row1[0], "synth", ICONS["dataset"], "Realistic Synthetic Dataset",
            "10 million records generated from published reference distributions. See the sources and the code.",
            lambda: html(f'<a class="lnk" href="{GITHUB_URL}" target="_blank">View GitHub repo →</a>'))
    explore(row1[1], "messy", ICONS["warning"], "Messy Dataset",
            "See the raw data and everything wrong with it.",
            lambda: st.page_link("views/messy.py", label="View messy dashboard →"))
    gap(1.5)
    row2 = st.columns(2, gap="medium")
    explore(row2[0], "clean", ICONS["check"], "Cleaned Dataset",
            "See what the data looks like after cleaning.",
            lambda: st.page_link("views/clean.py", label="View cleaned dashboard →"))
    explore(row2[1], "ai", ICONS["message"], "AI Assistant",
            "Ask questions about the data in plain language.",
            lambda: st.page_link("views/bot.py", label="Chat with the AI →"))

# ---------- About ----------
gap(4)
html('<div class="h2">About the dataset</div>')
gap(1)
html('<div class="card about"><div class="facts">'
     f'<div class="row">{ICONS["shield"]}<span><b>Synthetic:</b> no real patients, not medical advice</span></div>'
     f'<div class="row">{ICONS["code"]}<span><b>Purpose:</b> practice big-data cleaning and analysis</span></div>'
     f'<div class="row">{ICONS["scale"]}<span><b>Scale:</b> <span class="hl">10 million</span> rows across 14 columns</span></div>'
     '</div><div class="tech-tiles">'
     f'<div class="tech-tile"><img src="{PYTHON}" alt="Python logo"><span>Python</span></div>'
     f'<div class="tech-tile"><img src="{PARQUET}" alt="Parquet logo"><span>Parquet</span></div>'
     f'<div class="tech-tile"><img src="{POWER_BI}" alt="Power BI logo"><span>Power BI</span></div>'
     '</div></div>')

# ---------- Team ----------
gap(4)
html('<div class="h2">The team</div>')
gap(1)
for col, (initials, name, role) in zip(st.columns(len(TEAM)), TEAM):
    with col:
        html(f'<div class="card member"><div class="av">{initials}</div><b>{name}</b><span>{role}</span></div>')

footer()
