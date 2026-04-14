# Answers to hospital_analytics_questions.sql

---

## OBJECTIVE 1: ENCOUNTERS OVERVIEW

### a. How many total encounters occurred each year?

| Year | Encounters |
|------|------------|
| 2011 | 1,336 |
| 2012 | 2,106 |
| 2013 | 2,495 |
| 2014 | 3,885 |
| 2015 | 2,469 |
| 2016 | 2,451 |
| 2017 | 2,360 |
| 2018 | 2,292 |
| 2019 | 2,228 |
| 2020 | 2,519 |
| 2021 | 3,530 |
| 2022 | 220 |

**Total: 27,891 encounters (2011-2022)**

### b. Percentage of encounters by class per year

| Class | Count | Percentage |
|-------|-------|------------|
| Ambulatory | 12,537 | 44.95% |
| Outpatient | 6,300 | 22.59% |
| Urgentcare | 3,666 | 13.14% |
| Emergency | 2,322 | 8.33% |
| Wellness | 1,931 | 6.92% |
| Inpatient | 1,135 | 4.07% |

### c. Percentage of encounters over 24 hours vs under 24 hours

- Under 24 hours: 27,816 (99.73%)
- Over 24 hours: 75 (0.27%)
- Median Duration: 0.25 hours
- Average Duration: 7.27 hours

**Average duration by class:**
| Class | Avg Duration |
|-------|--------------|
| Inpatient | 36.84 hours |
| Ambulatory | 9.48 hours |
| Outpatient | 5.88 hours |
| Emergency | 1.54 hours |
| Urgentcare | 0.25 hours |
| Wellness | 0.25 hours |

---

## OBJECTIVE 2: COST & COVERAGE INSIGHTS

### a. Zero payer coverage encounters

- **Encounters with zero coverage: 13,586**
- **Percentage: 48.71%**

**Zero coverage by payer:**

| Payer | Count |
|-------|-------|
| NO_INSURANCE | 8,807 |
| Humana | 1,038 |
| Aetna | 898 |
| UnitedHealthcare | 820 |
| Cigna Health | 790 |
| Anthem | 704 |
| Blue Cross Blue Shield | 336 |
| Dual Eligible | 127 |
| Medicare | 61 |
| Medicaid | 5 |

### b. Top 10 most frequent procedures with average base cost

| Procedure | Count | Avg Base Cost |
|-----------|-------|---------------|
| Assessment of health and social care needs (procedure) | 4,596 | $431.00 |
| Hospice care (regime/therapy) | 4,098 | $431.00 |
| Depression screening (procedure) | 3,614 | $431.00 |
| Depression screening using Patient Health Questionnaire Two-Item score (procedure) | 3,614 | $431.00 |
| Assessment of substance use (procedure) | 2,906 | $431.00 |
| Renal dialysis (procedure) | 2,746 | $1,004.09 |
| Assessment using Morse Fall Scale (procedure) | 2,422 | $431.00 |
| Assessment of anxiety (procedure) | 2,288 | $431.00 |
| Medication Reconciliation (procedure) | 2,284 | $509.12 |
| Screening for drug abuse (procedure) | 1,484 | $431.00 |

### c. Top 10 procedures by highest average cost

| Procedure | Avg Cost | Frequency |
|-----------|----------|-----------|
| Admit to ICU (procedure) | $206,260.40 | 5 |
| Coronary artery bypass grafting | $47,085.89 | 9 |
| Lumpectomy of breast (procedure) | $29,353.00 | 5 |
| Hemodialysis (procedure) | $29,299.56 | 27 |
| Insertion of biventricular implantable cardioverter defibrillator | $27,201.00 | 4 |
| Electrical cardioversion | $25,903.11 | 1,383 |
| Partial resection of colon | $25,229.29 | 7 |
| Fine needle aspiration biopsy of lung (procedure) | $23,141.00 | 1 |
| Percutaneous mechanical thrombectomy of portal vein using fluoroscopic guidance | $20,228.04 | 57 |
| Percutaneous coronary intervention | $19,728.00 | 9 |

### d. Average total claim cost by payer

