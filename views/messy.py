import pandas as pd
import streamlit as st

from utils import ICONS, RAW_FILE, dashboard, footer, gap, html, icon


TOTAL_RECORDS = 10_024_574
TOTAL_CELLS = 140_344_036
TOTAL_MISSING = 3_340_269
COMPLETE_RECORDS = 7_139_287
INCOMPLETE_RECORDS = 2_885_287

MISSING_BY_COLUMN = pd.DataFrame([
    ("Age", 354_457, 3.54), ("Gender", 378_279, 3.77),
    ("Smoking_status", 372_873, 3.72), ("Pack_years", 367_779, 3.67),
    ("Air_pollution_exposure", 372_715, 3.72), ("Genetic_risk", 375_167, 3.74),
    ("Chronic_lung_disease", 370_458, 3.70), ("Chest_pain", 374_434, 3.74),
    ("Shortness_of_breath", 374_107, 3.73), ("Patient_id", 0, 0.00),
    ("Record_id", 0, 0.00), ("branch_id", 0, 0.00),
    ("Visit_date", 0, 0.00), ("Diagnosis_result", 0, 0.00),
], columns=["Column", "Missing values", "Missing percentage"])
MISSING_BY_COLUMN["Data type"] = "Raw text"

MISSINGNESS_BY_RECORD = pd.DataFrame([
    (0, 7_139_287), (1, 2_468_679), (2, 380_342), (3, 34_237),
    (4, 1_952), (5, 75), (6, 2),
], columns=["Missing cells per record", "Records"])

BRANCHES = pd.DataFrame([
    ("NE-1565", 3_707_875), ("NW-6754", 3_110_409),
    ("SW-4543", 2_002_918), ("SE-6239", 1_203_372),
], columns=["Branch", "Records"])
BRANCHES["Share of records"] = BRANCHES["Records"] / TOTAL_RECORDS

DIAGNOSIS = pd.DataFrame([
    ("Positive", 2_170_475), ("Negative", 7_854_099),
], columns=["Observed diagnosis", "Records"])

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


def compact_kpi(label, value, exact, detail, tone="teal"):
    html(f'<div class="card eda-kpi {tone}" title="Exact value: {exact}">'
         f'<div class="top"><span>{label}</span>{icon(ICONS["chart"], size=18)}</div>'
         f'<div class="v">{value}</div><div class="c">{detail}</div>'
         f'<div class="eda-exact">Exact: {exact}</div></div>')


gap(3)
html('<div class="eyebrow">Step 1 · EDA &amp; Data Quality<span class="sub">• Raw ingestion reference</span></div>')
html('<div class="h1 mid">Data quality, explained clearly</div>')
html('<div class="lead">A presentation-ready view of the raw synthetic dataset: its size, missingness, format problems, and the work required before analysis.</div>')

gap(2)
summary = [
    ("Total records", "10.02M", "10,024,574", "Raw ingestion rows", "teal"),
    ("Features", "14", "14", "Columns in the raw schema", "teal"),
    ("Missing cells", "3.34M", "3,340,269", "Cells requiring a missingness decision", "red"),
    ("Overall missing rate", "2.38%", "3,340,269 / 140,344,036", "Share of all dataset cells", "red"),
    ("Complete records", "7.14M", "7,139,287", "71.22% have zero missing cells", "good"),
    ("Incomplete records", "2.89M", "2,885,287", "28.78% have one or more missing cells", "red"),
]
for row in (summary[:3], summary[3:]):
    for col, item in zip(st.columns(3), row):
        with col:
            compact_kpi(*item)
    gap(1)

html('<div class="section-title"><div><div class="h2">Key findings</div><div class="muted">The headline facts to use during a live walkthrough.</div></div></div>')
key_left, key_right = st.columns(2, gap="medium")
with key_left:
    html('<div class="card eda-note"><b>Missingness is broad, not isolated.</b><p>Nine columns contain missing values, ranging from 3.54% to 3.77%. Five columns have no missing values.</p></div>')
with key_right:
    html('<div class="card eda-note"><b>Low overall rate does not mean clean data.</b><p>Format variation, invalid values, and categorical inconsistency still need validation before analysis.</p></div>')

gap(3)
html('<div class="h2">Missing Values Analysis</div><div class="muted">Counts are aggregated EDA results. Hover the chart for exact values; no raw records are rendered.</div>')
gap(1)
chart_col, callout_col = st.columns([3, 1], gap="medium")
with chart_col:
    chart_data = MISSING_BY_COLUMN[MISSING_BY_COLUMN["Missing values"] > 0].sort_values("Missing values")
    st.bar_chart(chart_data, x="Missing values", y="Column", horizontal=True, color="#14B8A6", use_container_width=True)
with callout_col:
    html('<div class="card eda-callout"><span class="badge">Highest missingness</span><h4>Gender · 3.77%</h4><p>Gender has the highest observed missing percentage, closely followed by Genetic_risk and Chest_pain at 3.74%.</p></div>')

