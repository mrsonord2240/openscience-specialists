# OpenScience Specialists

Research Specialists for the OpenScience App by Samuel Nord, published as a signed Protocol v1
marketplace.

## Add this marketplace in OpenScience

In the App: Marketplace → Add GitHub source →
`https://github.com/mrsonord2240/openscience-specialists/tree/published`. On the review screen,
confirm the marketplace name is `OpenScience Specialists (Samuel Nord)`, the key ID is
`openscience-samuelnord-2026-09`, and the fingerprint is `1e615f87f702b9ce5343ac6107e6b602e6f72d8828c8937539964b09d4e24345`. Do not add the source if any of
these differ.

## Specialists

| ID                                      | What it does                                                                                                                                                                                                                                                                            | Upstream skills                                                                                                                           |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `clinical-prediction-model-specialist`  | Plans, develops, and validates diagnostic and prognostic clinical prediction models with leakage-safe selection, sample-size and optimism checks, calibration, decision curves, and TRIPOD-aligned reporting for research, without issuing individual patient risk predictions.         | [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26)@f5ef65b |
| `clinical-trial-protocol-designer`      | Designs estimand-anchored, registry-informed clinical trial protocols—endpoints, eligibility, sample size, randomization, interim rules, and reporting checks—for research and regulatory planning without giving individual treatment advice or implying ethics approval.              | [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26)@f5ef65b |
| `critical-appraisal-specialist`         | Appraises individual biomedical papers or small paper sets for journal club, peer review and citation decisions, routing by verified study design to risk-of-bias, claim, spin and registry checks without reconstructing papers from memory.                                           | [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26)@f5ef65b |
| `manuscript-revision-specialist`        | Runs pre-submission QA, reporting-guideline, consistency and reference checks, anonymization, revision triage, and location-mapped reviewer responses for biomedical manuscripts without claiming experiments, analyses, or edits the authors have not supplied.                        | [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26)@f5ef65b |
| `mendelian-randomization-specialist`    | Designs assumption-audited Mendelian randomization, pleiotropy-sensitivity, and QTL colocalization studies from GWAS summary statistics, with instrument, ancestry, overlap, and harmonization gates and supporting MR execution, without claiming proven causality or clinical advice. | [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26)@f5ef65b |
| `pharmacovigilance-signal-designer`     | Designs deduplicated, MedDRA-versioned FAERS disproportionality, single-drug safety-atlas, and active-comparator signal studies with reporting-bias controls, without inventing reporting ratios, case counts, case facts, or causal claims.                                            | [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26)@f5ef65b |
| `preclinical-validation-designer`       | Designs claim-locked cell and animal validation routes from computational or association findings, with defined experimental units, randomization, blinding, controls, and escalation gates, without inventing models, effect sizes, or ethics approvals.                               | [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26)@f5ef65b |
| `real-world-evidence-epidemiologist`    | Designs and audits target-trial-aligned cohort, case-control, and survey studies on EHR, claims, registry, and NHANES-type data with explicit time zero, DAG-justified confounding control, and bias sensitivity analyses, without drawing individual patient conclusions.              | [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26)@f5ef65b |
| `research-grant-proposal-specialist`    | Frames testable aims, drafts agency-aligned proposal sections, and stress-tests them with structured mock review, verifying the current funding notice and never inventing preliminary data, citations, budgets, or reviewer scores.                                                    | [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26)@f5ef65b |
| `tumor-immune-microenvironment-analyst` | Estimates, triangulates and interprets tumor immune microenvironment composition from bulk transcriptomes via CIBERSORT-style deconvolution, ssGSEA, ESTIMATE and consensus subtyping, without treating scores as measured infiltration or making patient-level claims.                 | [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26)@f5ef65b |

More Specialists are added as they pass audit.

## How Skills are validated

Every bundled Skill is graded with AIPOCH's `skill-auditor` method (shipped in
[aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills)). A Specialist
is published only if its Skills also clear this marketplace's own bar, described at the end.

