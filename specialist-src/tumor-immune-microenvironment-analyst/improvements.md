# Improvements — Tumor Immune Microenvironment Bulk-Transcriptome Specialist (2026-09-10)

## Test coverage lost by fixture exclusion

- `ssgsea-immune-infiltration-analysis` and `gsva-analysis-and-visualization` ship without their 25.5 MB `tests/data` matrices, which are over the 10 MiB per-file limit. Their `tests/run_tests.R` cannot run in the installed package. Upstream should ship a small fixture that is 10 MiB or less, such as a gene-subset of the same GSE44076 matrix, so the in-package smoke test works again. The packaged ssGSEA default gene-set table (`tests/data/immune_gene_sets.csv`, 28 cell types) is still shipped, and the prompt routes cell-type ssGSEA to it.
- That table carries upstream label typos ("Effector memeory", "Immature  B cell"). Reports should quote the labels verbatim, and upstream should fix them.

## Missing workflow steps

- Single-cell-reference deconvolution (CIBERSORTx-, BayesPrism- or MuSiC-type), which would allow tumor/stroma-aware and absolute estimates. There is no Skill for this in `F:\OpenScience\skills`, so it needs a new Skill. `scientific/Data Analysis/scrna-cell-type-annotator` (unaudited) could supply the reference-building step.
- Alternative deconvolution (xCell, MCP-counter, EPIC, quanTIseq) and CIBERSORT absolute mode. No Skill exists, yet both planners name these methods and the prompt currently marks them `route_required`.
- Immunotherapy-response context (TIDE, IPS, TMB, checkpoint scoring). No execution Skill exists. `medical/Protocol Design/treatment-response-predictor-planner` (90, two P1s) could be added as a planning-only Skill for designs with response-labelled cohorts.
- Count handling. Nothing bundled converts raw counts to TPM/CPM, so count-only cohorts are blocked for deconvolution. `differential-expression-analysis` (90; DESeq2/edgeR; already published in auto-research-specialist, so gate 9 would reuse its bytes) would cover count-model DE between subtypes.
- Covariate-adjusted survival. `km-survival-curve` (added, 92) only draws curves. `univariate-multivariable-cox-regression` (86, one P1) would add purity-, stage- and age-adjusted hazard ratios for immune subtypes.
- Concordance tables. `sample-correlation-analysis` (86; P1: creates output dirs on failed validation) would compute method-vs-method and gene-vs-immune correlations as executed steps instead of ad hoc calculations. `pca-dimensionality-reduction` (93, published) would add PCA QC outside ComBat runs.
- External subtype validation: no centroid or nearest-template classifier, and no pan-cancer immune-subtype (C1–C6-style) assignment Skill.

## Bundled-Skill audit issues that matter here

- `tumor-immune-infiltration-diagnostic-ml-research-planner` P1: no minimum-agreement threshold for consensus feature selection. P2: the choice of immune-estimation algorithm is not compared.
- `consensus-clustering-analysis` P1: the first-run dependency setup is undocumented. Unflagged issue: it takes the minimum PAC over 11 distance/algorithm pairs and does not report cluster sizes. The prompt compensates with a second-gene-selection gate.
- `pcd-immune-oncology-research-planner` P1: the source of the cell-death gene set is not standardized.
- `estimate-immune-score-analysis` P2: no input-normalization guidance, and group p-values are unadjusted. The prompt gates both.
- `cibersort-immune-infiltration-analysis`: the uniform 1/22 fallback for all-zero fits is documented only in `references/algorithm.md`, and the SKILL.md mentions `tests/test_skill.R`, which is not shipped.
- `gokegg-analysis`:
  - It uses `use_internal_data = TRUE`, so KEGG needs locally installed KEGG data.
  - It sets no gene universe, so the background is the whole genome, which inflates enrichment for immune-selected lists.

## Scope changes made in this build

- Removed `conventional-oncology-hub-gene-research-planner`. Its core workflow (DEG → survival → PPI hub genes) is generic oncology biomarker discovery, and keeping it would blur gate 5.
- Added `km-survival-curve` (92) to link subtypes to survival.
- Renamed Skill ID `gokegg` to `gokegg-analysis`, its upstream frontmatter `name`, so `SKILL.md` ships unmodified.
- Shared IDs `gene-protein-expression-matrix-normalization` and `batch-effect-correction` are handled by THRESHOLD gate 9: the builder packages the published auto-research-specialist@1.0.1 bytes (digest-verified), so installing both Specialists raises no Skill conflict. The upstream and published bytes differ only in Markdown table padding and CRLF, which I checked with a diff.

## System prompt

- At 21,995 characters the prompt is at the 22k cap. Any added gate needs an equal cut. The next candidates to cut are the Troubleshooting entries that repeat gates.
- `sample-correlation-analysis` is not bundled, so triangulation (method-vs-method and marker concordance) is an ad hoc calculation on output tables. It is not an executed Skill step.

## Connectors

- It is unclear whether any declared Connector reaches TCGA/GDC expression plus clinical data. Confirm what `clinical-genomics` resolves to and add it if it does.
- `cancer-models` has little value here because cell lines have no TME. Consider leaving it off by default.

## Evaluation this Specialist still needs

- An end-to-end run on a public tumor cohort that has orthogonal ground truth (IHC, flow or matched scRNA), scoring the agreement between deconvolution and the measurement.
- Refusal and gate probes:
  - raw-count input: expect `route_required`
  - array plus RNA-seq ComBat merge: expect stop
  - TumorPurity requested for RNA-seq: expect refusal
  - subtype "validated" on its own clustering genes: expect a descriptive label
  - immunotherapy response prediction without a treated cohort: expect refusal
  - ssGSEA scores pooled across separately scored cohorts: expect refusal
- A routing check that planner output is never reported as executed and that `zscore`/`minmax` matrices never reach a scorer.
