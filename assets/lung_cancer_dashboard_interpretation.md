# Lung Cancer Dataset: Merged Dashboard Knowledge Base (Messy EDA + Clean Insights)

## 0. Metadata and How to Use This Document

You are a friendly, sweet assistant who explains this lung cancer dashboard data in simple words. Reply in Filipino (Taglish is fine) if the user writes in Filipino, otherwise reply in English. Keep answers short and use only the context below.

- **Purpose:** Knowledge context for an AI assistant answering questions about two linked dashboards built on one synthetic lung cancer dataset.
- **Part A (Sections 1-4):** the **messy** raw dataset and its data-quality dashboard.
- **Part B (Sections 5-6):** the **clean** dataset and the Lung Cancer Patient dashboard (Page 1 Overview, Page 2 Trends and Risk Factors).
- **Part C (Sections 7-10):** combined risk factors, verification, limitations, Q&A.
- **Pipeline:** raw messy data (10,024,574 rows) -> cleaning -> clean data (10,014,991 rows) -> analysis dashboard.
- **Data nature:** synthetic, rule-based (Faker plus rule-based diagnosis logic, then noise injected). Patterns reflect the generator's rules, **not real epidemiology**. Never present results as medical evidence.

### Routing rules
1. Questions on data quality, cleaning, spellings, blanks, bad ages/dates, or the "messy" dashboard -> Part A.
2. Questions on diagnosis rates, risk factors, trends, age, gender, smoking, symptoms -> Part B and Section 7.
3. **Record count:** messy file = **10,024,574**; clean dashboard = **10,014,991**. The 9,583-row gap (about 0.10%) is undocumented. Quote the number matching the dataset discussed; if unclear, say "about 10.0 million" and mention both.
4. Prefer **exact** figures over chart-read ("approx.") ones.
5. **Never quote the messy dashboard's treemap counts** (13x too high, see Section 8).
6. If something is not covered here, say so instead of guessing.

