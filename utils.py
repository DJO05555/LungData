import base64
import mimetypes
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image  # installed together with Streamlit

APP_NAME = "LungData"
TEAL, RED = "#14B8A6", "#EF4444"

GITHUB_URL = "https://github.com/DJO05555/LungData"
RAW_FILE = "lung_study_raw_v0.csv"             # TODO: raw file name shown under the messy dashboard
CLEAN_FILE = "cleaned_lung_cancer_dataset.csv" # TODO: cleaned file name

# Paste each Power BI "Publish to web" link between the quotes (the src="..." inside the iframe code).
# It must start with https://app.powerbi.com/view?r=   ("" = placeholder box)
POWERBI = {
    "messy": "https://app.powerbi.com/reportEmbed?reportId=f8d82a2d-c8b1-4199-97a8-8be7c9efc1d8&autoAuth=true&ctid=cceb61f2-e867-476f-8597-b4cf22555bc4",
    "clean": "https://app.powerbi.com/reportEmbed?reportId=023dec27-f439-42c2-b7d9-ef3985f8c1a9&autoAuth=true&ctid=cceb61f2-e867-476f-8597-b4cf22555bc4",
}

STATS = {
    "records": "10,024,574",
    "columns": "14",
    "raw_missing_rows": "28.8%",
    "sparsity": "3.5-3.8%",
    "positive_rate": "21.65%",
    "clean_records": "10,014,808",      # TODO: rows after cleaning
    "clean_columns": "14",      # TODO: columns after cleaning
    "clean_missing": "0",      # TODO: blank cells left after cleaning
}

TEAM = [
    ("RA", "Ralph Zedrick Abayon", "Lead Architect"),
    ("LE", "Lance Evangelista", "Data Pipeline"),
    ("HO", "Hansel Nino Ofilan", "ML Modeling"),
    ("DO", "Dardy Jr. Onia", "Frontend & AI"),
    ("MS", "Marc Deanielle Santiago", "EDA & Quality"),
]

