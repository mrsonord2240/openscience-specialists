# OpenScience Specialists

Research Specialists for the OpenScience App by Samuel Nord, published as a signed Protocol v1
marketplace.

## Add this marketplace in OpenScience

In the App: Marketplace → Add GitHub source →
`https://github.com/mrsonord2240/openscience-specialists/tree/published`. On the review screen,
confirm the marketplace name is `OpenScience Specialists (Samuel Nord)`, the key ID is
`openscience-samuelnord-2026-09`, and the fingerprint is `3d0a93f80ac3f5361fdac9d3746f9a4f1168d4b38456f260c0dfc60fb6c032f1`. Do not add the source if any of
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

## Quality bar

Each Skill is chosen by an executed audit: core skills score at least 85, supporting skills at
least 75, with no veto and no open P0. Specialists are research-only and never make
individual patient-level calls.

## Licensing

Repository tooling is Apache-2.0 (see [NOTICE](NOTICE)). Each Specialist's Skills keep their
upstream license, recorded in its `release.config.json`.

## Protocol

See [protocol/README.md](protocol/README.md) for the discovery and release protocol. Publication
is GitHub-only: GitHub Releases plus the `published` branch.