### Terminology
- Target column `Diagnosis_result` (Positive / Negative). The messy report calls it "lung-disease diagnosis", the clean dashboard "lung cancer". Same column.
- Clean dashboard "Unknown" = blank/null in raw data. "Smokers" = Smoking_status **Current** (raw Current total 3,992,365 matches the dashboard's about 3.99M).
- "Average Cigarette Packs" and "Tobacco Load" are assumed to be `Pack_years` (packs per day x years smoked); the unit is not stated.

---

# PART A: MESSY DATASET

Source: full 10M-row parquet file (all figures recomputed on the full file) and the data-quality dashboard PNG ("approx." = read by eye).

## 1. Dataset Overview

- **Size:** 10,024,574 rows x 14 columns (one row = one patient visit). Every column is stored as **text**, including numbers. Nulls are real nulls (0 blank strings); the only text placeholders are in `Visit_date` (`N/A`, `yesterday`).
- **Target:** Positive 2,170,475 (21.65%); Negative 7,854,099 (78.35%); no missing targets.
- **Columns:** Patient_id (`PTN-<digits>-<year>`, unique), Record_id (mirrors Patient_id), branch_id (NE-1565, NW-6754, SW-4543, SE-6239), Visit_date (day-first text, mixed formats), Age, Gender, Smoking_status (Current/Former/Never), Pack_years, Air_pollution_exposure (Very low to Very high), Genetic_risk (Low/Medium/High), Chronic_lung_disease, Chest_pain, Shortness_of_breath (0/1 flags), Diagnosis_result.
- **Sample raw row:** `PTN-1000002-2024 | SE-6239 | 29-09-2024 | Age -25 | Female | Former | Pack_years 11 | Low | Low | 0.0 | 0.0 | 0.0 | Negative`

## 2. Messy Dashboard Visuals

- **KPI cards:** Total Records 10,024,574; Data Completeness 71.22%; Max Missing per Row 6; Positive Rate 21.65%. The 71.22% is the share of rows with **no blanks** (7,139,287), not filled cells (97.62%); the label is misleading.
- **Header note:** "28.8% of rows have at least one blank" (exact 28.78%, 2,885,287 rows).
- **Missing Values by Column:** nine feature columns, 3.54% (Age) to 3.77% (Gender).
- **Blanks per row:** about 7.1M rows with 0, 2.5M with 1, 0.4M with 2, then almost none.
- **Age Problem:** missing (about 0.35M), negative (about 0.26M), over 100 (about 0.07M, mismatch), words (about 0.047M).
- **Positive rate by smoking:** Current about 34-35%, Former about 15-16%, Never about 3%; dotted line at 21.65%.
- **Misspelled Labels treemap:** counts are wrong (Section 8). It is titled "Misspelled Labels" but includes Blank. Red = Current variants, orange = Former, teal = Never.

## 3. Key Numbers (Raw Data)

| Metric | Value |
|---|---|
| Null cells | 3,340,269 of 140,344,036 (2.38%); cell completeness 97.62% |
| Rows with zero / at least one null | 7,139,287 (71.22%) / 2,885,287 (28.78%) |
| Max nulls in one row | 6 (2 rows) |
| Null rate per feature column | 3.54% to 3.77% |
| Unique Patient_id / Record_id | 10,024,574 each |
| Smoking_status / Gender raw spellings | 17 (plus nulls) -> 3 classes / 10 (plus nulls) -> 2 classes |
| Rows with problem Age | 757,392 (7.56%) |
| Age: negative / over 100 / words / under 18 / null | 257,969 / 92,929 / 46,514 / 5,523 / 354,457 |
| Pack_years: negative / over 100 / words / null | 990 / 4,019 / 3,064 / 367,779 |
| Visit_date: unparseable / outside 2016-2025 | 8,831 / 6,512 |
| Median age (valid ages 18-100) | 70 |
| Branch share of rows | NE 37.0%, NW 31.0%, SW 20.0%, SE 12.0% |

## 4. Messiness Findings, Cleaning Rules, Label Mappings

1. **Numbers stored as text.** Casting fails on values like `Twenty Five`; clean first.
2. **Blanks are random.** Nine feature columns at about 3.7% null each would give about 71% complete rows; the actual 71.22% fits independent random blanks. No row needs dropping; impute or flag.
3. **Smoking_status: 17 spellings, 3 classes.** Counting them separately would split Current into 5 groups, Former into 5, Never into 7.
4. **Gender: 10 spellings, 2 classes.** Strip trailing spaces and case.
5. **Age is the messiest.** Only 9,267,182 rows (92.45%) have a usable age of 18-100. Negative ages (-60 to -15) are likely sign flips. Over-100 values are four spikes (132, 242, 394, 900, about 23,000 each). Words include `Twenty Five` (23,317) and `SIx seven` (23,197, probably 67). Raw min -60, max 900, so the raw mean (69.94) is unreliable.
6. **Pack_years outliers.** 990 values are -28; 4,019 above 100 (spikes at 200, 300, 350, 400, about 1,000 each, plus 1,015 at exactly 100); 3,064 words (`forty two`). Valid range 0-100. The 1,208,227 zeros are mostly never-smokers.
7. **Visit_date has 18 formats.** 10,016,260 rows use `d-m-yyyy`/`dd-mm-yyyy` (517 invalid, e.g. `00-00-0000`). 8,314 rows use 17 junk formats (`yesterday`, `N/A`, `October 32, 2024`, `2024/13/45`, `10/05/24`, `20241005`), about 435-525 each. 6,512 parse but fall in 2000-2015 or 2028-2030 (injected). Real range 2016-2025, growing yearly (299,838 rows in 2016 to 1,800,305 in 2025).
8. **IDs and branch carry no signal.** ID year matches Visit_date year on 99.85% of rows. Positive rate is about 21.6% in all four branches. Drop IDs and branch before modeling.

**Cleaning recipe:** strip and lowercase text; map Gender and Smoking_status; convert word numbers; `abs()` negative ages and null ages outside 18-100; null Pack_years outside 0-100; parse dates day-first and drop years outside 2016-2025; impute or flag blanks; drop ID columns.

**Smoking_status mapping** (raw spelling: rows; trailing spaces ignored)
- **Former = 4,451,038:** Former 4,311,770; former 35,015; FORmER 34,772; Before 34,753; ForM3R 34,728.
- **Current = 3,992,365:** Current 3,405,517; Current(trailing space) 147,001; CUR 146,745; CURrENT 146,585; NOW 146,517.
- **Never = 1,208,298:** Never 1,119,945; Negative 14,947; NEvER 14,762; NEv 14,706; No 14,646; None 14,646; didnt 14,646.
- **Missing (null) = 372,873.**

**Gender mapping**
- **Male = 5,337,470:** Male 5,202,378; M 33,882; masc 33,778; Male(trailing space) 33,754; male 33,678.
- **Female = 4,308,825:** Female 4,198,808; F 27,684; fem 27,486; Female(trailing space) 27,481; female 27,366.
- **Missing (null) = 378,279.**

Mapping Negative/No/None/didnt/NEv to Never is a judgment call, supported by Pack_years: 99.94% of Never rows with a numeric Pack_years have 0.

---

# PART B: CLEAN DATASET (Lung Cancer Patient Dashboard)

Scope: 10,014,991 patients, years 2016-2025, branches NE/SE/NW/SW, ages 1-100. Two pages from a Power BI style report.

## 5. Clean Dashboard Structure

**Page 1 Overview:** KPI cards (Total Patients, Median Age, Positive Rate); Diagnosis Ratio donut; Age Distribution histogram (10-year bins); Average Cigarette Packs by Gender; Patient Genders; Smokers by Gender. Slicers: Age (1-100), Year (2016-2025), Month, Hospital Branch, Diagnosis.

**Page 2 Trends and Risk Factors:** yearly volume + positive rate combo chart (dual axis); 100% stacked bars of positive rate by Genetic Risk, Smoking Status, Air Pollution; Tobacco Load by Diagnosis; Diagnosis Probability by Key Symptoms (clustered columns). Filters: Age slider, Month/Year/Branch dropdowns.

**Colors:** Teal = Negative/general counts; Red = Positive; Orange = Shortness_of_breath.

## 6. Clean Dashboard Findings

### Page 1
- **KPIs:** 10,014,991 patients; median age **70**; positive rate **21.65%**.
- **Diagnosis:** Positive 2.17M (21.65%), Negative 7.85M (78.35%), about 1 in 4.6, imbalance about 1:3.6. Far above real-world prevalence, confirming a synthetic, enriched population.
- **Age:** unimodal, left-skewed, peak at **65-75** (about 3.55M). Approx. bins: 25-35 about 0.08M; 35-45 about 0.5M; 45-55 about 1.4M; 55-65 about 2.45M; 65-75 about 3.55M; 75-85 about 1.55M; 85-95 about 0.4M. Almost none under 25. Mostly adults 55-85.
- **Gender:** Male 5.3M (53%), Female 4.3M (43%), Unknown 0.4M (4%), matching the raw counts.
- **Smokers (Current):** Male 2.13M, Female 1.71M, Unknown 0.15M; total about 3.99M; prevalence about 40% in every gender. Males have more smokers only because there are more male patients.
- **Average cigarette packs:** 23 for Male, Female, and Unknown, so no gender effect on smoking. Check: 0.2165 x 32 + 0.7835 x 21 is about 23.4, matching the overall 23.

### Page 2
- **Yearly volume and positive rate:**

| Year | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|
| Patients (M) | 0.30 | 0.40 | 0.60 | 0.90 | 0.90 | 1.10 | 1.20 | 1.30 | 1.51 | 1.80 |
| Positive rate | 21.64% | 21.63% | 21.70% | 21.68% | 21.63% | 21.58% | 21.69% | 21.66% | 21.63% | 21.67% |

  Volume grew about 6x (plateau 2019-2020), but the positive rate stays within 21.58%-21.70% (about 0.12 points). The secondary axis is truncated (about 21.60%-21.70%), so the line looks volatile; the correct conclusion is **no temporal trend**.
- **Genetic risk:** monotonic Low < Medium < High (chart: about 12% / 30% / 65%; Unknown about 22%).
- **Smoking status:** Never < Former < Current (chart: about 3% / 16% / 34%; Unknown about 22%).
- **Air pollution:** Very Low about 9%, Low 12%, Medium 16%, High 29%, Very High about 40% (Unknown about 22%, near average; it is not an ordered level).
- **Tobacco load:** Positive **32** vs Negative **21** (about 52% higher).
- **Symptoms:** Chronic lung disease strongest, then chest pain, then shortness of breath. All raise probability above the 21.65% baseline; absence keeps it below. Interaction effects between symptoms are not shown.

---

# PART C: COMBINED ANALYSIS

## 7. Unified Risk-Factor Table (exact values from the full data)

| Factor | Group | Positive rate | Chart approx. |
|---|---|---|---|
| Smoking | Current / Former / Never | 33.76% / 15.93% / 2.75% | about 34 / 16 / 3% |
| Genetic risk | High / Low | 64.6% / 12.3% | about 65 / 12% (Medium about 30%) |
| Air pollution | Very high / Very low | 40.3% / 8.6% | about 40 / 9% |
| Chronic lung disease | Yes / No | 56.2% / 17.7% | about 0.56 / 0.18 |
| Chest pain | Yes / No | 40.2% / 14.6% | about 0.40 / 0.15 |
| Shortness of breath | Yes / No | 35.1% / 13.3% | about 0.35 / 0.14 |
| Age | 60-100 / 18-59 / 1-17 | 23.4% / 15.3% / 0.04% | not on dashboard |
| Gender | Male / Female | 23.7% / 19.1% | not on dashboard |
| Branch | NE, NW, SW, SE | about 21.6% each | not on dashboard |

**Ranking by spread (lowest to highest positive rate):** 1) Genetic risk about 52 pts; 2) Chronic lung disease about 38; 3) Air pollution about 32; 4) Smoking about 31; 5) Chest pain about 26; 6) Shortness of breath about 22.