PAGES = [
    ("views/home.py", "Home"),
    ("views/messy.py", "Messy Data"),
    ("views/clean.py", "Cleaned Data"),
    ("views/bot.py", "AI Bot"),
]

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
html, body, .stApp {margin: 0; overflow-x: hidden;}
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer {display: none !important;}
.block-container, [data-testid="stMainBlockContainer"] {max-width: none !important; padding: 0 var(--gut) 0 var(--gut) !important;}
.muted {color: var(--muted);}
.small {font-size: .8rem;}
.dot {display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #14B8A6;}

/* ---------- top bar (full width) ---------- */
.st-key-topbar {position: sticky; top: 0; z-index: 999; background: #1E2428; border-bottom: 1px solid var(--line);
                margin: 0 calc(-1 * var(--gut)) 0 !important;
                width: calc(100% + 2 * var(--gut)) !important; max-width: none !important;
                box-sizing: border-box; padding: 0 var(--gut);}
.brand {display: flex; align-items: center; gap: .5rem; font-weight: 700; font-size: 1.25rem; color: #fff; white-space: nowrap;}
.st-key-nav [data-testid="stHorizontalBlock"] {justify-content: flex-end; gap: 32px !important;}
.st-key-nav [data-testid="stColumn"] {width: auto !important; flex: 0 0 auto !important; min-width: 0 !important;}
.st-key-nav a {background: transparent !important; justify-content: center; border-radius: 0 !important;
               padding: 1.25rem 0 !important; border-bottom: 2px solid transparent; gap: 0; white-space: nowrap;}
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
.about {display: flex; justify-content: space-between; align-items: center; gap: 2rem; padding: 2rem;}
.about .facts {display: grid; gap: 1rem;}
.about .row {display: flex; align-items: center; gap: .7rem; color: rgba(255,255,255,.9); font-size: 1rem;}
.line-icon {width: 20px; height: 20px; flex: 0 0 20px; color: #14B8A6; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; fill: none; stroke: currentColor;}
.ico24 .line-icon {width: 20px; height: 20px; color: rgba(255,255,255,.7);}
.tech-tiles {display: grid; grid-template-columns: repeat(4, 130px); gap: 10px; align-items: center;}
.tech-tile {width: 130px; height: 96px; border: 1px solid var(--line); border-radius: 12px; background: rgba(255,255,255,.04);
            display: flex; flex-direction: column; justify-content: center; align-items: center; box-sizing: border-box; overflow: hidden;}
.tech-tile img {display: block; height: 40px; max-width: 92px; object-fit: contain; margin-bottom: 7px;}
.tech-tile span {color: var(--muted); font-size: .7rem; font-weight: 600; line-height: 1;}
.member {text-align: center;}
.member .av {width: 48px; height: 48px; border-radius: 50%; border: 1px solid rgba(255,255,255,.2);
             background: rgba(255,255,255,.08); display: grid; place-items: center; margin: 0 auto .7rem;
             color: #fff; font-weight: 700; font-size: .85rem;}
.member b {display: block; color: #fff; font-size: .9rem;}
.member span {color: var(--muted); font-size: .75rem;}

/* explore cards (container with a colored top edge) */
[class*="st-key-card_"] {background: var(--card); border: 1px solid var(--line); border-top: 3px solid rgba(255,255,255,.3);
                         border-radius: 16px; padding: 1.5rem; height: 264px; box-sizing: border-box; overflow: hidden;}
.st-key-explore_grid [data-testid="stHorizontalBlock"] {gap: 24px !important;}
[class*="st-key-card_"] [data-testid="stVerticalBlock"] {height: 100%; display: flex; flex-direction: column;}
[class*="st-key-card_"] [data-testid="stPageLink-NavLink"], [class*="st-key-card_"] .lnk {margin-top: auto;}
.st-key-card_messy {border-top-color: #EF4444 !important;}
.st-key-card_clean {border-top-color: #14B8A6 !important;}
[class*="st-key-card_"] a {padding: 0 !important; background: transparent !important;}
[class*="st-key-card_"] a p {color: #14B8A6 !important; font-weight: 600; font-size: .88rem; margin: 0;}
.lnk {color: #14B8A6; font-weight: 600; font-size: .88rem; text-decoration: none;}
.ico24 {height: 20px; line-height: 1;}

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
[data-testid="stChatMessage"] {background: #252B2F; border: 1px solid var(--line); border-radius: 16px;}
.disclaimer {text-align: center; color: var(--muted); font-size: .75rem; margin-top: .6rem;}
.st-key-bot_info_grid [data-testid="stHorizontalBlock"] {gap: 24px !important;}
.st-key-bot_info_grid [class*="st-key-panel_"] {height: 136px; box-sizing: border-box; overflow: hidden;}
.st-key-bot_info_grid .ask {display: inline-flex; width: 32%; margin: .35rem 0; gap: .45rem; vertical-align: top;}
.st-key-bot_info_grid .ask .ico {width: 28px; height: 28px; border: 0; background: transparent;}
.st-key-bot_info_grid .ask .ico svg {width: 20px; height: 20px;}
.st-key-bot_info_grid .ask span {font-size: .72rem; line-height: 1.25;}
.st-key-bot_info_grid .good {display: inline-block; width: 31%; margin: .45rem 0; vertical-align: top; font-size: .8rem;}
.st-key-panel_chat {height: 75vh; min-height: 580px; max-height: 780px; display: flex; flex-direction: column; box-sizing: border-box;}
.st-key-panel_chat [data-testid="stVerticalBlock"] {min-height: 0;}
.st-key-panel_chat [data-testid="stChatInput"] {margin-top: auto; padding-top: .75rem;}
.st-key-panel_chat [class*="st-key-chat_messages"] {height: clamp(330px, 52vh, 560px) !important; overflow-y: auto; padding-right: .25rem;}
.st-key-panel_chat .st-key-new_chat button {width: 100%; border: 1px solid var(--line); color: rgba(255,255,255,.8); background: transparent; border-radius: 8px; font-size: .78rem; padding: .45rem .6rem;}
.chat-avatar {width: 34px; height: 34px; flex: 0 0 34px; border-radius: 50%; overflow: hidden; box-shadow: 0 0 12px rgba(20,184,166,.25);}
.chat-avatar svg {display: block; width: 100%; height: 100%;}
[class*="st-key-chat_message_"] {margin: .85rem 0;}
[class*="st-key-chat_message_"] [data-testid="stHorizontalBlock"] {gap: .65rem; align-items: flex-start;}
[class*="st-key-chat_bubble_"] {background: #252B2F; border: 1px solid var(--line); border-radius: 14px; padding: .75rem .9rem; box-sizing: border-box;}
[class*="st-key-chat_bubble_user_"] {background: rgba(20,184,166,.14); border-color: rgba(20,184,166,.28);}
[class*="st-key-chat_bubble_"] [data-testid="stMarkdownContainer"] {color: rgba(255,255,255,.92); font-size: .9rem; line-height: 1.55; overflow-wrap: anywhere;}
[class*="st-key-chat_bubble_"] [data-testid="stMarkdownContainer"] > :first-child {margin-top: 0;}
[class*="st-key-chat_bubble_"] [data-testid="stMarkdownContainer"] > :last-child {margin-bottom: 0;}
[class*="st-key-chat_bubble_"] h1, [class*="st-key-chat_bubble_"] h2, [class*="st-key-chat_bubble_"] h3 {color: #fff; line-height: 1.25; margin: 1rem 0 .45rem;}
[class*="st-key-chat_bubble_"] h1 {font-size: 1.2rem;} [class*="st-key-chat_bubble_"] h2 {font-size: 1.08rem;} [class*="st-key-chat_bubble_"] h3 {font-size: 1rem;}
[class*="st-key-chat_bubble_"] p {margin: .45rem 0;}
[class*="st-key-chat_bubble_"] ul, [class*="st-key-chat_bubble_"] ol {margin: .45rem 0; padding-left: 1.25rem;}
[class*="st-key-chat_bubble_"] li {margin: .2rem 0;}
[class*="st-key-chat_bubble_"] code {background: rgba(255,255,255,.09); color: #b7f3ed; border-radius: 4px; padding: .1rem .3rem; font-size: .82em;}
[class*="st-key-chat_bubble_"] pre {max-width: 100%; overflow-x: auto; background: #161c20; border: 1px solid var(--line); border-radius: 8px; padding: .75rem;}
[class*="st-key-chat_bubble_"] pre code {background: transparent; padding: 0; color: rgba(255,255,255,.9);}
[class*="st-key-chat_bubble_"] table {display: block; width: max-content; min-width: 100%; max-width: 100%; overflow-x: auto; border-collapse: collapse; margin: .7rem 0;}
[class*="st-key-chat_bubble_"] th, [class*="st-key-chat_bubble_"] td {border: 1px solid rgba(255,255,255,.16); padding: .45rem .6rem; text-align: left; white-space: nowrap;}
[class*="st-key-chat_bubble_"] th {background: rgba(20,184,166,.14); color: #fff; font-weight: 700;}
[class*="st-key-chat_bubble_"] td {color: rgba(255,255,255,.82);}

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

/* Expanded data dictionary */
.eda-detail {padding: .25rem 0;}
.eda-detail b {color: #fff; font-size: .9rem;}
.eda-detail p {margin: .45rem 0 0; color: var(--muted); font-size: .86rem; line-height: 1.55;}

/* footer (full width) */
.st-key-footerbar {background: #1E2428; border-top: 1px solid var(--line);
                   margin-left: calc(-1 * var(--gut)); margin-right: 0;
                   width: calc(100% + 2 * var(--gut)) !important; max-width: none !important;
                   box-sizing: border-box; padding: 1rem var(--gut);}
</style>
"""

# ---------- image slider (runs inside its own small page, so it needs its own CSS and JS) ----------
SLIDER_DOC = """
<style>
html, body {margin: 0; background: transparent; font-family: Inter, system-ui, sans-serif;}
.wrap {position: relative; width: 100%; height: 100vh; box-sizing: border-box; overflow: hidden;
       border: 1px solid rgba(255,255,255,.12); border-radius: 16px; background: #0E1418;}
.slide {position: absolute; inset: 0; display: none; align-items: center; justify-content: center;}
.slide.on {display: flex;}
.slide img {max-width: 100%; max-height: 100%; object-fit: contain;}
.arrow {position: absolute; top: 50%; transform: translateY(-50%); width: 36px; height: 36px; padding: 0;
        border: none; border-radius: 50%; cursor: pointer; display: grid; place-items: center; color: #111;
        background: rgba(255,255,255,.65); box-shadow: 0 2px 8px rgba(0,0,0,.35); transition: background .2s, transform .2s;}
.arrow:hover {background: rgba(255,255,255,.95); transform: translateY(-50%) scale(1.08);}
.prev {left: 12px;}
.next {right: 12px;}
.count {position: absolute; bottom: 10px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,.55);
        color: #fff; font-size: 12px; padding: 3px 12px; border-radius: 999px;}
</style>
<div class="wrap">
__SLIDES__
__ARROWS__
<div class="count" id="count"></div>
</div>
<script>
const slides = Array.from(document.querySelectorAll('.slide'));
const count = document.getElementById('count');
let i = 0;
function show(n) {
  i = (n + slides.length) % slides.length;
  slides.forEach((s, k) => s.classList.toggle('on', k === i));
  count.textContent = 'Page ' + (i + 1) + ' of ' + slides.length;
}
const prev = document.getElementById('prev'), next = document.getElementById('next');
if (prev) prev.onclick = () => show(i - 1);
if (next) next.onclick = () => show(i + 1);
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowLeft') show(i - 1);
  if (e.key === 'ArrowRight') show(i + 1);
});
show(0);
</script>
"""

ARROWS = (
    '<button class="arrow prev" id="prev" aria-label="Previous page">'
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
    'stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg></button>'
    '<button class="arrow next" id="next" aria-label="Next page">'
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
    'stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg></button>'
)


# ---------- shared line icons (used by the messy and cleaned pages) ----------
def icon(paths, size=22, color="#9aa4ad"):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.75" '
        f'stroke-linecap="round" stroke-linejoin="round">{paths}</svg>'
    )


ICONS = {
    "missing": '<circle cx="12" cy="12" r="9" stroke-dasharray="3 3"/>',
    "labels": '<path d="M20.6 13.4l-7.2 7.2a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.2"/>',
    "words": '<line x1="4" y1="9" x2="20" y2="9"/><line x1="4" y1="15" x2="20" y2="15"/><line x1="10" y1="3" x2="8" y2="21"/><line x1="16" y1="3" x2="14" y2="21"/>',
    "impossible": '<circle cx="12" cy="12" r="9"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>',
    "dates": '<rect x="3" y="4" width="18" height="17" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><line x1="10" y1="14" x2="14" y2="18"/><line x1="14" y1="14" x2="10" y2="18"/>',
    "text": '<polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15" y2="20"/><line x1="12" y1="4" x2="12" y2="20"/>',
    "database": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "columns": '<rect x="3" y="3" width="18" height="18" rx="2"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/>',
    "alert": '<path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    "chart": '<line x1="6" y1="20" x2="6" y2="12"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="18" y1="20" x2="18" y2="9"/>',
    "check": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
}


def html(s):
    st.markdown(" ".join(line.strip() for line in s.strip().splitlines()), unsafe_allow_html=True)


def gap(rem=2):
    html(f'<div style="height:{rem}rem"></div>')


def inject_css(accent=TEAL, active=0):
    st.markdown(CSS.replace("__ACCENT__", accent).replace("__N__", str(active + 1)), unsafe_allow_html=True)


def header():
    with st.container(key="topbar"):
        left, right = st.columns([1, 3], vertical_alignment="center")
        with left:
            html(f'<div class="brand">{APP_NAME}<span class="dot"></span></div>')
        with right:
            with st.container(key="nav"):
                cols = st.columns(len(PAGES), gap=None)
                for col, (path, label) in zip(cols, PAGES):
                    with col:
                        st.page_link(path, label=label)


def footer():
    gap(3)
    with st.container(key="footerbar"):
        left, middle, right = st.columns([1, 3, 1], vertical_alignment="center")
        with middle:
            html('<div class="muted small" style="text-align:center">'
                 'Group 5 · Introduction to Big Data · Synthetic data, not medical advice</div>')


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


def _slide_files(key):
    folder = Path(__file__).parent / "assets"
    files = []
    for ext in ("png", "jpg", "jpeg"):
        files += folder.glob(f"{key}_dashboard*.{ext}")
    return sorted(files)


@st.cache_data(show_spinner=False)
def _load_slides(items):
    # items = ((path, modified-time), ...); the modified time refreshes the cache when you replace an image
    uris, ratios = [], []
    for path_str, _ in items:
        p = Path(path_str)
        mime = mimetypes.guess_type(p.name)[0] or "image/png"
        uris.append(f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}")
        with Image.open(p) as im:
            ratios.append(im.height / im.width)
    return uris, ratios


def image_slider(key, width=1180):
    files = _slide_files(key)
    if not files:
        html(f'<div class="dash"><div class="ico">🖼️</div><h3>Image preview not available</h3>'
             f'<p>Save screenshots of the dashboard pages as assets/{key}_dashboard_1.png, '
             f'assets/{key}_dashboard_2.png, and so on.</p></div>')
        return
    uris, ratios = _load_slides(tuple((str(f), f.stat().st_mtime) for f in files))
    slides = "".join(
        f'<div class="slide"><img src="{uri}" alt="Dashboard page {n}"></div>' for n, uri in enumerate(uris, start=1)
    )
    doc = SLIDER_DOC.replace("__SLIDES__", slides).replace("__ARROWS__", ARROWS if len(uris) > 1 else "")
    height = max(360, min(900, int(width * max(ratios))))
    components.html(doc, height=height)


def dashboard(key, badge, status):
    tab_live, tab_img = st.tabs(["Live Dashboard", "View as Image"])
    with tab_live:
        powerbi_embed(key, badge)
    with tab_img:
        image_slider(key)
    html(f'<div class="statusbar">☁️ {status}</div>')