html('<div class="eda-interpretation">Out of 140.34 million dataset cells, 3.34 million are missing, representing approximately 2.38% of all cells. Nine columns contain missing values, with missingness ranging from approximately 3.54% to 3.77%. The remaining five columns have no missing values.</div>')
show_all = st.toggle("Show columns without missing values", value=True, help="Turn this off to focus only on fields that need a missingness decision.")
quality_table = MISSING_BY_COLUMN if show_all else MISSING_BY_COLUMN.query("`Missing values` > 0")
st.dataframe(quality_table.sort_values("Missing values", ascending=False), hide_index=True, use_container_width=True,
             column_config={"Column": st.column_config.TextColumn("Column name", help="Original raw dataset column name."),
                            "Missing values": st.column_config.NumberColumn("Missing count", format="%,d", help="Number of blank or missing entries in this column."),
                            "Missing percentage": st.column_config.NumberColumn("Missing percentage", format="%.2f%%", help="Missing count divided by 10,024,574 raw records."),
                            "Data type": st.column_config.TextColumn("Raw data type", help="All raw fields are ingested as text because of inconsistent representations.")})

gap(3)
html('<div class="h2">Missingness Distribution Across Records</div><div class="muted">How many missing cells each raw record contains.</div>')
distribution_col, distribution_note = st.columns([3, 1], gap="medium")
with distribution_col:
    st.bar_chart(MISSINGNESS_BY_RECORD, x="Missing cells per record", y="Records", color="#14B8A6", use_container_width=True)
with distribution_note:
    html('<div class="card eda-callout"><h4>Most gaps are single-cell gaps</h4><p>Approximately 71.22% of records are complete, while 28.78% contain at least one missing value. Most incomplete records contain only one missing value. A small number contain four or more.</p></div>')

gap(3)
html('<div class="h2">Data Dictionary · 6 Priority Features</div><div class="muted">Definitions, observed data-quality signals, and recommended cleaning actions. Examples are not counts.</div>')
for feature, status, definition, missing, anomalies, recommendation in PRIORITY_FEATURES:
    with st.expander(f"{feature} · {status}"):
        left, right = st.columns([1, 2], gap="large")
        with left:
            html(f'<div class="eda-detail"><span class="badge">{status}</span><h4>Missing: {missing}</h4><p><b>Definition</b><br>{definition}</p></div>')
        with right:
            html(f'<div class="eda-detail"><p><b>Identified anomalies</b><br>{anomalies}</p><p><b>Suggested action</b><br>{recommendation}</p></div>')

gap(3)
html('<div class="h2">Additional Data Quality Findings</div><div class="muted">Supporting checks that should inform, but not overcrowd, the priority-feature review.</div>')
branch_col, diagnosis_col = st.columns(2, gap="medium")
with branch_col:
    html('<div class="h3">Branch distribution</div><div class="muted small">Share of all raw records by branch.</div>')
    st.bar_chart(BRANCHES, x="Branch", y="Records", color="#14B8A6", use_container_width=True)
    st.dataframe(BRANCHES, hide_index=True, use_container_width=True,
                 column_config={"Records": st.column_config.NumberColumn(format="%,d"), "Share of records": st.column_config.ProgressColumn(format="%.2f%%", min_value=0, max_value=1)})
with diagnosis_col:
    html('<div class="h3">Observed diagnosis distribution</div><div class="muted small">Observed labels, not a model prediction or proof of diagnostic accuracy.</div>')
    st.bar_chart(DIAGNOSIS, x="Observed diagnosis", y="Records", color="#EF4444", use_container_width=True)
    html('<div class="card eda-detail"><p><b>Identifier columns</b><br>Patient_id and Record_id have no missing values and each has more than 100,000 unique values in the available summary. Their uniqueness per row has not been tested here.</p><p><b>Other fields to validate</b><br>Chest_pain (3.74%) and Shortness_of_breath (3.73%) include valid-looking 0/1 values. Genetic_risk (3.74%) includes Low, Medium, High; Air_pollution_exposure (3.72%) includes Very low through Very high.</p></div>')

gap(3)
html('<div class="h2">Recommended Data Cleaning Workflow</div><div class="muted">A deliberate sequence that keeps raw evidence, decisions, and validation separate.</div>')
workflow = [
    ("1", "Profile", "Identify missing values, types, unique values, and invalid ranges."),
    ("2", "Standardize", "Normalize whitespace, casing, dates, categories, and numeric representations."),
    ("3", "Validate", "Apply domain rules to ages, pack-years, dates, and binary fields."),
    ("4", "Handle Missingness", "Investigate patterns; retain, impute, or exclude according to the analytical objective."),
    ("5", "Verify", "Recalculate missingness, check types and duplicates, and confirm transformations introduced no errors."),
    ("6", "Document", "Record every transformation, assumption, and change in quality metrics."),
]
for items in (workflow[:3], workflow[3:]):
    for col, (number, title, text) in zip(st.columns(3), items):
        with col:
            html(f'<div class="card workflow"><span>{number}</span><h4>{title}</h4><p>{text}</p></div>')
    gap(1)

comparison = pd.DataFrame([("Raw records", "10,024,574", "Pending cleaning"), ("Missing cells", "3,340,269", "Pending cleaning"), ("Missing-cell rate", "2.38%", "Pending cleaning")], columns=["Metric", "Before cleaning", "After cleaning"])
html('<div class="h3">Before-and-after verification</div><div class="muted small">Post-cleaning metrics will appear here only when verified pipeline results are available.</div>')
st.dataframe(comparison, hide_index=True, use_container_width=True)

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