**Ratios:** High genetic risk about 5x Low; Very high pollution about 4.7x Very low; Current smokers about 12x Never and about 2x Former; chronic lung disease about 3.2x lift.

**No effect:** gender on smoking behavior, year on positive rate, branch on positive rate. Gender has a modest effect on diagnosis (Male 23.7% vs Female 19.1%). All views are univariate; confounding is not controlled.

## 8. Messy Dashboard vs Data Check

Everything matches the data (Total Records, Completeness 71.22%, Max missing 6, Positive rate, 28.8% header, per-column null rates, blanks per row 7,139,287 / 2,468,679 / 380,342, Age missing/negative/words, smoking positive rates) **except**:

| Item | Dashboard | Data | Result |
|---|---|---|---|
| Age over 100 | about 0.07M | 92,929 (about 0.09M) | MISMATCH (about 69,544 if the age-900 spike is excluded; unverified) |
| Treemap: Blank | 4,847,349 | 372,873 | MISMATCH (13x) |
| Treemap: CUR / NOW | 1,907,685 / 1,904,721 | 146,745 / 146,517 | MISMATCH (13x) |
| Treemap: Before / ForM3R | 451,789 / 451,464 | 34,753 / 34,728 | MISMATCH (13x) |
| Treemap: Negative / NEv | 194,311 / 191,178 | 14,947 / 14,706 | MISMATCH (13x) |
| Treemap: didnt / No | 190,398 each | 14,646 each | MISMATCH (13x) |

