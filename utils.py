from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

APP_NAME = "LungData"
GROUP = "DS301"
TEAL, RED = "#14B8A6", "#EF4444"

GITHUB_URL = "https://github.com/"             # TODO: paste your team's repo link
RAW_FILE = "lung_study_raw_v0.csv"             # TODO: raw file name shown under the messy dashboard
CLEAN_FILE = "cleaned_lung_cancer_dataset.csv" # TODO: cleaned file name

# Paste the Power BI "Publish to web" link (the src="..." inside the iframe code). "" = placeholder.
POWERBI = {"messy": "", "clean": ""}

STATS = {
    "records": "5,004,574",
    "columns": "14",
    "raw_missing_rows": "40.8%",
    "sparsity": "5.3–5.9%",
    "positive_rate": "21.6%",
    "clean_records": "TBD",      # TODO: rows after cleaning
    "clean_columns": "TBD",      # TODO: columns after cleaning
    "clean_missing": "TBD",      # TODO: blank cells left after cleaning
}

# TODO: replace with your real group members (these are the design's placeholders)
TEAM = [
    ("RA", "Ralph Zedrick Abayon", "Lead Architect"),
    ("LE", "Lance Evangelista", "Data Pipeline"),
    ("HO", "Hansel Nino Ofilan", "ML Modeling"),
    ("DO", "Dardy Jr. Onia", "Frontend & AI"),
    ("MS", "Marc Deanielle Santiago", "EDA & Quality"),
]

PAGES = [
    ("views/home.py", "Home", "🏠"),
    ("views/messy.py", "Messy Data", "🧹"),
    ("views/clean.py", "Cleaned Data", "✅"),
    ("views/bot.py", "AI Bot", "🤖"),
]

PERSON_SVG = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="#003731">'
              '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8z"/></svg>')

LUNG_SVG = """
<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:340px">
<g fill="none" stroke="rgba(255,255,255,.45)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M200 60 V165"/><path d="M200 165 L165 190"/><path d="M200 165 L235 190"/>
<path d="M170 170 C120 175 85 245 92 305 C97 345 140 360 168 338 C190 320 186 250 182 200 Z"/>
<path d="M230 170 C280 175 315 245 308 305 C303 345 260 360 232 338 C210 320 214 250 218 200 Z"/>
</g>
<g fill="none" stroke="rgba(20,184,166,.6)" stroke-width="1.5">
<path d="M150 205 L125 255 L140 300"/><path d="M150 205 L165 265"/>
<path d="M250 205 L275 255 L260 300"/><path d="M250 205 L235 265"/>
</g>
<g fill="#14B8A6">
<circle cx="150" cy="205" r="4"/><circle cx="125" cy="255" r="4"/><circle cx="140" cy="300" r="4"/><circle cx="165" cy="265" r="4"/>
<circle cx="250" cy="205" r="4"/><circle cx="275" cy="255" r="4"/><circle cx="260" cy="300" r="4"/><circle cx="235" cy="265" r="4"/>
</g>
</svg>
"""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root {--gut: max(1.5rem, calc((100vw - 1200px) / 2)); --line: rgba(255,255,255,.12);
       --card: rgba(255,255,255,.06); --muted: rgba(255,255,255,.65);}
