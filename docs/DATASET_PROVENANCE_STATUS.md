# Stage 2 — Dataset Provenance and Licensing Status

**Audit date:** 2026-08-15  
**Status:** `PARTIAL_BLOCKED`

This document records only provenance facts that have been verified from an original/official dataset source or the competition host. It does not assert a license where the source evidence reviewed by the project does not establish one.

## 1. UCI Bank Marketing

**Status:** `PROVENANCE_VERIFIED / LICENSE_VERIFIED / EXECUTION_NOT_STARTED`

- **Original provider/repository:** UCI Machine Learning Repository
- **Dataset name:** Bank Marketing
- **Creators:** S. Moro, P. Rita, P. Cortez
- **UCI dataset ID:** 222
- **DOI:** `10.24432/C5K306`
- **Task:** Classification — predict whether a client subscribes to a term deposit (`y`)
- **Legacy full dataset size:** 45,211 instances, 16 listed input features in the current UCI metadata for the legacy representation
- **Date-ordered extended release:** `bank-additional-full.csv` contains 41,188 examples and 20 inputs, ordered by date from May 2008 to November 2010
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0), as stated by UCI
- **Prediction-time integrity issue:** `duration` is known only after the marketing call completes and must be excluded from pre-contact deployment-style models
- **Raw-data status in this repository:** `NOT_PRESENT`
- **Execution status:** `NOT_EXECUTED`

### Required next actions

1. Download from the original UCI source (preferred over an unverified mirror).
2. Record access date, file names, byte sizes, SHA-256 hashes, and exact release used.
3. Generate the complete per-feature availability audit.
4. Confirm how the available ordering/time variables support rolling-origin evaluation; do not invent dates that are not present.

## 2. Home Credit — Credit Risk Model Stability

**Status:** `SOURCE_VERIFIED / ACCESS_RULES_REQUIRE_VALIDATION / EXECUTION_NOT_STARTED`

- **Host/provider:** Home Credit Group via Kaggle
- **Competition:** Home Credit — Credit Risk Model Stability
- **Scientific role:** Primary temporal/stability benchmark
- **Official competition framing:** model evaluation explicitly concerns stability/degradation over time
- **Configured target:** `target`
- **Configured entity key:** `case_id`
- **Configured time variable:** `WEEK_NUM`
- **Raw-data status in this repository:** `NOT_PRESENT`
- **License/redistribution status:** `REQUIRES_VALIDATION`
- **Competition rules/access:** `REQUIRES_VALIDATION` and may require account authentication/rule acceptance before local download
- **Execution status:** `NOT_EXECUTED`

### Required next actions

1. Authenticate through the data-access route authorized for the user.
2. Review/accept applicable competition rules before download where required.
3. Record the rule/version/access evidence and any redistribution restrictions.
4. Download locally only; do not commit competition raw data to GitHub.
5. Hash all files and construct a dataset card before modeling.

## 3. Porto Seguro — Safe Driver Prediction

**Status:** `SOURCE/TARGET_VERIFIED / ACCESS_RULES_REQUIRE_VALIDATION / EXECUTION_NOT_STARTED`

- **Host/provider:** Porto Seguro via Kaggle
- **Competition:** Porto Seguro’s Safe Driver Prediction
- **Task:** predict the probability that a driver will initiate an auto-insurance claim in the **next year**
- **Competition evaluation metric:** Normalized Gini Coefficient
- **Configured target:** `target`
- **Configured entity key:** `id`
- **Raw-data status in this repository:** `NOT_PRESENT`
- **License/redistribution status:** `REQUIRES_VALIDATION`
- **Execution status:** `NOT_EXECUTED`

### Horizon implication

The official task is explicitly a **next-year claim** target. Therefore, this dataset must **not** be rewritten as a 90-day claim horizon unless source timestamps permit exact reconstruction, which has not been established. It can remain in Part 2 as a task-native external-validation benchmark if the manuscript states the target horizon accurately.

### Required next actions

1. Validate Kaggle access/rules and redistribution constraints.
2. Download locally under the applicable terms.
3. Record file hashes, schema, row/feature counts, missingness conventions, class prevalence, and anonymized feature semantics.
4. Do not upload competition raw files to GitHub, Hugging Face, or a new Kaggle dataset unless the terms explicitly permit redistribution.

## 4. IEEE-CIS Fraud Detection

**Status:** `DISABLED / NOT_AUDITED_FOR_EXECUTION`

This remains an optional stress test only. It is not required to establish the main Part 2 contribution. It must not be enabled until the three primary datasets are stable and the additional compute/manuscript burden is justified.

## 5. Part 1 institutional 120,000-customer dataset

**Status:** `INSUFFICIENT_EVIDENCE_FOR_PART2_REUSE`

The Part 2 pre-results manuscript refers to the same de-identified 120,000-customer, 24-month environment used in Part 1. That dataset, its original authorization, raw timestamps, complete label-construction logic, and prediction-time feature lineage are not present in the current repository audit.

Therefore:

- the project must **not** claim that Part 2 executed on this institutional dataset;
- the common 90-day horizon must **not** be presented as executed for those four tasks;
- reuse is permitted only after current authorization, source data, timestamps, labels, and feature availability are independently revalidated.

If that evidence cannot be recovered, the final Part 2 paper should clearly present itself as a **reproducible public-benchmark extension inspired by Part 1**, not as a new empirical analysis of the unavailable institutional dataset.

## Stage 2 gate

| Dataset | Source provenance | License/rules | Raw files | Dataset card | Stage-2 state |
|---|---|---|---|---|---|
| UCI Bank Marketing | PASS | PASS (CC BY 4.0) | NOT_PRESENT | PENDING | PARTIAL |
| Home Credit Stability | PASS | REQUIRES_VALIDATION | NOT_PRESENT | PENDING | BLOCKED |
| Porto Seguro | PASS | REQUIRES_VALIDATION | NOT_PRESENT | PENDING | BLOCKED |
| IEEE-CIS | NOT_REQUIRED_YET | NOT_AUDITED | NOT_PRESENT | NOT_STARTED | DISABLED |
| Part 1 institutional data | Historical manuscript claim only | REQUIRES_REVALIDATION | NOT_PRESENT | NOT_AVAILABLE | BLOCKED |

**Stage 2 overall: FAIL/PARTIAL.**

The project must not proceed to a full prediction-time feature audit or empirical model execution for a dataset until its local raw files and data-use status are documented. Work may continue on code/tests/templates that do not require access to the missing data.