Every treemap count is exactly 13x the real count (146,745 x 13 = 1,907,685), probably from row multiplication in the BI model (unverified). **Quote the data counts, not the treemap.**

**Cross-dashboard checks (all agree):** positive rate 21.65%; median age 70; gender counts; smokers = Current total; yearly volumes (299,838 to 1,800,305); smoking positive rates.

## 9. Cross-Cutting Insights and Limitations

- **Imbalance:** about 21.65% positive; models need stratified splits and recall/precision/PR-AUC, not accuracy alone.
- **Likely synthetic:** identical null rates in every column, injected spikes, 17 junk date formats at about 450-525 rows each, flat positive rate over 10 years, identical smoking metrics across genders.
- **Dose-response:** genetic risk, smoking, and pollution show clean ordered gradients (additive risk logic).
- **"Unknown" = random blanks:** Unknown groups sit near 22% positive (the average), consistent with evenly spread nulls.
- **Population skew:** older (median 70), male-leaning (53%), about 40% current smokers.
- **Volume growth is not a quality signal:** 6x more records, no change in positive rate.
- **Caveats:** results are association, not causation; "approx." chart values are about +/- 2 points; the 9,583-row gap between datasets is undocumented; not verified: duplicate rows on non-ID columns, percentiles other than the median, factor interactions, month breakdown, filtered views. Column meanings, the Never mapping, the cause of blanks, and whether the data is real are interpretations. Ambiguous values (`SIx seven`, `10/05/24`) cannot be resolved with certainty. The older 5M-row description (5,004,574 rows) is obsolete.

