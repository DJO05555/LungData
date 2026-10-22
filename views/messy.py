import streamlit as st

from utils import ICONS, RAW_FILE, STATS, dashboard, footer, gap, html, icon, kpi


PRIORITY_FEATURES = [
    ("Age", "Missing Values · Invalid Values", "Patient chronological age in years.", "354,457 (3.54%)",
     "Negative ages such as -60 and -4; implausible ages such as 900; text values including ‘Twenty Five’ and ‘SIx seven’.",
     "Convert valid numeric and recognized text representations to one numeric format. Flag invalid or implausible values for investigation rather than silently replacing them."),
    ("Gender", "Missing Values · Inconsistent Categories", "Recorded patient gender or sex category, according to the dataset documentation.", "378,279 (3.77%)",
     "Variants include Male, male, Male , M, masc, Female, female, F, and fem.",
     "Trim whitespace, standardize capitalization, and map only semantically equivalent categories. Preserve unknown or ambiguous values instead of guessing."),
    ("Smoking_status", "Missing Values · Inconsistent Categories", "Cigarette smoking status.", "372,873 (3.72%)",
     "Variants include Former, former, ForM3R, Current, CUR, CURrENT, NOW, Never, NEv, Before, No, and None.",
     "Normalize casing and whitespace, then map clearly equivalent labels to Current, Former, and Never. Review ambiguous terms such as Negative, No, and None before assigning a status."),
    ("Pack_years", "Missing Values · Requires Validation", "Cumulative lifetime cigarette-smoking exposure, expressed in pack-years.", "367,779 (3.67%)",
     "Numeric range detected: -28 to 400. Text representations include Twenty three, twenty five, and forty two.",
     "Convert recognized number words and valid numeric strings. Flag negative and clinically implausible values for review; do not automatically remove high values without domain validation."),
    ("Visit_date", "Requires Validation", "Clinical intake or visit date.", "0 (0.00%)",
     "3,681 unique values. Mixed day-month-year strings and numeric values such as 20241005.",
     "Parse dates using explicit, validated formats, standardize to one representation, and flag invalid or ambiguous values. Do not treat every numeric value as a valid date without verification."),
    ("Chronic_lung_disease", "Missing Values · Requires Validation", "Indicator for a pre-existing chronic lung disease.", "370,458 (3.70%)",
     "Observed values include 0 and 1.",
     "Standardize valid binary representations to Boolean or documented 0/1 encoding. Investigate unexpected strings and do not treat missing values as negative cases."),
]


gap(3)
html('<div class="eyebrow">Step 1 · EDA &amp; Data Quality<span class="sub">• Raw ingestion reference</span></div>')
html('<div class="h1 mid">Data quality, explained clearly</div>')
html('<div class="lead">A presentation-ready view of the raw synthetic dataset: its size, missingness, format problems, and the work required before analysis.</div>')

gap(2)
cards = [
    ("Cohort volume", STATS["records"], "Total ingestion rows", icon(ICONS["database"])),
    ("Schema width", STATS["columns"], "Raw attribute columns", icon(ICONS["columns"])),
    ("Defect rate", STATS["raw_missing_rows"], "Rows with ≥1 missing cell", icon(ICONS["alert"])),
    ("Field sparsity", STATS["sparsity"], "Missing per feature column", icon(ICONS["chart"])),
]
for col, args in zip(st.columns(4), cards):
    with col:
        kpi(*args)

gap(3)
html('<div class="h2">Data Dictionary · 6 Priority Features</div><div class="muted">Definitions, observed data-quality signals, and recommended cleaning actions. Examples are not counts.</div>')
for feature, status, definition, missing, anomalies, recommendation in PRIORITY_FEATURES:
    with st.expander(f"{feature} · {status}"):
        left, right = st.columns([1, 2], gap="large")
        with left:
            html(f'<div class="eda-detail"><span class="badge">{status}</span><h4>Missing: {missing}</h4><p><b>Definition</b><br>{definition}</p></div>')
        with right:
            html(f'<div class="eda-detail"><p><b>Identified anomalies</b><br>{anomalies}</p><p><b>Suggested action</b><br>{recommendation}</p></div>')

gap(2)
with st.expander("Raw dashboard reference"):
    st.caption(f"Embedded source report for reference: {RAW_FILE}.")
    dashboard("messy", "Raw Ingestion Mode · Unindexed", f"Upstream unverified: {RAW_FILE}")

gap(2)
with st.container(key="panel_next"):
    text_col, button_col = st.columns([3, 1], vertical_alignment="center")
    with text_col:
        html('<div class="h3" style="margin-top:0">Next: see how we cleaned it</div><div class="muted">Inspect pipeline transformations, imputation strategies, and schema standardization.</div>')
    with button_col.container(key="cta_primary"):
        st.page_link("views/clean.py", label="View cleaned dataset →")

footer()