### 1. Two hard vetoes (any fail rejects the Skill)

- **Structural veto**, before scoring: a failure rate above 20%, missing or broken frontmatter,
  results that vary randomly on identical input, or executing raw user input.
- **Research veto**, after the test runs: invented citations or data (M1); diagnosing, prescribing
  or triaging an individual (M2); a fundamental methodological error (M3); generated code that
  cannot run (M4).

### 2. Static score (/100) — reading the Skill

25 criteria scored 0–4, in eight groups:

| Group                                              | Points |
| -------------------------------------------------- | -----: |
| Functional suitability                             |     12 |
| Reliability                                        |     12 |
| Performance and context cost                       |      8 |
| Agent usability                                    |     16 |
| Human usability                                    |      8 |
| Security                                           |     12 |
| Maintainability                                    |     12 |
| Agent-specific (trigger precision, composability…) |     20 |

### 3. Execution score (/100) — using the Skill

- The auditor writes 3, 5 or 7 realistic requests, scaled to the Skill's complexity: a canonical
  case, variants, an edge case, a stress case, a scope-boundary case and an ambiguous one.
- It completes each request by following the Skill and runs the code it produces, recording
  whether each input actually executed.
- Each output is scored on a general rubric (/40: correctness, clarity, efficiency, scope and
  safety) plus a category rubric (/60). For data-analysis Skills that is methodological validity
  20, code executability 15, data quality control 10, reproducibility 10, security 5.
- Each output also gets 3–5 true/false assertions, for example "the collapse step actually
  collapses low-support nodes".

### 4. Final score and grade

**Final score = static × 0.4 + execution average × 0.6**

| Score  | Grade            |
| ------ | ---------------- |
| 85–100 | Production Ready |
| 75–84  | Limited Release  |
| 60–74  | Beta Only        |
| < 60   | Reject           |

Floors lower the grade by one tier regardless of the number. Production Ready needs an execution
average of at least 85 and at least 90% of assertions passing; Limited Release needs 75 and 80%.
A Skill can therefore score 84 and still be graded Beta Only.

### 5. This marketplace's bar

- Every bundled Skill has an audit report with no veto, no open P0 recommendation, `deployable`
  true and a final score of at least 75.
- Every **core** Skill — one the Specialist's central workflow depends on — scores at least 85,
  and each Specialist has at least three, covering design, the central operation, and validation
  or reporting.
- Every file a Skill references is present, and Skill files are byte-identical to the source
  commit recorded in the release.
- Specialists are research-only and never make individual patient-level calls.

### Audit records

Every audit is published in
[mrsonord2240/optimizing-agent-science-skills](https://github.com/mrsonord2240/optimizing-agent-science-skills)
— including Skills that failed, earlier versions that were later fixed, and Specialist candidates
that were not viable — with each Skill's author, source commit and license, and a
[backlog](https://github.com/mrsonord2240/optimizing-agent-science-skills/blob/main/audits/BACKLOG.md)
of open improvements. That repository is where Skills are audited, fixed and re-audited before they
are bundled here.

### How to read the numbers

Most sub-scores are an auditor's judgment, so a difference of a point or two is noise. The stronger
evidence is what actually ran: a command that failed, a tree that matched the simulated truth, a
count that came out wrong. The Specialists listed above were assembled from the audit reports
shipped with their upstream Skills (only the reports with genuine per-Skill test cases were
counted). Specialists added from now on are audited here, with the generated code executed
wherever the tools run.

## Licensing

Repository tooling is Apache-2.0 (see [NOTICE](NOTICE)). Each Specialist's Skills keep their
upstream license, recorded in its `release.config.json`.

## Protocol

See [protocol/README.md](protocol/README.md) for the discovery and release protocol. Publication
is GitHub-only: GitHub Releases plus the `published` branch.
