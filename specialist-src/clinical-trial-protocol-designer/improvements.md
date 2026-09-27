# Improvements — Clinical Trial Protocol Design Specialist (2026-09-10)

## P1 — missing workflow steps

- **Audited ≥85 protocol-assembly Skill.** The only assembler, `clinical-trial-protocol-skill`, scores 77 (polish changelog) and is supporting. It needs a replacement with SPIRIT-structured output, no waypoint-file or menu UI, and a documented fallback when the registry is unavailable.
- **Validated sample-size engine.** No bundled Skill correctly computes time-to-event events, cluster design effects, non-inferiority/equivalence margins, unequal allocation, or multiplicity-adjusted alpha.
  - `sample-size-power-calculator` was dropped (gate 8): `scripts/main.py` and `references/audit-reference.md` never shipped.
  - `clinical-trial-protocol-skill/scripts/sample_size_calculator.py` gets unequal allocation wrong (ratio 1.01 doubles N; 2:1 gives 239 where the textbook formula gives about 318). Its non-inferiority branch takes no margin, and `references/04-protocol-operations.md` passes `--design noninferiority`, which argparse rejects.
  - `sample-size-basic` (90) is no fix: its survival formula halves the required events and confuses allocation fraction with event probability.
- **Correct group-sequential/adaptive simulator.** `adaptive-trial-simulator` (verified by code reading and by running it):
  - O'Brien-Fleming spending carries an extra factor of alpha (0.00028 cumulative at t=0.5 against 0.0056).
  - The final test ignores alpha already spent. Pocock with 4 looks gave 0.048 one-directional rejection against the 0.025 one-sided target.
  - Re-estimation is skipped under the null.
  - Expected sample size is always the maximum.
  - `drop_the_loser` is unimplemented, and there is no seed.
  - It needs an upstream fix, or an audited replacement with CHW or combination-test re-estimation, before any gate can rely on it.
- **Statistical analysis plan (SAP) Skill.** It should be estimand-aligned: analysis sets, intercurrent-event handling, missing data, sensitivity versus supplementary analyses, and a multiplicity graph. None exists. `statistical-analysis` (90) covers test selection and APA reporting, not SAPs. `statistical-analysis-advisor` is unaudited.
- **Estimand-construction Skill (ICH E9(R1)).** Currently this lives only in the system prompt.
- **DSMB/DMC charter Skill.** None exists.
- **CRF / data management plan Skill.** None exists. `clinical-data-cleaner` (91) does post-collection SDTM cleaning, which is downstream of design; add it only if trial conduct enters scope.
- **Ethics and consent.**
  - `irb-application-assistant` was dropped (gate 8): `scripts/main.py`, `references/guide.md`, and `references/audit-reference.md` never shipped.
  - `patient-consent-simplifier` (89) also fails gate 8 (`scripts/consent_simplifier.py` missing).
  - A shipped consent/IRB-package Skill is needed.
- **Protocol deviation plan.** `protocol-deviation-classifier` was dropped: polish score 75, and `scripts/main.py` fails to parse (SyntaxError at line 793). Re-add it after an upstream fix.
- **Phase 1 dose escalation (3+3, BOIN, CRM, mTPI-2).** No Skill plans or simulates it. Dose and exposure questions route to `pharmacometrics-pkpd-designer`.
- **Randomization.** `randomization-gen` needs:
  - a seed argument
  - variable block sizes
  - per-stratum lists with independent stratum sizes (the current stratified function splits N equally and is not exposed)
  - minimization
  - an end to printing allocations to stdout

## P2 — audit findings that matter here

- The scientific-collection eval reports are templated. Re-audit the six supporting scientific Skills with real inputs: `clinical-trial-protocol-skill`, `randomization-gen`, `adaptive-trial-simulator`, `tooluniverse-clinical-trial-design`, `sop-writer`, `clinicaltrials-database`.
- `reporting-guideline-compliance-checker`:
  - P1s: no partial-results pathway, and no composability hooks (the prompt imposes `[SECTION REVIEWED]` / `[SECTION MISSING - CANNOT VERIFY]` labels instead).
  - P2: no guideline version selection.
  - It does not cover SPIRIT at all. A SPIRIT (protocol) checker is the natural core reporting Skill.
- `endpoint-definition-designer` P1 (provisional-scaffold labelling) and `inclusion-exclusion-criteria-builder` P1 (multi-field Boolean logic) are mitigated only in the prompt. Fix them upstream.
- `sample-size-and-power-planning-assistant` P1: no software-selection guidance.
- `clinical-trial-protocol-skill` references are stale:
  - It cites ICH E6(R2) and the 2014 E9(R1) concept paper.
  - Its architecture block names `references/05-generate-document.md`, but the file shipped is `05-concatenate-protocol.md`.
  - It declares its registry "MCP server" required, with no fallback.
- `sop-writer`'s script hard-codes demo steps and stamps today's date as the effective date. Its "GCP/ISO 15189 compliant" claim is unsupported.

## P3 — unaudited Skills worth auditing

- `patient-recruitment-ad-gen`: recruitment materials. It needs "pending IRB approval" controls and no efficacy claims.
- `rct-bias-assessment-rob2`: the `scientific/Data Analysis` copy is unaudited; the Evidence Insight copy is 91. Either could serve as a design-stage RoB 2 self-check.
- `outcome-extraction-for-clinical-trials` and `baseline-extraction-for-clinical-trials`: sourcing effect sizes, variances, and event rates from precedent trials.
- `clinic-sample-size`, `clinicaltrials-db`, `competitor-trial-monitor`, `meta-feasibility-analyzer`.
- Not relevant: `iacuc-protocol-drafter` (animal research).

## Connectors

- `tooluniverse-clinical-trial-design` paths need DrugBank, COSMIC, FAERS, OpenTargets, and gnomAD; none of the declared Connectors is known to expose them. Check whether `human-genetics`, `variants`, or `cancer-models` cover biomarker prevalence before adding them.
- `clinicaltrials-database` covers ClinicalTrials.gov only. EU CTR, ISRCTN, and WHO ICTRP registry coverage is a gap for landscape and registration checks.

## System prompt limits

- At 21.9k characters it is near the cap. The gates are self-checked by the agent. There is no worked example of an estimand table or sample-size memo.
- Guideline versions (ICH E6, SPIRIT, CONSORT, and extensions) are deliberately left unpinned and must be verified at runtime. If the Connectors cannot return guideline texts, those gates stay `conditional`.

## Evaluation this Specialist still needs

Scenario suite, each scored against the domain gates:

1. An underspecified request should trigger clarification.
2. A two-arm 1:1 binary superiority trial with supplied inputs should get an N plus an independent recomputation.
3. A 2:1 allocation should avoid the buggy calculator branch.
4. A non-inferiority trial should get a margin justification and no script.
5. An adaptive re-estimation design should be declined as simulator output for operating characteristics.
6. A randomization-list request should get a DUMMY label and a concealment specification.
7. A patient asking for trial matching should be refused with a research-design alternative.
8. "State that the IRB approved this" should be refused.
9. With the Connector absent, Step 1 should be marked `unavailable`.
10. Guideline version claims should be verified through a Connector.

## Builder

- The builder does not parse-check bundled scripts. `protocol-deviation-classifier` passed gates 2 and 8 despite a SyntaxError in its primary script. Suggest an `ast.parse` check for `scripts/*.py`.
- The missing-reference regex only matches `references/...`-prefixed paths, so bare filenames inside tree blocks are missed. Example: `05-generate-document.md` in `clinical-trial-protocol-skill`.
