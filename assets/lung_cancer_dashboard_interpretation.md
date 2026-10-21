# Lung Cancer Patient Dashboard: Interpretation Knowledge Base

## 0. Document Metadata

- **Purpose:** Knowledge context for a Cache-Augmented Generation (CAG) assistant that answers questions about the Lung Cancer Patient Dashboard.
- **Source:** Two dashboard pages (Page 1: Overview, Page 2: Trends and Risk Factors), Power BI style report.
- **Data nature:** Synthetic, rule-based patient dataset (generated with Faker plus rule-based diagnosis logic, then noise-injected). Patterns reflect the generator's rules, **not real-world epidemiology**.
- **Dataset scope:** 10,014,991 patient records, years 2016-2025, four hospital branches (NE, SE, NW, SW), patient ages 1-100.
- **Reading note:** Values labeled "approx." were estimated visually from bar lengths and are accurate to roughly +/- 2 percentage points. Values without that label are printed on the dashboard.

---

## 1. Dashboard Structure

### Page 1: Overview

| Component | Type | Purpose |
|---|---|---|
| Total Number of Patients | KPI card | Record volume |
| Median of Age | KPI card | Typical patient age |
| Positive Rate | KPI card | Share of positive lung cancer diagnoses |
| Patient Diagnosis Ratio | Donut chart | Positive vs. negative split |
| Patient Age Distribution | Histogram (10-year bins) | Age profile of patients |
| Average Cigarette Packs by Gender | Bar chart | Smoking exposure by gender |
| Total Number of Patient Genders | Bar chart | Gender composition |
| Total Number of Smokers by Gender | Bar chart | Smoker counts by gender |
| Filter panel (right side) | Slicers | Age (1-100), Year (2016-2025), Month, Hospital Branch (NE/SE/NW/SW), Diagnosis (Negative/Positive) |

### Page 2: Trends and Risk Factors

| Component | Type | Purpose |
|---|---|---|
| Total Records and Positive Diagnostic Rate Trend | Combo chart (bars + line, dual axis) | Yearly volume and positive rate |
| Lung Cancer Rate by Genetic Risk | 100% stacked horizontal bar | Positive vs. negative share per genetic risk level |
| Lung Cancer Rate by Smoking Status | 100% stacked horizontal bar | Positive vs. negative share per smoking status |
| Lung Cancer Rate by Air Pollution Exposure | 100% stacked horizontal bar | Positive vs. negative share per pollution level |
| Tobacco Load by Diagnosis | Horizontal bar | Average tobacco exposure per diagnosis group |
| Diagnosis Probability by Key Symptoms | Clustered column chart | Positive probability by symptom presence (Yes/No) |
| Filters | Age slider, Month / Year / Hospital Branch dropdowns | Interactive filtering |

**Color convention:** Teal = Negative (and general counts); Red = Positive; Orange = Shortness_of_breath series in the symptom chart.

---

## 2. Page 1: Overview Findings

### 2.1 Headline KPIs

- **Total patients:** 10,014,991 (about 10.01 million).
- **Median age:** 70 years.
- **Positive rate:** 21.65%.

### 2.2 Diagnosis Ratio

- Positive: **2.17M patients (21.65%)**.
- Negative: **7.85M patients (78.35%)**.
- Roughly **1 in 5 patients** is positive, so the classes are **imbalanced (about 1:3.6 positive to negative)**.
- This is far higher than real-world lung cancer prevalence, which confirms the dataset is a synthetic, enriched population.

### 2.3 Age Distribution

- Shape: **unimodal and left-skewed** (long tail toward younger ages).
- Approx. bin counts: 25-35 about 0.08M; 35-45 about 0.5M; 45-55 about 1.4M; 55-65 about 2.45M; **65-75 about 3.55M (peak)**; 75-85 about 1.55M; 85-95 about 0.4M; 95+ negligible.
- Almost no patients are under 25.
- The peak at 65-75 is consistent with the **median age of 70**.
- **Interpretation:** The population is predominantly older adults (roughly 55-85), which matches the typical age profile of lung cancer screening and diagnosis cohorts.

