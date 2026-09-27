# Improvements — Real-World Evidence and Observational Epidemiology Specialist (2026-09-10)

## Missing workflow steps (no packaged Skill executes them)

- **General regression execution (logistic, conditional logistic, Poisson/negative binomial, linear, mixed-effects, GEE).** Lost when `tooluniverse-statistical-modeling` was dropped under gate 8: its SKILL.md routes to six unshipped `references/*.md` (cox_regression, logistic_regression, ordinal_logistic, linear_models, bixbench_patterns, troubleshooting). It needed no ToolUniverse service. The consequence: case-control ORs, NHANES cross-sectional logistic models and rate ratios are now `planning_only` or `unpackaged_computation`. Fix: get upstream to ship the six references (then re-add as core), or audit a replacement. `statistical-analysis` cannot stand in: that ID is already published from K-Dense, so gate 9 blocks it.
- **Propensity score estimation, matching, IPTW/overlap weights, SMD balance diagnostics.** No Skill in `F:\OpenScience\skills`. Partial coverage: `confounder-and-bias-control-planner` (chooses the strategy), `real-world-evidence-study-designer` (analysis line), `epidemiology` (one-line mention). Highest-value new Skill for this Specialist.
- **E-value and quantitative bias analysis.** No Skill. The prompt carries the RR E-value formula; `confounder-and-bias-control-planner` plans negative controls. A small scripted E-value/QBA Skill (with OR/HR conversions) would close this.
- **DAG construction and adjustment-set derivation.** No Skill. `epidemiology` gives a DAG checklist (it names DAGitty); `confounder-and-bias-control-planner` does role classification without drawing a diagram.
- **Competing risks (Aalen-Johansen cumulative incidence, Fine-Gray).** `scikit-survival` covers cumulative incidence under competing risks, but its audit file is `scikit-survival_audit_result_v1.json` (score 86), not `eval_report_*`, so the builder treats it as unaudited. Rename or re-export the report, then verify gate 8.
- **Multiple imputation.** No Skill. `clinical-data-cleaner` does single mean/median/mode imputation only. `knn-imputation` (95) targets expression matrices and doesn't fit here.
- **Survey-weighted (design-based) estimation for NHANES.** No Skill. `nhanes-clinical-retrospective-biomarker-research-planner` plans `survey::svyglm` but nothing runs it.
- **Time-varying exposure, marginal structural models, clone-censor-weight, RMST, and PH testing.** No Skill. `univariate-multivariable-cox-regression` has no PH test, weights, strata, or time-varying covariates.
- **Claims/EHR phenotype and code-list construction (ICD, NDC, ATC, OMOP concept sets).** No Skill and no Connector.

## Bundled-Skill audit P1s and defects that matter here

- `nhanes-clinical-retrospective-biomarker-research-planner` P1: survey weights not always mandated. The prompt's survey gate overrides it, but fixing the Skill is better.
- `univariate-multivariable-cox-regression` P1: silent fall-back to all features when fewer than 3 pass univariate screening. For causal work the prompt forces `--skip_univariate true`. Upstream should warn, and should add a `cox.zph` PH check, `weights=`, and `cluster()`.
- `case-control-study-planner` P1s: Section L gives no alternative when fit is poor, and the description is too short to trigger reliably.
- `confounder-and-bias-control-planner` P1: no clarification gate when the variable list is missing. Handled in the prompt.
- `reporting-guideline-compliance-checker` P1: no pathway for partial material. Its references cover STROBE but not RECORD/RECORD-PE or target-trial-emulation reporting items; adding those would remove a Connector dependency.
- `real-world-evidence-study-designer` P1: no database-suitability guidance (claims vs EHR vs registry). Partly covered in the prompt's framing section.
- `clinical-data-cleaner` (script, observed): every run imputes (default median; no "none" option); `standardize_dates` coerces any column whose name contains "DT" and silently blanks unparseable dates; `cap` clips every numeric column, including time and event columns; `fillna(method='ffill')` is deprecated in pandas 2.x. Upstream should add `--missing-strategy none` and date-loss reporting.
- `table-1-generator-advanced` (script, observed): SKILL.md promises a missingness appendix and normality-based choice of summary statistic. Neither is implemented. There are no SMDs and no weights, and numeric variables with 5 or fewer values become categorical. It is byte-identical to `table-1-generator`. An SMD column plus a `--weights` option would make it fit for RWE.
- `km-survival-curve`: `--auto_convert_days` defaults to true (a max-time > 365 heuristic). The prompt forces false unless the unit is known.

## Candidate Skills already in `F:\OpenScience\skills`

- `scikit-survival` (competing risks; audit file misnamed, see above).
- `survival-curve-risk-table` (audit in `*_audit_result_v2.json`, score 88; needs a standard report and a gate 8 check).
- `statistical-analysis-advisor` (audit in `*_audit_result_v2.json`; test selection).
- `cohort-study-quality-assessment-nos` and `Case-control-study-quality-assessment-nos`: appraise published cohorts and case-control studies for evidence review. The polish changelog puts cohort-NOS at 77 (supporting only).
- Excluded under gate 8: `survival-analysis-km` and `sample-size-power-calculator` both reference a `scripts/main.py` that was never shipped.

## System-prompt limits

- At 21.9k characters it is near the 22k cap, so there's no room for worked examples (for example a filled target-trial table or an immortal-time case).
- The OR→RR and HR→RR conversions for E-values are deferred to cited sources rather than stated.
- The SMD threshold, grace period, and washout lengths are deliberately left unfixed. The agent must elicit them, which may slow simple requests.
- Core execution is thin: every EXEC Skill is supporting. Estimation beyond complete-case Cox and KM depends on `unpackaged_computation`.

## Connector gaps

- No terminology/code-system Connector (ICD-10-CM, NDC, RxNorm, ATC, OMOP vocabularies).
- No survey data-access Connector (NHANES files and weights). `research-resources` only covers documentation.
- No Connector for reporting-guideline repositories. RECORD, RECORD-PE, and target-trial-emulation guideline versions have to come through `literature`.

## Evaluation this Specialist still needs

- Adversarial prompts, each scored on mode choice, gate firing, and no fabricated numbers:
  - an immortal-time trap ("users = at least 2 fills in the first year after diagnosis")
  - a prevalent-user request
  - a non-user comparator
  - adjusting for a mediator
  - an elderly outcome where death competes
  - NHANES analysis without weights
  - Cox run with the default screening
  - a patient-specific risk question (expect `reject`)
  - a RECORD version claim with no Connector available
- An execution smoke test in the target runtime: `Rscript` with `survival`, `openxlsx`, `readxl`, `forestplot`, and `optparse` for Cox, plus `survminer`, `data.table`, and `ggplot2` for KM; Python with `pandas` and `scipy` for Table 1 and the cleaner.
- An end-to-end run on a public synthetic claims-like dataset, checking that PLAN outputs are never reported as executed results.
