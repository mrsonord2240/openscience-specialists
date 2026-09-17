# Untargeted Metabolomics Analyst

Takes untargeted LC-MS metabolomics from raw mzML to biological interpretation: xcms 4.x feature extraction, QC-based drift correction and normalization (pmp), confidence-stratified metabolite annotation (matchms/MetFrag) with MSI/Schymanski levels, permutation-validated statistics (PCA/OPLS-DA/univariate), and background-aware pathway mapping (MetaboAnalystR/FELLA). Batch/plate design and an alternate MS-DIAL/lipidomics route are included as supporting Skills. Research use only.

## Versions

- `1.0.0` - initial release with 9 bundled Skills and 3 Connector references.

The package uses the OpenScience App export/import v1 layout. Connector entries are references only;
credentials and executable Connector configuration are not included.

## Bundled Skills

Scores come from skill-auditor runs made for this release on 2026-09-16; the upstream
repository ships no audits. Where the generated code could not run here, the output was
graded by inspection; the table says how many test inputs actually ran.

| Skill                                    | Display name                                        | Role       | Audit score                                                     |
| ---------------------------------------- | --------------------------------------------------- | ---------- | --------------------------------------------------------------- |
| `bio-metabolomics-xcms-preprocessing`    | XCMS Untargeted LC-MS Feature Extraction            | core       | 92 (Production Ready, 2026-09-16; code ran for 2/9 test inputs) |
| `bio-metabolomics-normalization-qc`      | Metabolomics QC, Drift Correction and Normalization | core       | 92 (Production Ready, 2026-09-16; code ran for 0/9 test inputs) |
| `bio-metabolomics-metabolite-annotation` | Metabolite Annotation and MSI Confidence Levels     | core       | 95 (Production Ready, 2026-09-16; code ran for 0/7 test inputs) |
| `bio-metabolomics-statistical-analysis`  | Metabolomics Statistical Analysis                   | core       | 96 (Production Ready, 2026-09-16; code ran for 0/9 test inputs) |
| `bio-metabolomics-pathway-mapping`       | Metabolite Pathway Mapping                          | core       | 92 (Production Ready, 2026-09-16; code ran for 0/7 test inputs) |
| `bio-metabolomics-msdial-preprocessing`  | MS-DIAL Preprocessing (DIA/GC-MS Route)             | supporting | 91 (Limited Release, 2026-09-16; code ran for 6/7 test inputs)  |
| `bio-metabolomics-lipidomics`            | Lipidomics Analysis                                 | supporting | 92 (Production Ready, 2026-09-16; code ran for 0/9 test inputs) |
| `bio-workflows-metabolomics-pipeline`    | Untargeted Metabolomics Pipeline Orchestration      | supporting | 92 (Production Ready, 2026-09-16; code ran for 0/9 test inputs) |
| `bio-experimental-design-batch-design`   | Batch and Confounding Design                        | supporting | 87 (Production Ready, 2026-09-16; code ran for 7/7 test inputs) |

## Connector references

`pubmed`, `chemistry`, `omics-archives`

## Source

Skills from [https://github.com/mrsonord2240/optimizing-agent-science-skills](https://github.com/mrsonord2240/optimizing-agent-science-skills) at `f5ad8c583206a9124732d9518ace53ab17a9be3b`, under `skills/bioSkills/` (MIT).

These Skills originate in https://github.com/GPTomics/bioSkills at commit d91ed3d563019e649dc854c56ccd62551359488a (MIT).
They have been MODIFIED: defects found by audit were fixed in https://github.com/mrsonord2240/bioSkills-Improved at commit 9d31109159d4d490ec375d4ae88c9b77570f3840, then exported to the repository named above. Files change only where an audit
demonstrated a defect; every change has a fix log and a post-fix audit report.

Packaging notes (Skill files are otherwise byte-identical to that commit; audit reports are not
packaged):

- 29 text file(s) normalized to repository format: LF line endings, no trailing whitespace, no blank lines at end of file