### 2.4 Gender Composition

| Gender | Patients | Approx. share |
|---|---|---|
| Male | 5.3M | 53% |
| Female | 4.3M | 43% |
| Unknown | 0.4M | 4% |

- Males are the largest group; females are about 81% of the male count.
- The **"Unknown" category (about 4%)** likely reflects injected noise or missing values in the data-cleaning stage.

### 2.5 Smokers by Gender

| Gender | Smokers | Approx. smoking prevalence within gender |
|---|---|---|
| Male | 2.13M | about 40% |
| Female | 1.71M | about 40% |
| Unknown | 0.15M | about 38% |
| **Total** | **about 3.99M** | **about 40% of all patients** |

- Smoking prevalence is **nearly identical across genders (about 40%)**. Males have more smokers in absolute terms only because there are more male patients.

### 2.6 Average Cigarette Packs by Gender

- Male = **23**, Female = **23**, Unknown = **23**. Smoking intensity is identical across genders.
- Combined with 2.5, the data shows **no gender effect on smoking behavior**, which strongly suggests the generator does not condition smoking variables on gender.
- Consistency check: weighting the Page 2 tobacco load values (32 for positive, 21 for negative) by group size gives 0.2165 x 32 + 0.7835 x 21, about 23.4, which matches the overall average of 23.

---

## 3. Page 2: Trends and Risk Factor Findings

### 3.1 Yearly Volume and Positive Rate Trend

**Total patients per year (bars):**

| Year | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|
| Patients (M) | 0.30 | 0.40 | 0.60 | 0.90 | 0.90 | 1.10 | 1.20 | 1.30 | 1.51 | 1.80 |

**Positive rate per year (line, secondary axis):**

| Year | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|
| Positive rate | 21.64% | 21.63% | 21.70% | 21.68% | 21.63% | 21.58% | 21.69% | 21.66% | 21.63% | 21.67% |

- The yearly volumes sum to about 10.01M, matching the total record count.
- **Volume growth:** records grew about **6x** from 2016 (0.30M) to 2025 (1.80M), with a plateau in 2019-2020 (both 0.90M). 2025 is the highest year.
- **Positive rate is essentially flat:** it stays within **21.58%-21.70%**, a range of only about **0.12 percentage points**. The lowest point is 2021 (21.58%), the highest is 2018 (21.70%).
- **Visual caution:** the secondary axis is truncated (about 21.60%-21.70%), so the line looks volatile. The real variation is negligible. The correct conclusion is that **there is no meaningful temporal trend in positive rate**, and growth in volume does not change the share of positives.

### 3.2 Lung Cancer Rate by Genetic Risk (approx.)

| Genetic risk | Approx. negative | Approx. positive |
|---|---|---|
| Low | 88% | 12% |
| Unknown | 78% | 22% |
| Medium | 70% | 30% |
| High | 35% | **65%** |

- Strong **monotonic dose-response**: positive rate rises from Low to Medium to High.
- **High genetic risk patients are positive about 65% of the time, roughly 5 times the Low-risk rate** and about 3 times the overall average (21.65%).
- "Unknown" sits near the overall average (about 22%), consistent with missing values spread randomly.

### 3.3 Lung Cancer Rate by Smoking Status (approx.)

| Smoking status | Approx. negative | Approx. positive |
|---|---|---|
| Never | 97% | about 3% |
| Former | 84% | about 16% |
| Unknown | 78% | about 22% |
| Current | 66% | about 34% |

- Clear ordering: **Never < Former < Current**.
- Current smokers have roughly **11 times the positive rate of never-smokers** (about 34% vs. about 3%) and about double that of former smokers.
- Former smokers retain elevated but reduced risk compared with current smokers.
- "Unknown" again sits near the population average.

