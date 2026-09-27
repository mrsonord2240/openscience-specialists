# OpenScience Specialists — design report (2026-09-10)

Ten new Specialists built from the local AIPOCH skill library and validated against a clean clone of
`aipoch/openscience-specialist-marketplace`: `format:check`, `npm test` (28/28), `validate`
(20 versions), and byte-identical ZIPs on two builds each. Three more were designed but did not
make it; sixteen other directions are listed with what they would need.

- **Install these:** `F:\OpenScience\dist\<id>-1.0.0.zip`. They are checked against the App's own
  import rules by `preflight_app.mjs`. Don't zip the `specialists\` folders by hand: the App needs
  `manifest.json` at the ZIP root.
- Packages: `F:\OpenScience\specialists\<id>\` (marketplace layout, ready to copy into a fork)
- Authoring sources: `F:\openscience-specialists\specialist-src\<id>\` (`spec.json`, `system_prompt.md`,
  `improvements.md`)
- The bar: [`THRESHOLD.md`](THRESHOLD.md) · Builder: `build_specialist.py` · Check: `validate_all.sh`
- Not built: [`NEAR-MISSES.md`](NEAR-MISSES.md) · Upstream gaps: [`MISSING-FILES.md`](MISSING-FILES.md)

## What the skill library turned out to be

These change how far the audit scores can be trusted, so they come first.

1. **The `scientific` audit scores are inflated.** All 131 `eval_report` files there were
   overwritten by an upstream "polish" pass with a templated test section: inputs named
   "Test case N", generic assertions, and 104 reports with identical input totals. They claim
   86–92. The `POLISH_CHANGELOG.md` from the same pass records 75–79. The changelog number is
   used. The other 148 reports (all 141 `medical`, 7 unpolished
   `scientific`) are real and used as reported.
2. **The 183 `*_audit_result_v2.json` files are backfill, not audits.** Their "inputs" are
   sentences from the Skill's own description, their notes cite an "archived / legacy review",
   and every one scores 85 or more. They are not counted.
3. **157 referenced files were never shipped** (81 Skills, 80 of the files are scripts). They are
   missing upstream too: the Downloads archive is exactly commit `f5ef65b9`, and the F: copy is
   byte-identical to it. 46 of those Skills carry an audit score.
4. **Bundled scripts have real defects.** The authoring agents found these by running or reading
   the code. The three marked ✓ I confirmed independently.
   - ✓ `model-calibration-curve` reports 1 − Harrell's C: `concordance()` without
     `reverse = TRUE`. Its sibling `nomogram-construction` gets this right.
   - ✓ `meta-analysis` Egger test returns the slope's p-value and SE, not the intercept's.
   - ✓ `protocol-deviation-classifier/scripts/main.py` does not parse (line 793).
   - `mendelian-randomisation`: the documented input keys crash it; F defaults to 0; MR-Egger
     changes under allele recoding; its "Steiger" test uses no sample sizes.
   - `adaptive-trial-simulator`: Pocock early boundaries give about 0.048 type I error against a
     0.025 target.
   - `clinical-trial-protocol-skill`: its calculator gets unequal allocation wrong (239 vs about
     318 for 2:1).
   - `sample-size-basic`: undersizes small groups (7 where the exact t-test gives 9).
   - `xgboost-analysis`: early-stops on its own test split.
   - `decision-curve-analysis`: defaults to a case-control design with prevalence 0.3.
   - `randomization-gen`: has no seed option and prints the allocation.
   - `retraction-watcher`: counts failed lookups as "clear".
   - `rebuttal-letter-strategist` and `response-tone-polisher`: insert "We have revised…"
     whatever was done.
   - `adverse-event-narrative`: writes today's date as the report date.
   - `nsfc-grant-writer`: its guide says to "generate plausible preliminary work".
   - `systematic-review-screener`: its default CSV output crashes.
   - `rct-bias-assessment-rob2`: its D2 rule is inverted on 2.3.
5. **Shared Skill IDs would have broken installs.** The App refuses a Skill whose ID is already
   installed with different content. Ten Skills here also ship in `auto-research-specialist`, so
   they are packaged with the published bytes (digest-verified).

## Built

Every system prompt follows the structure of the nine published domain Specialists, with the
Open Science runtime contract verbatim and 21.9–22.0k characters. "Core" means the Skill passed
at 85 or more on a real audit.

| Specialist | Skills (core) | What it does |
| --- | --- | --- |
| `clinical-prediction-model-specialist` | 18 (9) | Diagnostic and prognostic models: leakage-safe selection, sample-size and optimism checks, calibration, decision curves, TRIPOD reporting |
| `tumor-immune-microenvironment-analyst` | 15 (6) | Bulk-transcriptome immune deconvolution (CIBERSORT, ssGSEA, ESTIMATE), triangulated, plus immune subtyping |
| `manuscript-revision-specialist` | 16 (5) | Pre-submission QA, reporting and reference checks, anonymisation, revision triage, location-mapped responses |
| `critical-appraisal-specialist` | 14 (4) | Single-paper appraisal routed by verified design: risk of bias, claim, spin, registry and retraction checks |
| `real-world-evidence-epidemiologist` | 12 (5) | Target-trial-aligned cohort, case-control and survey designs on EHR, claims, registry and NHANES data |
| `clinical-trial-protocol-designer` | 10 (4) | Estimand-anchored protocols: endpoints, eligibility, sample size, randomisation, interim rules |
| `mendelian-randomization-specialist` | 9 (3) | MR, pleiotropy-sensitivity and colocalisation study design with instrument, ancestry, overlap and harmonisation gates |
| `research-grant-proposal-specialist` | 8 (3) | Aims, agency-aligned sections and mock review, verified against the current funding notice |
| `preclinical-validation-designer` | 8 (3) | Cell and animal validation routes with experimental unit, randomisation, blinding and controls defined |
| `pharmacovigilance-signal-designer` | 4 (3) | FAERS disproportionality, single-drug and active-comparator signal study designs |

### How each could be improved

The full, prioritised list for each is in its `improvements.md`. The top items:

- **Clinical prediction models:**
  - No Skill does binary-outcome calibration or optimism-corrected AUC.
  - No Skill applies a frozen clinical model to an external cohort.
  - Fix the calibration C-index and the XGBoost early-stopping leak upstream.
- **Tumor immune microenvironment:**
  - Add single-cell-reference deconvolution and TIDE/TMB-type scoring.
  - Add count-model DE and Cox regression.
  - Upstream should ship ssGSEA/GSVA test data under 10 MiB (packaged here without it).
- **Manuscript revision:**
  - Response-letter writing has no core-grade Skill; `author-response-builder` is the best at 84.
  - Fix the boilerplate "We have revised…" insertion.
  - Add a reference-existence check for Word manuscripts.
- **Critical appraisal:**
  - Observational designs have no risk-of-bias tool: the NOS pair is broken upstream, and there is
    no ROBINS-I/E.
  - Upgrade RoB 2 to a real 85+ Skill.
  - Patch `retraction-watcher`.
- **Real-world evidence:**
  - Nothing runs a regression since `tooluniverse-statistical-modeling` failed (six references
    missing).
  - No propensity score/IPTW, E-value, multiple imputation, or survey weighting.
- **Clinical trials:**
  - No audited protocol-assembly Skill.
  - No validated sample-size or interim engine.
  - No SAP, DSMB-charter or consent/IRB Skills.
- **Mendelian randomization:**
  - Execution is supporting-grade (77) and defective.
  - No LD clumping or harmonisation against an ancestry-matched panel.
  - No colocalisation or SMR executor.
- **Grants:**
  - No 85+ full-proposal or mock-review Skill (the mock reviewer counts keywords).
  - No Connector returns funder rules.
- **Preclinical:**
  - No ARRIVE checker.
  - The IACUC, western-blot and FACS Skills have only backfilled audits.
  - Fix the `sample-size-basic` undersizing.
- **Pharmacovigilance:**
  - Design-only: nothing computes ROR/PRR/IC/EBGM or deduplicates FAERS.
  - Add a time-to-onset Skill.

## Not built

- **Systematic review & meta-analysis:** fully drafted, then failed gate 3. Every core Skill is
  from the inflated `scientific` set (76–78), and three were dropped for missing files. The prompt
  is kept as a draft for when re-audits land.
- **Computational pathology:** `pathology-roi-selector` is an empty template, `pathml` points at
  six missing references, and nothing trains a slide-level model.
- **Network toxicology:** blocked by the model's biology safety filter during authoring. Not
  retried.
- Sixteen more directions, with what each needs: [`NEAR-MISSES.md`](NEAR-MISSES.md).

## Decisions for Sam

- **Publisher** is set to `mrsonord2240` / Samuel Nord. The official `aipoch` ID is reserved for
  AIPOCH. `author` is omitted.
- **`manifest.json` says `exported_with_app_version: 0.19.0`,** like the published ones, but these
  were assembled, not exported. Importing one into the App and re-exporting it would prove the
  round trip.
- **Upstream:** `MISSING-FILES.md` and the defect list above are a ready issue list for
  `aipoch/medical-research-skills`.
