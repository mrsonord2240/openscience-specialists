# Selection — crispr-screen-analyst (2026-09-16)

Scope per `CANDIDATES.md`: pooled knockout/CRISPRi/a screens, library design through
copy-number-aware hit calling (MAGeCK, BAGEL2, drugZ, JACKS) to essential/non-essential
benchmarking. Editing-outcome analysis only if it fits one workflow. Draw folders:
`crispr-screens`, `workflows/crispr-screen-pipeline`, `pathway-analysis`, `experimental-design`.

Chosen from `F:\OpenScience\audit-envs\crispr-screen-analyst\TOOLS.md`: choice is by coverage,
noting per Skill whether its central tool is installed/patched/blocked, not by convenience.

## Chosen Skills, audit order (core first)

| # | Skill ID | Role | Source folder | Central tool status (TOOLS.md) |
| --- | --- | --- | --- | --- |
| 1 | bio-crispr-screens-library-design | core — framing/design | crispr-screens/library-design | CRISPOR not installed (genome-scale indices, GB-scale); Skill's own runnable example uses a self-contained GC-content heuristic instead, so its floor is still reachable |
| 2 | bio-crispr-screens-screen-qc | core — QC/validation, pre-hit-calling | crispr-screens/screen-qc | MAGeCK-VISPR blocked (Linux/Mac-only dashboard); covered by installed `mageck count/test` + the Skill's own pandas/matplotlib `screen_qc.py` |
| 3 | bio-crispr-screens-mageck-analysis | core — central operation (hit calling) | crispr-screens/mageck-analysis | MAGeCK installed (built from source, patched for Windows), verified against real HAP1 TKOv3 data |
| 4 | bio-crispr-screens-bagel-essentiality | core — central operation (hit calling) | crispr-screens/bagel-essentiality | BAGEL2 installed (patched for numpy 2.x), verified against real HAP1 TKOv3 data, concordant with MAGeCK |
| 5 | bio-crispr-screens-drugz-chemogenomic | core — central operation (hit calling) | crispr-screens/drugz-chemogenomic | drugZ installed (patched for a silent pandas CoW data-loss bug), verified against real HAP1 TKOv3 data |
| 6 | bio-crispr-screens-jacks-analysis | core — central operation (hit calling) | crispr-screens/jacks-analysis | JACKS installed (patched, scipy→numpy alias break), verified on JACKS' own bundled Project Score dataset |
| 7 | bio-crispr-screens-copy-number-correction | supporting — copy-number-aware hit calling (**re-marked from core, Sam 2026-09-16**: after two fix passes and three audits it holds at 82, deployable, no open P0/P1, but capped under the 85 core floor. The central operation is carried by hit-calling (90) with MAGeCK/BAGEL2/drugZ/JACKS; CN correction is an adjunct. Raising it to core level is tabled, not abandoned.) | crispr-screens/copy-number-correction | CRISPRcleanR (its named primary tool) failed to install (VariantAnnotation pthread link failure, time-boxed); Chronos, the Skill's own cited DepMap-standard alternative, is installed and verified — floor reachability depends on which path the audit exercises |
| 8 | bio-crispr-screens-hit-calling | core — cross-method reconciliation | crispr-screens/hit-calling | No standalone tool; decision-tree/reconciliation logic over the four hit-calling Skills above, all of which are runnable here |
| 9 | bio-workflows-crispr-screen-pipeline | core — end-to-end orchestration | workflows/crispr-screen-pipeline | tool_type mixed, primary_tool MAGeCK (installed); depends_on the Skills above, all reachable except the CRISPRcleanR branch |
| 10 | bio-crispr-screens-batch-correction | supporting — multi-batch/multi-cohort screens | crispr-screens/batch-correction | R side (sva, RUVSeq, EDASeq) installed; pyComBat (its stated primary_tool) not separately verified in TOOLS.md — flag for the audit |
| 11 | bio-experimental-design-batch-design | supporting — design framing (reused) | experimental-design/batch-design | Re-audited post-fix 2026-09-16: **87, Production Ready**, deployable (was 82, Limited Release) |
| 12 | bio-pathway-go-enrichment | supporting — hit-list interpretation (reused) | pathway-analysis/go-enrichment | Re-audited post-fix 2026-09-16: **90, Production Ready**, deployable (unchanged score) |
| 13 | bio-pathway-gsea | supporting — hit-list interpretation (reused) | pathway-analysis/gsea | Re-audited post-fix 2026-09-16: **97, Production Ready**, deployable (was 90, Limited Release; the Limited Release cap was an assertion-rate downgrade the fixes cleared) |
| 14 | bio-crispr-screens-crispresso-editing | core — editing-outcome quantification (added 2026-09-16, Sam: editing is in scope) | crispr-screens/crispresso-editing | CRISPResso2 2.3.4 via Docker `pinellolab/crispresso2`; CRISPResso/Pooled/Batch/Compare verified against upstream test expectations |
| 15 | bio-crispr-screens-base-editing-analysis | supporting — base-editing outcomes (added 2026-09-16) | crispr-screens/base-editing-analysis | CRISPResso2 via Docker; BE-Hive in its own venv (patched for pandas 2.x) |
| 16 | bio-crispr-screens-prime-editing-screens | supporting — prime-editing design and outcomes (added 2026-09-16) | crispr-screens/prime-editing-screens | PRIDICT2 in its own uv venv on Python 3.10, CPU; README example verified |

Gene-level screen hits are gene lists, so both pathway-analysis reuses apply directly (unlike
metabolomics). `bio-experimental-design-multiple-testing` (82, not deployable) and
`bio-experimental-design-sample-size` (67, Reject, veto) are excluded per the brief.

## Skills read but not chosen

- `bio-crispr-screens-combinatorial-screens` — paralog/multiplex design guidance with no installable
  central tool (enCas12a is a guide-design concept, not a CLI); niche relative to core pooled-screen scope.
- `bio-crispr-screens-in-vivo-screens` — animal-model design guidance only, nothing here to execute
  against; niche relative to core pooled-screen scope.
- `bio-crispr-screens-perturb-seq-analysis` — single-cell CRISPR screens (Perturb-seq); despite a fully
  working tool stack (pertpy/scanpy/anndata installed), this sits on the `single-cell-transcriptomics-analyst`
  candidate's side of the line, not this candidate's pooled-screen scope.
- `experimental-design/power-analysis`, `experimental-design/randomization-blocking` — unaudited;
  skipped for breadth control given the two other experimental-design Skills already scored from this
  folder (multiple-testing, sample-size) both had quality problems, and batch-design already covers the
  design-framing role needed here.
- `pathway-analysis/kegg-pathways`, `reactome-pathways`, `wikipathways`, `enrichment-visualization` —
  unaudited; go-enrichment + gsea already give validation/interpretation coverage for gene-level hits,
  so the extra pathway-analysis Skills were left out for breadth control.
