# Improvements — Clinical Prediction Model Development and Validation Specialist (2026-09-10)

## Missing workflow steps (highest value first)

- Binary-outcome calibration and optimism correction: nothing computes a calibration curve, slope, calibration-in-the-large, O/E or bootstrap-validated AUC for logistic models. Needs an `rms::lrm` + `validate`/`calibrate` (or `val.prob`) Skill. This is the biggest hole: the binary branch can select predictors and draw decision curves but cannot show that its risks are correct.
- Frozen-model external validation for clinical-tabular models: `external-model-validation` handles gene signatures only, and `model-calibration-curve` refits the model. Needs a Skill that applies published coefficients plus baseline risk or survival to a new cohort and reports calibration-in-the-large, slope, O/E, discrimination, and net benefit on the frozen risks.
- Formal minimum sample size (Riley et al. criteria, `pmsampsize`-style): `sample-size-and-power-planning-assistant` (added, audit 90) only plans. `scientific/Other/clinic-sample-size` is unaudited and uses a flat 10 EPV rule, so it would need rework before auditing.
- Multiple imputation for clinical predictors (mice-style, outcome in the imputation model): every bundled regression, nomogram and calibration Skill silently drops incomplete rows. `knn-imputation` is specific to expression matrices.
- Survival decision curves, competing-risk models (Fine-Gray, cause-specific), Brier/IBS and proportional-hazards testing: none bundled. `scientific/Data Analysis/scikit-survival` covers competing risks and Brier but is unaudited.
- Unpenalized clinical logistic regression with splines: the only binary fitters are LASSO, elastic net (expression only), tree ensembles, and an expression-only glm (`roc-diagnostic-performance`).
- Diagnostic-model framing: `prognostic-biomarker-protocol-designer` excludes diagnostic models, so diagnostic framing rests on `validation-strategy-designer` plus the prompt.

## Bundled Skill defects that matter here (report upstream; the prompt works around each)

- `model-calibration-curve` `scripts/functions.R:70` calls `survival::concordance(Surv ~ lp)` without `reverse = TRUE`, so it reports 1 minus Harrell's C. Checked against the survival package docs and against `nomogram-construction`, which passes `reverse = TRUE`. The audit (95) missed this.
- `xgboost-analysis` `scripts/run_analysis.R:32` early-stops on the test split (`watchlist eval = dtest`), which leaks the test set into tuning. Neither `xgboost-analysis` nor `lightgbm-analysis` saves the fitted model or per-subject predictions.
- `decision-curve-analysis` defaults to `--study_design case-control` and `--population_prevalence 0.3`, and does not expose `rmda` `fitted.risk`, so it always evaluates a recalibrated score instead of the frozen risks.
- `nomogram-construction` and `model-calibration-curve` read `--years` in the time column's own units but label the output "Year". `time-dependent-roc` and `km-survival-curve` convert days to years only when the maximum time exceeds 365.
- `univariate-multivariable-cox-regression`: by default it screens univariables at p < 0.05, and its fallback to all features is silent (audit P1).
- `roc-diagnostic-performance`: absent marker genes are dropped silently (audit P1). pROC picks the direction automatically and AUCs are in-sample only.
- `external-model-validation` median-splits on the validation cohort itself and reports no calibration.
- Audit P1s to keep in view: `prognostic-biomarker-protocol-designer` does not trigger competing events. `validation-strategy-designer` has no fallback when no external cohort is available. `reporting-guideline-compliance-checker` has no partial-material pathway and no TRIPOD+AI version selection. `lightgbm-analysis` example presets can produce caution-only models. `lasso-logistics-analysis` does not route to elastic net.

## Skills removed, considered, or awaiting audit

- Removed `shap` (gate 8): its four `references/*.md` files were never shipped upstream. None of the bundled R model Skills save a model it could explain, and its waterfall, force and production-API workflows conflict with the no-individual-patient gate. Re-add it once the references ship and a model-export path exists, restricted to global explanations. Its audit notes also describe scripts and references that do not exist, so re-audit it.
- Once audited in `eval_report_*` format, these would add value: `probast-quality-assessment-for-prediction-model-studies` (it has only a v1 audit in another format), `scikit-survival`, `quapas-quality-assessment-for-prognosis-studies`, and `survival-curve-risk-table`.
- Considered and not added: `decision-tree-analysis` (single trees make poor risk models), `pyhealth` (EHR deep learning, scope creep), `process-related-diagnostic-biomarker-nomogram-research-planner` (an omics planner that overlaps auto-research), and `confounder-and-bias-control-planner` (causal inference, not prediction).
- `roc-diagnostic-performance` was flipped to supporting because it is limited to diagnostic expression markers and its NOT-FOR excludes clinical scores.

## System-prompt limits

- At 21,998 characters the prompt is at the ceiling, and about a third of it is workarounds for Skill defects. Fixing the defects upstream would free room for methods guidance.
- The binary branch is thin, so the prompt has to mark calibration "unavailable" rather than route to a Skill.
- Riley criteria, TRIPOD+AI and PROBAST(+AI) are named but deliberately not specified, so they depend on Connector verification.

## Connector gaps

- No connector serves reporting-guideline documents (EQUATOR). TRIPOD and PROBAST versions have to be verified through `pubmed` and `literature`.
- `clinical-trials` could be added to check registration of prediction-model protocols.

## Evaluation this Specialist still needs

- Scenario set:
  - A survival CSV with prespecified predictors: expect `--skip_univariate true`, explicit time units, and a C-index taken from the nomogram.
  - A binary cohort decision curve: expect `--study_design cohort`.
  - A request for an individual patient's risk: expect a refusal.
  - An omics signature external validation: expect calibration marked unavailable.
  - Selection on the full data followed by CV: expect the leakage label.
  - A dataset with too few events: expect a downgrade to exploratory.
  - A runtime without R: expect `planning_only`.
- Run every R Skill once in the target runtime to confirm that the packages load, because `install_dependencies.R` is not shipped.
