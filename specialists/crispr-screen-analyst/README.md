# CRISPR Screen Analyst

Analyzes pooled CRISPR knockout/CRISPRi/CRISPRa screens end to end: library design, screen QC, MAGeCK/BAGEL2/drugZ/JACKS hit calling, copy-number and batch correction, cross-method reconciliation, pipeline orchestration, pathway interpretation of hit lists, and CRISPResso2-based quantification of nuclease, base-editing, and prime-editing outcomes.

## Versions

- `1.0.0` - initial release with 16 bundled Skills and 5 Connector references.

The package uses the OpenScience App export/import v1 layout. Connector entries are references only;
credentials and executable Connector configuration are not included.

## Bundled Skills

Scores come from skill-auditor runs made for this release on 2026-09-16; the upstream
repository ships no audits. Where the generated code could not run here, the output was
graded by inspection; the table says how many test inputs actually ran.

| Skill                                       | Display name                   | Role       | Audit score                                                      |
| ------------------------------------------- | ------------------------------ | ---------- | ---------------------------------------------------------------- |
| `bio-crispr-screens-library-design`         | CRISPR Library Design          | core       | 91 (Production Ready, 2026-09-16; code ran for 8/8 test inputs)  |
| `bio-crispr-screens-screen-qc`              | CRISPR Screen QC               | core       | 94 (Production Ready, 2026-09-16; code ran for 0/9 test inputs)  |
| `bio-crispr-screens-mageck-analysis`        | MAGeCK Analysis                | core       | 88 (Limited Release, 2026-09-16; code ran for 0/9 test inputs)   |
| `bio-crispr-screens-bagel-essentiality`     | BAGEL2 Essentiality            | core       | 88 (Production Ready, 2026-09-16; code ran for 0/7 test inputs)  |
| `bio-crispr-screens-drugz-chemogenomic`     | drugZ Chemogenomic Screens     | core       | 90 (Production Ready, 2026-09-16; code ran for 0/7 test inputs)  |
| `bio-crispr-screens-jacks-analysis`         | JACKS Analysis                 | core       | 92 (Production Ready, 2026-09-16; code ran for 0/7 test inputs)  |
| `bio-crispr-screens-copy-number-correction` | CRISPR Copy-Number Correction  | supporting | 82 (Limited Release, 2026-09-16; code ran for 0/7 test inputs)   |
| `bio-crispr-screens-hit-calling`            | CRISPR Screen Hit Calling      | core       | 90 (Production Ready, 2026-09-16; code ran for 0/9 test inputs)  |
| `bio-workflows-crispr-screen-pipeline`      | CRISPR Screen Pipeline         | core       | 85 (Limited Release, 2026-09-16; code ran for 0/7 test inputs)   |
| `bio-crispr-screens-batch-correction`       | CRISPR Screen Batch Correction | supporting | 91 (Production Ready, 2026-09-16; code ran for 6/7 test inputs)  |
| `bio-experimental-design-batch-design`      | Batch Design                   | supporting | 87 (Production Ready, 2026-09-16; code ran for 7/7 test inputs)  |
| `bio-pathway-go-enrichment`                 | GO Enrichment                  | supporting | 90 (Production Ready, 2026-09-16; code ran for 7/7 test inputs)  |
| `bio-pathway-gsea`                          | Gene Set Enrichment Analysis   | supporting | 97 (Production Ready, 2026-09-16; code ran for 7/7 test inputs)  |
| `bio-crispr-screens-crispresso-editing`     | CRISPResso Editing Outcomes    | core       | 91 (Production Ready, 2026-09-16; code ran for 0/9 test inputs)  |
| `bio-crispr-screens-base-editing-analysis`  | Base-Editing Screen Analysis   | supporting | 92 (Production Ready, 2026-09-16; code ran for 9/9 test inputs)  |
| `bio-crispr-screens-prime-editing-screens`  | Prime-Editing Screens          | supporting | 81.2 (Limited Release, 2026-09-16; code ran for 8/9 test inputs) |

## Connector references

`pubmed`, `genes`, `genomes`, `variants`, `cancer-models`

## Source

Skills from [https://github.com/mrsonord2240/optimizing-agent-science-skills](https://github.com/mrsonord2240/optimizing-agent-science-skills) at `f5ad8c583206a9124732d9518ace53ab17a9be3b`, under `skills/bioSkills/` (MIT).

These Skills originate in https://github.com/GPTomics/bioSkills at commit d91ed3d563019e649dc854c56ccd62551359488a (MIT).
They have been MODIFIED: defects found by audit were fixed in https://github.com/mrsonord2240/bioSkills-Improved at commit 9d31109159d4d490ec375d4ae88c9b77570f3840, then exported to the repository named above. Files change only where an audit
demonstrated a defect; every change has a fix log and a post-fix audit report.

Packaging notes (Skill files are otherwise byte-identical to that commit; audit reports are not
packaged):

- 50 text file(s) normalized to repository format: LF line endings, no trailing whitespace, no blank lines at end of file
