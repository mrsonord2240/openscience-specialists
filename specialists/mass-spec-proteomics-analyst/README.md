# Mass-Spec Proteomics Analyst

Takes bottom-up proteomics from a search engine's output or raw DIA runs to differential protein abundance: imports MaxQuant, DIA-NN and mzML data and strips search-engine bookkeeping, runs DDA database search with target-decoy FDR and DIA-NN searches filtered at the right q-value level and context, resolves protein-group parsimony and protein-level FDR, normalises and rolls peptides up to protein quantities, tests for differential abundance with missingness modelled rather than imputed, localises and quantifies PTM sites, and carries instrument-, run- and quant-level QC through the whole chain. Research use only; no patient-level interpretation.

## Versions

- `1.0.0` - initial release with 11 bundled Skills and 4 Connector references.

The package uses the OpenScience App export/import v1 layout. Connector entries are references only;
credentials and executable Connector configuration are not included.

## Bundled Skills

Scores come from skill-auditor runs made for this release on 2026-09-15; the upstream
repository ships no audits. Where the generated code could not run here, the output was
graded by inspection; the table says how many test inputs actually ran.

| Skill                                   | Display name                             | Role       | Audit score                                                       |
| --------------------------------------- | ---------------------------------------- | ---------- | ----------------------------------------------------------------- |
| `bio-proteomics-data-import`            | MS Data Import and Bookkeeping Strip     | core       | 85.2 (Limited Release, 2026-09-15; code ran for 8/8 test inputs)  |
| `bio-proteomics-dia-analysis`           | DIA Search and q-Value Filtering         | core       | 86.2 (Limited Release, 2026-09-15; code ran for 7/7 test inputs)  |
| `bio-proteomics-peptide-identification` | Peptide Identification and PSM-Level FDR | core       | 90 (Production Ready, 2026-09-15; code ran for 10/10 test inputs) |
| `bio-proteomics-protein-inference`      | Protein Inference and Protein-Level FDR  | core       | 88.8 (Production Ready, 2026-09-15; code ran for 7/7 test inputs) |
| `bio-proteomics-quantification`         | Protein Quantification and Roll-Up       | core       | 89 (Production Ready, 2026-09-15; code ran for 10/11 test inputs) |
| `bio-proteomics-differential-abundance` | Differential Protein Abundance           | core       | 89 (Production Ready, 2026-09-15; code ran for 10/11 test inputs) |
| `bio-proteomics-proteomics-qc`          | Proteomics QC                            | core       | 88.1 (Production Ready, 2026-09-15; code ran for 8/8 test inputs) |
| `bio-proteomics-ptm-analysis`           | PTM and Phosphoproteomics Analysis       | supporting | 86.4 (Production Ready, 2026-09-15; code ran for 6/6 test inputs) |
| `bio-pathway-go-enrichment`             | GO Over-Representation Analysis          | supporting | 90 (Production Ready, 2026-09-15; code ran for 5/5 test inputs)   |
| `bio-experimental-design-batch-design`  | Batch and Confounding Design             | supporting | 82 (Limited Release, 2026-09-15; code ran for 5/5 test inputs)    |
| `bio-workflows-proteomics-pipeline`     | End-to-End Proteomics Workflow           | supporting | 87.7 (Production Ready, 2026-09-15; code ran for 7/8 test inputs) |

## Connector references

`pubmed`, `protein-annotation`, `omics-archives`, `genes`

## Source

Skills from [https://github.com/mrsonord2240/optimizing-agent-science-skills](https://github.com/mrsonord2240/optimizing-agent-science-skills) at `567cab000f3728427c4c8a18e36d2f794a9def7d`, under `skills/bioSkills/` (MIT).

These Skills originate in https://github.com/GPTomics/bioSkills at commit d91ed3d563019e649dc854c56ccd62551359488a (MIT).
They have been MODIFIED: defects found by audit were fixed in https://github.com/mrsonord2240/bioSkills at commit a62c7097f37cde2f1d44763ac22c3f5c6d5350bb, then exported to the repository named above. Files change only where an audit
demonstrated a defect; every change has a fix log and a post-fix audit report.

Packaging notes (Skill files are otherwise byte-identical to that commit; audit reports are not
packaged):

- 38 text file(s) normalized to repository format: LF line endings, no trailing whitespace, no blank lines at end of file
