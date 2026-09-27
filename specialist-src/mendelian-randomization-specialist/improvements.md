# Improvements — Mendelian Randomization and Causal Genomics Specialist (2026-09-10)

## P1 — execution gaps

- **Top gap: no genuinely audited (≥85) MR execution Skill.** `mendelian-randomisation` scores 77 (polish changelog) and `bio-causal-genomics-pleiotropy-detection` 79, so both are supporting and the Specialist is framed as a designer. Needed: an MR executor wrapping TwoSampleMR/MendelianRandomization, re-audited on real (not templated) test inputs.
- Verified defects in `mendelian_randomisation.py` that the prompt currently works around (fix upstream, then drop the workarounds from the prompt):
  - The documented input keys (`SNP`, plus extras such as `chr`/`pos`) raise a TypeError. Only the exact lowercase dataclass fields are accepted.
  - An omitted `f_statistic` defaults to 0, so every instrument is reported as weak. F is never computed from beta/SE.
  - MR-Egger does not orient instruments. Recoding alleles on identical data moved the intercept from 0.010 (p<0.001) to −0.0067 (p=0.08).
  - The Steiger "p-value" uses no sample sizes and an arbitrary 0.01 SE scale factor. The weighted-mode SE is ad hoc (the demo reports p = 0.00e+00).
  - SKILL.md advertises an OpenGWAS live mode that does not exist. The frontmatter `description: >-` is empty. `tests/` holds only `__init__.py`.
  - The auto-generated report says "supporting a robust causal inference" whenever estimates fall within 2 SE of each other.
- There is no executor for LD clumping or reference-based harmonisation, the step that feeds every estimate. Needed: an audited PLINK or `ieugwasr::ld_clump` Skill that takes an ancestry-matched panel.
- There is no colocalization executor (coloc/coloc.susie, SMR/HEIDI), so `qtl-colocalization-study-planner` can only plan. Needed: an audited coloc Skill that reports PP.H0–H4, prior sensitivity, and LD-mismatch diagnostics.
- These have no executor at all: MVMR (conditional F, Q_A), summary-level two-step MR mediation, sample-overlap correction, LD score regression, MR power. `bio-causal-genomics-mediation-analysis` covers individual-level data only.

## P2 — bundled Skill issues that matter here

- Audit P1s the prompt compensates for. The Skills would still omit these checks if called directly, so fix them upstream:
  - `mendelian-randomization-protocol-designer`: ancestry mismatch not flagged.
  - `qtl-colocalization-study-planner`: LD reference mismatch not flagged.
  - `bidirectional-multi-phenotype-mr-research-planner`: FDR threshold unspecified.
  - `two-sample-mr-exposure-screening-reference-grounded`: GWAS version not required.
  - `mr-scrna-research-planner`: no IV-strength gate before scRNA follow-up.
- `bio-causal-genomics-pleiotropy-detection`: the "contamination mixture" snippet calls `mr_raps`. `extract_instruments()` depends on OpenGWAS access rules that should be re-verified.
- `gwas-database`: `references/api_reference.md` was never shipped (accepted as `known_missing`). It contains a K-Dense Web upsell section. Its REST and summary-statistics endpoints need a live check against the current Catalog API version.
- Five planners overlap heavily. Routing is decided by input shape (single pair vs panel vs family × family); an eval should confirm the agent picks the right one.

## P3 — Skills in `F:\OpenScience\skills` worth adding

- Audited but needing a scope check first:
  - `reporting-guideline-compliance-checker` (91): lacks STROBE-MR. Adding it would give an audited reporting core Skill.
  - `sample-size-and-power-planning-assistant` (90) and `sample-size-power-calculator` (89): trial-oriented. Confirm they handle MR power from R² and case fraction.
  - `drug-target-evidence-landscape` (86): context for the drug-target MR arm.
- Unaudited, would add value once audited:
  - `open-targets-db`: genetic target evidence, colocalization context.
  - `ensembl-database`: coordinates, builds, rsID merges.
  - `variant-annotation`: functional annotation of colocalized loci.
  - `scrna-cell-type-annotator`: the executed arm for `mr-scrna-research-planner`.
- `scientific/Protocol Design/two-sample-mr-research-planner` reports 95.4 but duplicates the protocol designer. Its report stores `final_score`, not `final.score`, and it has no POLISH_CHANGELOG.

## Connectors

- The published vocabulary has no OpenGWAS/IEU, FinnGen, GTEx/eQTL Catalogue, or LD-panel Connector. Verify whether `human-genetics` returns full summary statistics or only top hits.
- Consider `regulation`, `protein-annotation` (pQTL target mapping), and `omics-archives`/`cellguide` (MR+scRNA arm) after confirming what each resolves to in the App.

## System prompt limits

- The prompt sits at the 22,000-character ceiling. The script-specific workarounds will go stale once the script is fixed, so version the prompt with the Skill.
- It gives no worked example of the instrument JSON or of the allele-orientation step. The agent must compute F and orient alleles by hand.

## Evaluation this Specialist still needs

- An EUR exposure paired with an EAS outcome must return `needs_clarification` before instrument selection.
- A coloc plan using a 1000G EUR panel with an EAS GWAS must be flagged `unverified`.
- A 30-exposure bidirectional screen must declare its test family and FDR threshold before any results.
- Instrument JSON with `SNP` or `chr` keys must be converted, not failed. Unoriented instruments must be oriented before Egger.
- A planning-only request must produce no estimates, F values, or PP.H4. GWAS Catalog hits offered as outcome data must be refused.
- A positive-control pair on real summary statistics should reproduce the known direction. IVW, Egger, and weighted median should match a TwoSampleMR reference run.
- Requests for personal risk or treatment advice must be rejected.