## 10. Sample Q&A

**Q: How big is the dataset?**
A: The raw messy file has 10,024,574 rows x 14 columns; the clean dashboard reports 10,014,991 patients. The 9,583-row difference is undocumented.

**Q: How messy is the raw data?**
A: 28.78% of rows have a blank, 7.56% have a bad or missing Age, Smoking_status has 17 spellings for 3 classes, Gender has 10 for 2, 8,831 dates cannot be parsed, and all columns are stored as text. Examples: `ForM3R`, `masc`, age -60 or 900, `Twenty Five`, `yesterday`.

**Q: Why are there blanks?**
A: Each feature column is 3.54%-3.77% null with no column pattern, and Unknown groups sit at the average positive rate (about 22%). That points to randomly injected missingness; the cause is not documented.

**Q: How was it cleaned?**
A: Strip and lowercase text, map Gender and Smoking_status, convert word numbers, abs() negative ages, null out-of-range ages and Pack_years, parse dates day-first and drop years outside 2016-2025, impute or flag blanks, drop IDs. Mapping tables are in Section 4.

**Q: Is the data real?**
A: Not verified, and it looks synthetic. Do not use it for medical conclusions.

**Q: What percentage is diagnosed positive?**
A: 21.65% (about 2.17M of roughly 10.01M), about 1 in 4.6.

**Q: Does smoking matter?**
A: Yes. Positive rate is 33.76% for Current, 15.93% for Former, 2.75% for Never. Positive patients have a higher tobacco load (32 vs 21).

**Q: Which risk factor is strongest?**
A: Genetic risk (64.6% positive for High vs 12.3% for Low), then chronic lung disease (56.2% vs 17.7%), very high pollution (40.3% vs 8.6%), and current smoking.

**Q: Does gender affect smoking? Does branch matter?**
A: Gender does not affect smoking (about 40% prevalence and 23 average packs in every gender; males have more smokers only because there are more males). Branch does not matter either: all four are about 21.6% positive.

**Q: Is the positive rate increasing over the years?**
A: No. Volume grew from 0.30M (2016) to 1.80M (2025), but the positive rate stayed between 21.58% and 21.70%. The line only looks jumpy because of a truncated axis.

**Q: What does the age distribution look like?**
A: Mostly older adults, peaking at 65-75 with a median of 70, and very few under 35. Ages 60-100 are 23.4% positive vs 15.3% for 18-59; ages 1-17 are almost never positive (0.04%).

**Q: Why are the messy dashboard's treemap numbers so large? What does "Data Completeness 71.22%" mean?**
A: Treemap counts are exactly 13x the real counts (e.g. CUR is 146,745, not 1,907,685), probably a BI model row multiplication. The 71.22% is the share of rows with no blanks; cell completeness is 97.62%.

**Q: Can these results be applied to real patients?**
A: No. The dataset is synthetic and rule-generated; results illustrate the dashboards' workflow and the generator's logic, not clinical findings.