| Payer | Avg Total Claim Cost | Total Cost | Encounters |
|-------|----------------------|------------|------------|
| Medicaid | $6,205.22 | $8,954,131.02 | 1,443 |
| NO_INSURANCE | $5,593.20 | $49,259,290.16 | 8,807 |
| Anthem | $4,236.81 | $2,982,715.05 | 704 |
| Humana | $3,269.30 | $3,543,921.36 | 1,084 |
| Blue Cross Blue Shield | $3,245.58 | $3,002,166.01 | 925 |
| Cigna Health | $2,996.95 | $2,424,532.96 | 809 |
| UnitedHealthcare | $2,848.34 | $2,563,507.98 | 900 |
| Aetna | $2,767.05 | $2,589,956.10 | 936 |
| Medicare | $2,167.55 | $24,647,228.89 | 11,371 |
| Dual Eligible | $1,696.19 | $1,546,925.99 | 912 |

**Overall Average: $3,639.68 per encounter**

---

## OBJECTIVE 3: PATIENT BEHAVIOR ANALYSIS

### a. Unique patients admitted each quarter

- Total unique patients (2011-2022): 974
- Average new patients per quarter: 247.3

**Unique patients per year:**

| Year | Unique Patients |
|------|-----------------|
| 2011 | 410 |
| 2012 | 559 |
| 2013 | 570 |
| 2014 | 630 |
| 2015 | 553 |
| 2016 | 552 |
| 2017 | 546 |
| 2018 | 535 |
| 2019 | 514 |
| 2020 | 519 |
| 2021 | 649 |
| 2022 | 103 |

### b. Readmissions within 30 days

- Total readmissions: 16,786 encounters
- **Readmission rate: 60.18%**
- Definition: Patient returns within 30 days of previous encounter

**Readmissions by encounter class:**

| Class | Count |
|-------|-------|
| Ambulatory | 7,951 |
| Outpatient | 3,613 |
| Urgentcare | 2,752 |
| Emergency | 1,526 |
| Inpatient | 535 |
| Wellness | 409 |

### c. Patients with most readmissions

**Top 10 patients with most readmissions:**

| Rank | Patient ID | Readmissions |
|------|------------|--------------|
| 1 | 1712d26d-822d-1e3a-2... | 1,375 |
| 2 | 3de74169-7f67-9304-9... | 871 |
| 3 | 5e055638-0dad-dfd5-0... | 871 |
| 4 | 3f523789-55f3-bb31-2... | 440 |
| 5 | 5dcb295d-92df-a147-e... | 421 |
| 6 | 442dc617-c7f2-0513-1... | 382 |
| 7 | b4ab9ab3-f52a-751e-a... | 375 |
| 8 | 9b8ae606-5059-b3a6-1... | 346 |
| 9 | b4671e80-7e87-9260-c... | 289 |
| 10 | ff331e5c-ab16-e218-f... | 279 |

**Characteristics of top readmitting patients:**
- Total encounters for these patients: 5,759
- Average encounters per patient: 575.9

**Insurance distribution of top readmitters:**
- NO_INSURANCE: 63.2%
- Medicare: 34.6%
- Dual Eligible: 2.2%

---

## Key Dashboard Metrics

| Metric | Value |
|--------|-------|
| Total Encounters | 27,891 |
| Unique Patients | 974 |
| Avg Cost/Visit | $3,639.68 |
| Total Claim Cost | $101,514,375.52 |
| Total Payer Coverage | $31,097,506.99 |
| Coverage Rate | 30.63% |
| Readmission Rate | 60.18% |
| Total Procedures | 47,701 |
| Avg Duration | 7.27 hours |

---

**Key Findings Summary:**

1. **Encounter Volume**: Steady growth from 2011-2014, stable 2015-2020, peak in 2021, significant drop in 2022 (partial year data)

2. **Coverage Gap**: 48.71% of encounters have zero payer coverage, with NO_INSURANCE being the largest group (8,807 encounters)

3. **Readmission Crisis**: 60.18% readmission rate is extremely high - indicates potential issues with:
   - Discharge planning
   - Follow-up care coordination
   - Chronic disease management

4. **Cost Insights**: 
   - Medicaid patients have highest avg cost ($6,205.22)
   - NO_INSURANCE patients surprisingly have high avg cost ($5,593.20) - indicating uncompensated care burden
   - Medicare has highest total cost ($24.6M) due to volume

5. **Procedure Patterns**:
   - Most frequent procedures are assessments/screenings ($431 avg)
   - Highest cost procedures are ICU admissions and cardiac surgeries ($206K, $47K)
