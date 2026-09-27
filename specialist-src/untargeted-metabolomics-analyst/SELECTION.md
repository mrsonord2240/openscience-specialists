# `untargeted-metabolomics-analyst` — Skill selection (2026-09-16)

Scope (`CANDIDATES.md`): LC-MS untargeted metabolomics and lipidomics — XCMS/MS-DIAL
preprocessing, QC-based drift correction and normalization, annotation with MSI confidence
levels, statistics, pathway mapping. Targeted analysis and isotope tracing only as supporting.
Draw-from folders: `metabolomics`, `workflows/metabolomics-pipeline`, `pathway-analysis`,
`experimental-design`.

## Chosen Skills, audit order (core first)

| # | Skill ID | Role | Source folder | Tooling (from TOOLS.md) |
| --- | --- | --- | --- | --- |
| 1 | `bio-metabolomics-xcms-preprocessing` | core — entry, feature extraction | `metabolomics/xcms-preprocessing` | xcms installed, real: 1125 peaks from 2 faahKO CDFs |
| 2 | `bio-metabolomics-normalization-qc` | core — QC/drift correction/normalization | `metabolomics/normalization-qc` | pmp installed, real: QC-RSC end-to-end on MTBLS79 |
| 3 | `bio-metabolomics-metabolite-annotation` | core — annotation, MSI confidence levels | `metabolomics/metabolite-annotation` | matchms installed (import OK); SIRIUS login-gated, MetFrag jar installed and runs (usage error, not silent) as the free substitute |
| 4 | `bio-metabolomics-statistical-analysis` | core — statistics | `metabolomics/statistical-analysis` | ropls, scikit-learn, statsmodels installed |
| 5 | `bio-metabolomics-pathway-mapping` | core — pathway mapping, terminal step | `metabolomics/pathway-mapping` | MetaboAnalystR installed (GitHub build); FELLA/KEGGREST need live KEGG REST at runtime |
| 6 | `bio-metabolomics-msdial-preprocessing` | supporting — alternate preprocessing route (DIA/GC-MS) | `metabolomics/msdial-preprocessing` | MSDIALCUI.exe installed, real usage banner + `lcms --help` flags confirmed |
| 7 | `bio-metabolomics-lipidomics` | supporting — lipidomics branch | `metabolomics/lipidomics` | lipidr, pygoslin installed |
| 8 | `bio-workflows-metabolomics-pipeline` | supporting — orchestration | `workflows/metabolomics-pipeline` | depends only on Skills above, already tooled |
| 9 | `bio-experimental-design-batch-design` | supporting — framing/design | `experimental-design/batch-design` | reused; since re-audited post-fix 2026-09-16 (87, Production Ready) |

Five core Skills cover the full central pipeline end to end (entry → QC/normalization →
annotation → statistics → pathway), so gates 3 and 4 do not depend on any supporting Skill.
`msdial-preprocessing` and `lipidomics` are marked supporting, not core: the Specialist's
identity is the untargeted LC-MS route (xcms is the named `primary_tool` for the domain and is
the only preprocessing path already run end-to-end on real data), and both branch off it rather
than being load-bearing for it.

## Reused report

- `bio-experimental-design-batch-design` — **87, Production Ready, deployable, no veto** (fork
  `mrsonord2240/bioSkills@6847328:experimental-design/batch-design`; re-audited after the round-2
  fix pass on 2026-09-16, superseding the 82/Limited Release figure this row used to carry from
  `575ab946...`). Applies unchanged:
  balancing batch/plate/run-order against biology is the same problem for LC-MS injection
  sequences as for sequencing lanes.

## Read but not chosen

- `bio-metabolomics-isotope-tracing` — CANDIDATES.md scopes tracing as supporting-only; a
  separate SIRM/fluxomics branch (pool vs. flux) not needed to reach core coverage.
- `bio-metabolomics-targeted-analysis` — supporting-only per scope; a closed-panel MRM/PRM
  quantitation workflow, not the untargeted discovery pipeline this Specialist routes.
- `bio-pathway-gsea`, `bio-pathway-go-enrichment`, `bio-pathway-kegg-pathways`,
  `bio-pathway-reactome`, `bio-pathway-wikipathways`, `bio-pathway-enrichment-visualization` —
  all six operate on gene lists/ranked gene vectors (Entrez/ENSEMBL/SYMBOL), not metabolite or
  KEGG-compound IDs; `pathway-mapping`'s own SKILL.md cites go-enrichment/gsea only as a
  conceptual cross-reference for gene-set methods, not an interchangeable tool. Metabolomics'
  own `pathway-mapping` (MetaboAnalystR ORA/MSEA/mummichog, FELLA network diffusion) already
  covers this candidate's pathway step natively; bolting on a gene-centric tool would need an
  out-of-scope multi-omics translation layer. `gsea` and `go-enrichment` reports exist (both 90,
  Production Ready) but are not relevant here.
- `bio-experimental-design-sample-size` (67, Reject, veto fired) and
  `bio-experimental-design-multiple-testing` (82, not deployable) — excluded per brief, as in
  earlier specs.
- `bio-experimental-design-power-analysis` — negative-binomial count-model power (RNA-seq/ATAC/
  ChIP/methylation/proteomics depth-vs-replicate tradeoff), not continuous LC-MS intensity data.
- `bio-experimental-design-randomization-blocking` — generic design principles; redundant with
  `batch-design`'s more specific batch/confounding coverage for this workflow, and no existing
  report to reuse.

## SIRIUS note

`metabolite-annotation`'s SKILL.md names SIRIUS/CSI:FingerID as one of three annotation routes.
SIRIUS 6 requires a free account login since v5 (no anonymous CLI) — per TOOLS.md this is
blocked, not installable headlessly. MetFragCommandLine (in-silico fragmentation, no library
spectrum needed) and matchms (library-spectrum matching) are installed and cover the Skill's
other two routes; the audit should note SIRIUS as untestable-but-documented rather than treat its
absence as a Skill defect.
