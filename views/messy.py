import pandas as pd
import streamlit as st

from utils import RAW_FILE, STATS, dashboard, defect, footer, gap, html, kpi, table

gap(3)
html('<div class="eyebrow">Step 1 · The Messy Data<span class="sub">• Stage: Ingestion &amp; Triage</span></div>')
html('<div class="h1 mid">Raw data, straight from the source</div>')
html('<div class="lead"><span class="hl">5 million</span> patient records with real-world mistakes baked in.</div>')

gap(2)
cards = [
    ("Cohort volume", STATS["records"], "Total ingestion rows", "🗄️"),
    ("Schema width", STATS["columns"], "Raw attribute columns", "📏"),
    ("Defect rate", STATS["raw_missing_rows"], "Rows with ≥1 missing cell", "⚠️"),
    ("Field sparsity", STATS["sparsity"], "Missing per feature column", "📊"),
]
for col, args in zip(st.columns(4), cards):
    with col:
        kpi(*args)

gap(2)
dashboard("messy", "Raw Ingestion Mode · Unindexed", f"Upstream unverified: {RAW_FILE}")

gap(3)
html('<div style="display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:1rem">'
     '<div><div class="h2">What&#39;s wrong with this data</div>'
     '<div class="muted">Taxonomy of corrupted records identified during initial automated scanning.</div></div>'
     '<span class="badge">6 Primary Anomaly Classes</span></div>')
gap(1)

DEFECTS = [
    ("⛔", "5.3–5.9%", "Missing values",
     "About 1 in 18 values blank across all 14 clinical and behavioral features.",
     "Impact: 265,000+ empty slots"),
    ("🔤", "11 &amp; 18", "Inconsistent labels",
     "Gender has 11 casing variations; smoking status exhibits 18 redundant permutations.",
     "E.g. 'f_m', 'male', 'MALE', 'Current-Smk'"),
    ("🔢", "23,316 ages", "Numbers written as words",
     "Natural language numbers ('Twenty Five', 'sixty_two') stored in numeric columns.",
     "Bypasses standard float converters"),
    ("🚨", "128,044 negative", "Impossible values",
     "Physiologically implausible numbers including negative patient ages (-4, -12) and ages &gt; 115.",
     "Truncates statistical standard deviations"),
    ("📅", "~4,100 rows", "Junk dates",
     "Relative strings ('yesterday', 'N/A') interleaved with ISO-8601, slash, and dash delimiters.",
     "Prevents time-series indexing"),
    ("🧾", "14 of 14", "Everything is text",
     "All 14 columns inferred as raw strings     by database parsers due to messy values.",
     "No native vector operations possible"),
]
for chunk in (DEFECTS[:3], DEFECTS[3:]):
    for col, d in zip(st.columns(3), chunk):
        with col:
            defect(*d)

gap(2)
DICTIONARY = pd.DataFrame(
    [
        ("Age", "Patient chronological age in years",
         "Negative integers (-4, -12), text phrases ('Twenty Five'), empty slots"),
        ("Gender", "Biological sex designation",
         "11 casing variations ('M', 'male', 'FEMALE', 'f_m', 'Unknown')"),
        ("Smoking_status", "Cigarette consumption categorization",
         "18 disparate string categories, broken hyphenations, and unknown abbreviations"),
        ("Pack_years", "Cumulative lifetime smoking exposure volume",
         "Stored as alphanumeric with suffixes ('15 packs', '?', 'N/A')"),
        ("Visit_date", "Clinical intake timestamp",
         "Mixed delimiters (YYYY/MM/DD, DD-MM-YYYY), localized strings ('yesterday')"),
        ("Chronic_lung_disease", "Pre-existing pulmonary condition flag",
         "Boolean values collapsed into loose strings 'yes', 'no', 'TRUE', '1'"),
    ],
    columns=["Column Name", "Target Definition", "Raw Defects Identified"],
)
with st.expander("Data dictionary · 6 Priority Features"):
    table(DICTIONARY)

gap(2)
with st.container(key="panel_next"):
    text_col, button_col = st.columns([3, 1], vertical_alignment="center")
    with text_col:
        html('<div class="h3" style="margin-top:0">Next: see how we cleaned it</div>'
             '<div class="muted">Inspect our pipeline transformations, imputation strategies, and schema standardization.</div>')
    with button_col.container(key="cta_primary"):
        st.page_link("views/clean.py", label="View cleaned dataset →")

footer()