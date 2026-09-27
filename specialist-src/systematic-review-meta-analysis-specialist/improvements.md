# Improvements — Systematic Review and Meta-analysis Specialist (2026-09-10)

## Blocking (see not-viable.md)

- Re-audit the seven core `scientific` Skills with real inputs. Their changelog scores are 76–78, but their templated reports claim 86–91.
- Ship the missing files for `meta-screening-fulltext`, `cohort-study-quality-assessment-nos`, and `case-control-study-quality-assessment-nos`, or replace those Skills.
- Clear the stale P0 on `biomedical-search-strategy-builder`. The fix is already in its code, but the builder's P0 check still trips.

## Upstream defects the prompt currently works around

- `systematic-review-screener`:
  - The CSV writer crashes, so the prompt forces `--format json`.
  - Substring hard exclusions are given confidence 1.0.
  - Records without an abstract are auto-excluded.
  - Its PRISMA JSON mislabels counts.
  - Fix: add word-boundary and negation handling, and route every exclusion to review.
- `meta-analysis`:
  - Egger's test uses the slope's p-value and SE.
  - Begg's test is not Begg–Mazumdar.
  - Only DerSimonian–Laird pooling is available.
  - There is no prediction interval, no REML/HKSJ option, and no zero-cell handling (MH, Peto).
  - The forest plot's null line is fixed at 0.
  - The code is inline only, with no `scripts/`.
- `rct-bias-assessment-rob2`: D3–D5 algorithms are missing, the D2 rule on question 2.3 is inverted, the overall judgement is simplified, and the output is per study rather than per result.
- `diagnostic-study-quality-assessment-quadas-2`: there are no domain or applicability judgements, comments are forced into Chinese, and `api_reference.md` is a placeholder.
- `meta-analysis-methods-generator`:
  - It hard-codes a PubMed API search, fixed reviewer counts, and a fixed-versus-random switch at I² < 50%.
  - It describes RoB 1 domains as RoB 2.
  - It asks for "random" text.
  - These are fabrication vectors. Rewrite it to consume the review log.
- `prospero-registration-helper`: the `{}` defaults read as facts, and the end date is hard-coded to today + 28 days.
- `meta-results-*`:
  - They ask for 300+ word descriptions of images, including I² and p-values.
  - Figure and table numbers are hard-coded.
  - The funnel plot writer's Table 3 caption is wrong.
  - `meta-results-sensitivity-analysis` imports `scripts/format_result.py`, which was never shipped.
  - Fix: require a numeric input table.
- `systematic-review`: its integration points (`literature-search`, `scienceclaw-ie`, `paper-writing`) are not bundled, so it is planning only.
- `biomedical-search-strategy-builder`: the SKILL.md bracket-check warning is stale. The script builds PubMed syntax only (audit P2).

## Missing workflow steps and candidate Skills

These candidates have no skill-auditor `eval_report`; most have only a legacy `*_audit_result_v*.json`.

- **Data extraction**: no Skill. Candidates are `outcome-extraction-for-clinical-trials` and `baseline-extraction-for-clinical-trials`.
- **Full-text screening**: none after the gate 8 drop. `meta-abstract-screener` (report 89) is also missing its `references/screening_prompts.md` and scripts.
- **Non-randomized risk of bias**: none. There is no ROBINS-I/E Skill. Unaudited `probast-quality-assessment-for-prediction-model-studies`, `quapas-quality-assessment-for-prognosis-studies`, and `quadas-c-assessment-for-diagnostic-accuracy-studies` would widen the review types covered.
- **Certainty of evidence (GRADE / Summary of Findings)**: no Skill anywhere in `F:\OpenScience\skills`.
- **Plot execution**: the only plotting is the inline code in `meta-analysis`.
  - Candidates: `meta-forest-binary-plot`, `meta-forest-continuous-plot`, `meta-forest-model-plot`, `meta-funnel-plot` (Egger/Begg), `meta-sensitivity-plot`, `meta-baujat-plot`, `meta-radial-plot`, and `meta-rob2-plot` (traffic light).
  - `forest-plot-styler` (report 89) names `scripts/main.py`, but that file was never shipped.
- **Framing and feasibility**: `meta-picos-generator`, `meta-criteria-generator`, `meta-feasibility-analyzer` (checks for existing meta-analyses and trials), and `INPLASY-registration-helper` as an alternative registry.
- **Search**: `meta-search-builder` and `pubmed-search-specialist` (unaudited) are near-duplicates of `biomedical-search-strategy-builder`. `multi-database-literature-collector` (medical, 87, published) would add real retrieval.
- **Writing**: `methods-section-writer` (medical, 92, published) could replace `meta-analysis-methods-generator`. `meta-manuscript-generator` (report 90) ships `search_references.py`; check its service dependency before bundling.
- **No Skill for**: diagnostic-accuracy pooling (bivariate/HSROC), network meta-analysis, or deduplication.

## System prompt limits

- The prompt is at the 22,000-character ceiling. Once upstream fixes land, the defect workarounds can be removed and replaced with GRADE and extraction guidance.
- Screening, extraction, and non-randomized appraisal are handled unassisted, marked `unassisted_reviewer_support` or `unassisted_draft`. The prompt cannot enforce dual independent review; it can only label decisions as provisional.
- Guideline versions (PRISMA 2020 and its extensions, RoB 2, QUADAS-2, GRADE, the PROSPERO form) must be verified at runtime. Nothing in the bundle is pinned to a version.

## Connector gaps

- Embase, CENTRAL, Web of Science, Scopus, and CINAHL have no Connector, so a full systematic search needs user exports.
- There is no PROSPERO or registry-of-reviews Connector for duplicate checks, and no Unpaywall or full-text retrieval Connector.
- `drug-regulatory` was added for regulatory review documents. Confirm that it exposes FDA and EMA review packages.

## Evaluation this Specialist still needs

- An end-to-end run on a small published Cochrane review with known answers:
  - PRISMA counts reconcile;
  - the pooled estimate matches the published one within rounding;
  - RoB 2 agrees per result.
- Adversarial cases:
  - a forest-plot image with no table (must refuse to read I² or estimates);
  - a methods request with no log (must use placeholders);
  - a screener run on records without abstracts;
  - a trial published in several reports (must deduplicate);
  - a user request to switch models on I² (must flag it).
- Confirm that the `meta-analysis` corrections (Egger intercept, prediction interval, log-scale null line) are actually applied when the code runs.