html, body, .stApp, p, h1, h2, h3, h4, a, button, input, textarea, label {font-family: 'Inter', sans-serif;}
.stApp {overflow-x: hidden;}
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer {display: none !important;}
.block-container, [data-testid="stMainBlockContainer"] {max-width: none !important; padding: 0 var(--gut) 0 var(--gut) !important;}
.right {display: flex; justify-content: flex-end; align-items: center; gap: .4rem;}
.muted {color: var(--muted);}
.small {font-size: .8rem;}
.dot {display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #14B8A6;}

/* ---------- top bar (full width) ---------- */
.st-key-topbar {position: sticky; top: 0; z-index: 999; background: #1E2428; border-bottom: 1px solid var(--line);
                margin-top: 0 !important; margin-left: calc(-1 * var(--gut)); margin-right: 0;
                width: calc(100% + 2 * var(--gut)) !important; max-width: none !important;
                box-sizing: border-box; padding: 0 var(--gut);}
.brand {display: flex; align-items: center; gap: .5rem; font-weight: 700; font-size: 1.25rem; color: #fff; white-space: nowrap;}
.pill {padding: .15rem .6rem; border-radius: 999px; border: 1px solid #3C4947; background: #252B2F;
       color: #BBCAC6; font-size: .7rem; font-weight: 600; white-space: nowrap;}
.avatar {width: 32px; height: 32px; border-radius: 50%; background: #14B8A6; display: grid; place-items: center;}
.st-key-nav a {background: transparent !important; justify-content: center; border-radius: 0 !important;
               padding: 1.15rem .25rem !important; border-bottom: 2px solid transparent; gap: .4rem; white-space: nowrap;}
.st-key-nav a p {color: rgba(255,255,255,.65) !important; font-weight: 600; font-size: .9rem; margin: 0; white-space: nowrap;
                 overflow: visible !important; text-overflow: clip !important;}
.st-key-nav a:hover p {color: #fff !important;}
.st-key-nav [data-testid="stHorizontalBlock"] > div:nth-child(__N__) a {border-bottom-color: __ACCENT__ !important;}
.st-key-nav [data-testid="stHorizontalBlock"] > div:nth-child(__N__) a p {color: #fff !important;}

/* ---------- typography ---------- */
.eyebrow {font-size: .75rem; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: __ACCENT__;}
.eyebrow .sub {color: var(--muted); text-transform: none; letter-spacing: 0; font-weight: 500; margin-left: .6rem;}
.h1 {font-size: clamp(2.2rem, 5vw, 3.75rem); font-weight: 700; line-height: 1.1; letter-spacing: -.025em; color: #fff; margin: 1rem 0;}
.h1.mid {font-size: clamp(2rem, 4vw, 3rem);}
.h2 {font-size: 1.9rem; font-weight: 700; letter-spacing: -.02em; color: #fff; margin: 0 0 .4rem;}
.h3 {font-size: 1.25rem; font-weight: 700; color: #fff; margin: .9rem 0 .4rem;}
.lead {color: var(--muted); font-size: 1.125rem; line-height: 1.6; max-width: 38rem; margin: 0;}
.hl {color: __ACCENT__; font-weight: 700;}

/* ---------- cards ---------- */
.card {background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 1.5rem; height: 100%;}
.card h4 {margin: .8rem 0 .4rem; padding: 0; color: #fff; font-size: 1.05rem; font-weight: 700;}
.card p {margin: 0; color: var(--muted); font-size: .88rem; line-height: 1.5;}
.stat .v, .kpi .v {font-size: 2.25rem; font-weight: 700; color: __ACCENT__; letter-spacing: -.02em; line-height: 1.15;}
.stat .c, .kpi .c {color: var(--muted); font-size: .88rem; margin-top: .25rem;}
.kpi .top {display: flex; justify-content: space-between; align-items: center; margin-bottom: .8rem; color: var(--muted);
           font-size: .72rem; font-weight: 600; letter-spacing: .06em; text-transform: uppercase;}
.badge {padding: .15rem .65rem; border-radius: 999px; font-size: .72rem; font-weight: 700; white-space: nowrap;
        color: __ACCENT__; border: 1px solid __ACCENT__;}
.defect .top {display: flex; justify-content: space-between; align-items: center; font-size: 1.4rem;}
.mono {font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .75rem; color: __ACCENT__;
       border-top: 1px solid var(--line); margin-top: 1rem; padding-top: .8rem;}
.heroart {aspect-ratio: 1; max-width: 420px; margin-left: auto; background: var(--card); border: 1px solid var(--line);
          border-radius: 16px; display: grid; place-items: center; padding: 1.5rem;}
.about {display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1.5rem; padding: 2rem;}
.about .row {color: rgba(255,255,255,.9); margin: .55rem 0; font-size: 1rem;}
.chips {display: flex; flex-wrap: wrap; gap: .7rem;}
.chips span {white-space: nowrap; padding: .35rem .9rem; border-radius: 999px; border: 1px solid var(--line);
             background: rgba(255,255,255,.04); color: rgba(255,255,255,.8);
             font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .75rem;}
.member {text-align: center;}
.member .av {width: 48px; height: 48px; border-radius: 50%; border: 1px solid rgba(255,255,255,.2);
             background: rgba(255,255,255,.08); display: grid; place-items: center; margin: 0 auto .7rem;
             color: #fff; font-weight: 700; font-size: .85rem;}
.member b {display: block; color: #fff; font-size: .9rem;}
.member span {color: var(--muted); font-size: .75rem;}

/* explore cards (container with a colored top edge) */
[class*="st-key-card_"] {background: var(--card); border: 1px solid var(--line); border-top: 4px solid rgba(255,255,255,.3);
                         border-radius: 16px; padding: 1.6rem;}
.st-key-card_messy {border-top-color: #EF4444 !important;}
.st-key-card_clean {border-top-color: #14B8A6 !important;}
[class*="st-key-card_"] a {padding: 0 !important; background: transparent !important;}
[class*="st-key-card_"] a p {color: #14B8A6 !important; font-weight: 600; font-size: .88rem; margin: 0;}
.lnk {color: #14B8A6; font-weight: 600; font-size: .88rem; text-decoration: none;}
.ico24 {font-size: 1.5rem; line-height: 1;}

/* buttons */
.st-key-cta_primary a {background: #14B8A6 !important; border-radius: 8px !important; padding: .7rem 1.4rem !important; justify-content: center;}
.st-key-cta_primary a p {color: #1E2428 !important; font-weight: 600; margin: 0;}
.st-key-cta_ghost a {border: 1px solid rgba(255,255,255,.3); background: transparent !important; border-radius: 8px !important;
                     padding: .7rem 1.4rem !important; justify-content: center;}
.st-key-cta_ghost a p {color: #fff !important; font-weight: 500; margin: 0;}

/* panels (bot page, banners) */
[class*="st-key-panel_"] {background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 1.5rem;}
.panel-head {display: flex; align-items: center; gap: .8rem; padding-bottom: 1rem; border-bottom: 1px solid var(--line); margin-bottom: .5rem;}
.panel-head .ico {width: 44px; height: 44px; border-radius: 12px; border: 1px solid var(--line); display: grid;
                  place-items: center; font-size: 1.3rem; background: rgba(255,255,255,.05);}
.panel-head .t {font-weight: 700; color: #fff; font-size: 1.1rem; line-height: 1.2;}
.panel-head .s {color: #14B8A6; font-size: .75rem; font-weight: 600;}
.ask {display: flex; gap: .9rem; align-items: flex-start; margin: .9rem 0;}
.ask .ico {width: 40px; height: 40px; border-radius: 10px; border: 1px solid var(--line); display: grid; place-items: center; flex: none;}
.ask b {color: #fff; display: block;}
.ask span {color: var(--muted); font-size: .85rem;}
.good {color: rgba(255,255,255,.9); margin: .55rem 0; font-size: .95rem;}
.good::before {content: ""; display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #14B8A6; margin-right: .7rem; vertical-align: middle;}
.st-key-chips button {border-radius: 999px; border: 1px solid rgba(20,184,166,.45); background: transparent; color: #fff; font-size: .78rem; padding: .25rem .9rem;}
.st-key-chips button:hover {border-color: #14B8A6; color: #14B8A6;}
[data-testid="stChatMessage"] {background: #252B2F; border: 1px solid var(--line); border-radius: 16px;}
.disclaimer {text-align: center; color: var(--muted); font-size: .75rem; margin-top: .6rem;}

/* dashboard area */
.dash {border: 1px solid var(--line); border-radius: 16px; min-height: 420px; display: flex; flex-direction: column;
       align-items: center; justify-content: center; text-align: center; padding: 2rem; background-color: rgba(255,255,255,.03);
       background-image: radial-gradient(rgba(255,255,255,.07) 1px, transparent 1px); background-size: 22px 22px;}
.dash .ico {font-size: 2rem; border: 1px solid var(--line); border-radius: 14px; padding: .9rem 1rem; background: rgba(255,255,255,.05); margin-bottom: 1rem;}
.dash h3 {color: #fff; margin: .8rem 0 .3rem; font-size: 1.15rem; padding: 0;}
.dash p {color: var(--muted); max-width: 30rem; margin: 0; font-size: .9rem;}
.statusbar {color: var(--muted); font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .75rem; padding: .7rem .2rem;}
button[data-baseweb="tab"][aria-selected="true"] p {color: __ACCENT__ !important;}
[data-baseweb="tab-highlight"] {background-color: __ACCENT__ !important;}
[data-testid="stExpander"] {border: 1px solid var(--line); border-radius: 16px; background: var(--card);}
.tbl {width: 100%; border-collapse: collapse; font-size: .9rem;}
.tbl th {text-align: left; color: var(--muted); font-weight: 600; padding: .6rem .8rem; border-bottom: 1px solid var(--line);}
.tbl td {padding: .6rem .8rem; border-bottom: 1px solid rgba(255,255,255,.06); color: rgba(255,255,255,.9);}

/* footer (full width) */
.st-key-footerbar {background: #1E2428; border-top: 1px solid var(--line);
                   margin-left: calc(-1 * var(--gut)); margin-right: 0;
                   width: calc(100% + 2 * var(--gut)) !important; max-width: none !important;
                   box-sizing: border-box; padding: 1rem var(--gut);}
</style>
"""


def html(s):
    st.markdown(" ".join(line.strip() for line in s.strip().splitlines()), unsafe_allow_html=True)


def gap(rem=2):
    html(f'<div style="height:{rem}rem"></div>')


def inject_css(accent=TEAL, active=0):
    st.markdown(CSS.replace("__ACCENT__", accent).replace("__N__", str(active + 1)), unsafe_allow_html=True)


def header():
    with st.container(key="topbar"):
        left, mid, right = st.columns([2, 6, 2], vertical_alignment="center")
        with left:
            html(f'<div class="brand">{APP_NAME}<span class="dot"></span><span class="pill">{GROUP}</span></div>')
        with mid:
            with st.container(key="nav"):
                cols = st.columns([1, 1.5, 1.6, 1.1])
                for col, (path, label, icon) in zip(cols, PAGES):
                    with col:
                        st.page_link(path, label=label, icon=icon)
        with right:
            html(f'<div class="right"><div class="avatar">{PERSON_SVG}</div></div>')


def footer():
    gap(3)
    with st.container(key="footerbar"):
        left, middle, right = st.columns([1, 3, 1], vertical_alignment="center")
        with middle:
            html('<div class="muted small" style="text-align:center">'
                 'Group 5 · DS301 Introduction to Big Data · Synthetic data, not medical advice</div>')
        
def stat(value, caption):
    html(f'<div class="card stat"><div class="v">{value}</div><div class="c">{caption}</div></div>')


def kpi(label, value, caption, icon):
    html(f'<div class="card kpi"><div class="top"><span>{label}</span><span>{icon}</span></div>'
         f'<div class="v">{value}</div><div class="c">{caption}</div></div>')


def defect(icon, badge, title, text, mono):
    html(f'<div class="card defect"><div class="top"><span>{icon}</span><span class="badge">{badge}</span></div>'
         f'<h4>{title}</h4><p>{text}</p><div class="mono">{mono}</div></div>')


def table(df):
    html(df.to_html(index=False, classes="tbl", border=0))


def powerbi_embed(key, badge, height=640):
    url = POWERBI.get(key, "")
    if url:
        components.iframe(url, height=height, scrolling=False)
        st.link_button("Open full screen ↗", url)
    else:
        html(f'<div class="dash"><div class="ico">📊</div><span class="badge">● {badge}</span>'
             f'<h3>Power BI dashboard loads here</h3>'
             f'<p>Interactive dashboard connects to Microsoft Power BI Embedded. '
             f'Paste the publish-to-web link into POWERBI in utils.py.</p></div>')


def show_image(name):
    path = Path(__file__).parent / "assets" / name
    if path.exists():
        st.image(str(path))
    else:
        html(f'<div class="dash"><div class="ico">🖼️</div><h3>Image preview not available</h3>'
             f'<p>Save a screenshot of the dashboard as assets/{name} to show it here.</p></div>')


def dashboard(key, badge, status):
    tab_live, tab_img = st.tabs(["Live Dashboard", "View as Image"])
    with tab_live:
        powerbi_embed(key, badge)
    with tab_img:
        show_image(f"{key}_dashboard.png")
    html(f'<div class="statusbar">☁️ {status}</div>')