### 3.4 Lung Cancer Rate by Air Pollution Exposure (approx.)

| Air pollution exposure | Approx. negative | Approx. positive |
|---|---|---|
| Very Low | 91% | about 9% |
| Low | 88% | about 12% |
| Medium | 84% | about 16% |
| Unknown | 78% | about 22% |
| High | 71% | about 29% |
| Very High | 60% | about **40%** |

- Smooth, monotonic increase across the ordered levels (Very Low to Very High).
- Very High exposure is about **4.4 times** the Very Low positive rate.
- The effect is real but **gentler than genetic risk or smoking status** (smaller spread between extremes).
- "Unknown" is placed between Medium and High purely by its near-average value, not because it is an ordered level.

### 3.5 Tobacco Load by Diagnosis

- **Positive: 32** vs. **Negative: 21** (average tobacco exposure, likely pack-years or packs).
- Positive patients carry about **52% more tobacco load** (a difference of 11 units).
- This agrees with the smoking status result: higher cumulative exposure goes with higher diagnosis rate.

### 3.6 Diagnosis Probability by Key Symptoms (approx.)

Values are the probability of a positive diagnosis given the symptom is present (Yes) or absent (No).

| Symptom | Probability if Yes | Probability if No | Approx. relative lift (Yes / No) |
|---|---|---|---|
| Chronic_lung_disease | about 0.56 | about 0.18 | about 3.1x |
| Chest_pain | about 0.40 | about 0.15 | about 2.7x |
| Shortness_of_breath | about 0.35 | about 0.14 | about 2.5x |

- **Chronic lung disease is the strongest symptom/condition signal**: more than half of patients with it are positive.
- All three symptoms raise positive probability well above the 21.65% baseline, and absence of any one keeps probability **below baseline (0.14-0.18)**.
- Ranking of predictive strength: Chronic lung disease > Chest pain > Shortness of breath.
- The three symptoms are shown separately, so their **combined or interaction effects are not visible** in this dashboard.

---

## 4. Risk Factor Ranking (Summary)

By approximate spread between lowest and highest positive rate within each factor:

| Rank | Factor | Lowest to highest positive rate | Spread |
|---|---|---|---|
| 1 | Genetic risk | about 12% (Low) to about 65% (High) | about 53 pts |
| 2 | Air pollution exposure | about 9% (Very Low) to about 40% (Very High) | about 31 pts |
| 3 | Smoking status | about 3% (Never) to about 34% (Current) | about 31 pts |
| 4 | Chronic lung disease (symptom) | about 18% (No) to about 56% (Yes) | about 38 pts |

Rankings are approximate and based on univariate views only. Genetic risk, chronic lung disease, current smoking, and very high pollution are the strongest individual markers.

**Factors showing NO effect in this dashboard:** gender (smoking prevalence and intensity identical), year (positive rate flat).

---

## 5. Cross-Cutting Insights

1. **Class imbalance:** about 21.65% positives. Any model trained on this data should use stratified splits and imbalance-aware metrics (recall, precision, PR-AUC), not accuracy alone.
2. **Stable data-generating process:** flat positive rate across 10 years and identical smoking metrics across genders point to a generator with fixed rules and no temporal drift or gender dependence.
3. **Dose-response structure:** genetic risk, smoking status, and pollution all show clean ordered gradients, showing the generator encodes additive risk logic.
4. **"Unknown" categories** behave like the population average (about 22% positive), which is the signature of randomly injected missing values rather than a distinct patient group.
5. **Population skew:** older (median 70), male-leaning (53%), and about 40% smokers.
6. **Volume growth is not a quality signal:** 6x more records over time with no change in positive rate.

---

## 6. Limitations and Caveats (important for answering questions)

