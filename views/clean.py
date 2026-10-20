import streamlit as st

from utils import CLEAN_FILE, ICONS, STATS, dashboard, defect, footer, gap, html, icon, kpi

gap(3)
html('<div class="eyebrow">Step 2 · The Cleaned Data<span class="sub">• Stage: Standardization &amp; Validation</span></div>')
html('<div class="h1 mid">Clean data, ready for answers</div>')
html('<div class="lead"><span class="hl">10 million</span> patient records, standardized and validated.</div>')

gap(2)
cards = [
    ("Cleaned rows", STATS["clean_records"], "Rows after cleaning", icon(ICONS["database"])),
    ("Schema width", STATS["clean_columns"], "Typed attribute columns", icon(ICONS["columns"])),
    ("Missing after cleaning", STATS["clean_missing"], "Blank cells left", icon(ICONS["check"])),
    ("Positive rate", STATS["positive_rate"], "Positive diagnosis rate", icon(ICONS["chart"])),
]
for col, args in zip(st.columns(4), cards):
    with col:
        kpi(*args)

gap(2)
dashboard("clean", "Validated · Indexed", f"Source: {CLEAN_FILE}")

gap(3)
html('<div class="h2">What we fixed</div>'
     '<div class="muted">Each problem found in the messy data, and how the cleaning step handled it.</div>')
gap(1)

# TODO: edit these so they match exactly what your cleaning pipeline did
FIXES = [
    (icon(ICONS["missing"]), "Fixed", "Missing values",
     "Blank cells were filled or marked as Unknown so every row stays usable.",
     "Result: no blank slots left"),
    (icon(ICONS["labels"]), "Fixed", "Inconsistent labels",
     "Casing and spelling variants were merged into one standard label per category.",
     "Result: one label per category"),
    (icon(ICONS["words"]), "Fixed", "Numbers written as words",
     "Text numbers were converted into real numeric values.",
     "Result: numeric columns work"),
    (icon(ICONS["impossible"]), "Fixed", "Impossible values",
     "Negative and out-of-range ages were flagged or removed.",
     "Result: realistic ranges only"),
    (icon(ICONS["dates"]), "Fixed", "Junk dates",
     "Mixed date formats were parsed into one standard date; junk entries were blanked.",
     "Result: time-series ready"),
    (icon(ICONS["text"]), "Fixed", "Everything is text",
     "Columns were converted to proper types: dates, numbers, and categories.",
     "Result: typed columns"),
]
for i, chunk in enumerate((FIXES[:3], FIXES[3:])):
    if i:
        gap(1)
    for col, d in zip(st.columns(3), chunk):
        with col:
            defect(*d)

gap(2)
with st.container(key="panel_next"):
    text_col, button_col = st.columns([3, 1], vertical_alignment="center")
    with text_col:
        html('<div class="h3" style="margin-top:0">Questions about the data?</div>'
             '<div class="muted">Ask the assistant what we found and how we cleaned it.</div>')
    with button_col.container(key="cta_primary"):
        st.page_link("views/bot.py", label="Chat with the AI →")

footer()