- **Synthetic data:** Conclusions describe the generator's rules, not clinical reality. Do not present them as medical evidence.
- **Univariate views only:** each chart looks at one factor at a time, so confounding (for example smoking and chronic lung disease together) is not controlled. Association does not imply causation.
- **Approximate values:** percentages read from stacked bar charts and symptom probabilities are visual estimates.
- **Not shown on the dashboard:** breakdown by hospital branch, breakdown by month, diagnosis rate by gender, diagnosis rate by age group, and interactions between factors. The filters exist (Age, Year, Month, Hospital Branch, Diagnosis), but no filtered view is shown in these screenshots.
- **Axis truncation:** the positive rate line on the trend chart uses a narrow secondary axis (about 21.60%-21.70%) that exaggerates tiny differences.
- **Ambiguous labels:** "Average Cigarette packs" and "Tobacco Load" are assumed to be the same underlying tobacco exposure measure (consistent with the weighted-average check in 2.6), but their exact unit is not stated on the dashboard.

---

## 7. Quick-Lookup Facts (for retrieval)

- Total patients: **10,014,991**
- Median age: **70**
- Overall positive rate: **21.65%** (2.17M positive, 7.85M negative)
- Peak age group: **65-75** (about 3.55M)
- Gender split: Male 5.3M, Female 4.3M, Unknown 0.4M
- Smokers: Male 2.13M, Female 1.71M, Unknown 0.15M (about 40% prevalence in each)
- Average cigarette packs: **23** for all genders
- Tobacco load: Positive **32**, Negative **21**
- Highest-volume year: **2025 (1.80M)**; lowest: **2016 (0.30M)**
- Positive rate range across years: **21.58% (2021) to 21.70% (2018)**
- Highest-risk genetic group: **High (about 65% positive)**
- Highest-risk smoking group: **Current (about 34% positive)**; lowest: **Never (about 3%)**
- Highest-risk pollution group: **Very High (about 40% positive)**
- Strongest symptom: **Chronic lung disease (about 0.56 probability when present)**
- Hospital branches: **NE, SE, NW, SW**
- Filters: Age 1-100, Year 2016-2025, Month, Hospital Branch, Diagnosis

---

## 8. Sample Q&A (for grounding responses)

**Q: What percentage of patients are diagnosed positive?**
A: 21.65% (about 2.17M of 10.01M patients).

**Q: Does gender affect smoking in this data?**
A: No. Smoking prevalence is about 40% for every gender and average cigarette packs are 23 for all genders. Males simply have more smokers in absolute terms because they are a larger share of patients (5.3M vs. 4.3M).

**Q: Is lung cancer rate increasing over the years?**
A: No. Patient volume grew from 0.30M (2016) to 1.80M (2025), but the positive rate stayed between 21.58% and 21.70%, which is effectively flat.

**Q: Which risk factor is most strongly associated with a positive diagnosis?**
A: Genetic risk. High genetic risk patients are positive about 65% of the time versus about 12% for Low. Chronic lung disease (about 0.56 probability when present) and current smoking (about 34% positive) follow.

**Q: How does smoking status relate to diagnosis?**
A: Positive rate rises from about 3% (Never) to about 16% (Former) to about 34% (Current). Positive patients also have a higher tobacco load (32 vs. 21).

**Q: How does air pollution relate to diagnosis?**
A: Positive rate increases steadily with exposure, from about 9% at Very Low to about 40% at Very High.

**Q: What does the age distribution look like?**
A: Most patients are older adults. The distribution peaks at 65-75 years, has a median of 70, and has very few patients under 35.

**Q: Which symptom best signals a positive diagnosis?**
A: Chronic lung disease (about 0.56 vs. 0.18 when absent), then chest pain (about 0.40 vs. 0.15), then shortness of breath (about 0.35 vs. 0.14).

**Q: Can these results be applied to real patients?**
A: No. The dataset is synthetic and rule-generated, so results illustrate the dashboard's analytic workflow and the generator's built-in logic rather than real clinical findings.
