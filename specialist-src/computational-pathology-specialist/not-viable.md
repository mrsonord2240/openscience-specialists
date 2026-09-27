# Not viable — Computational Pathology Whole-Slide Image Specialist (2026-09-10)

Not built. Gate 4 (end-to-end coverage) fails, and the gate 3 scores for the core Skills do not hold up once the files are read. Gates 5–7 pass. Provenance matches upstream `f5ef65b9`, so every defect below exists upstream too. None were introduced locally.

## Failing gates

**Gate 4: no usable Skill performs the central operation.** The central operation here is slide-level WSI analysis: QC, then tiling, then tile features, then a slide/patient-level model. It rests on three `core` Skills:

| Skill | Nominal audit | What the files actually contain |
| --- | --- | --- |
| `pathology-roi-selector` | 89 | A generic template. Its only execution surface, `scripts/main.py`, is missing from both the local folder and the upstream tree. The rest is one line ("WSI region detection for AI training") plus three parameters (`wsi_file`, `tissue_type`, `magnification`). It has no ROI algorithm, no scoring rule, no MPP handling and no output schema. It cannot do what a core Skill must. |
| `pathml` | 87 | A capability list. It routes every topic to six `references/*.md` files (image_loading, preprocessing, graphs, machine_learning, multiparametric, data_management), and none of them exist locally or upstream. It gives no stain-normalization parameters and no training or evaluation procedure. It also carries a K-Dense Web promotion block. |
| `histolab` | 88 | A real library guide with 5 reference files present. It covers slides, tissue masks, Random/Grid/Score tilers and filters. It has no scripts. Its own NOT-FOR list excludes stain normalization and nuclei segmentation, and it stops at tile extraction. |

That leaves one intact Skill (`histolab`), and it only covers preprocessing. Nothing trains or evaluates a slide-level model. Promoting `validation-strategy-designer` or `statistical-analysis` to core would pass the counting rule, but a planning Skill would then stand in for the missing execution step, which gate 4 forbids.

**Gate 3: the scores cannot be taken at face value.** The reports for `histolab`, `pathml`, `pathology-roi-selector` and `pydicom` share a single dynamic template: seven inputs labelled "Test case N for <skill>", identical totals 81/86/91/90/83/88/87, and the same generic four assertions. All four also record "Scripts parse without errors", including the three whose scripts do not exist. Their `POLISH_CHANGELOG.md` files record polished scores of 76 / 78 / 75 (histolab / pathml / roi-selector), while the reports claim 88 / 87 / 89. The builder would accept these numbers. A strict reading does not.

**Supporting Skill defect.** `pydicom` advertises `scripts/anonymize_dicom.py`, two more scripts and `references/`. None of them exist upstream. That leaves PHI de-identification of DICOM-WSI (label/overview images, headers) with no executable path.

## What is needed to make it viable

1. **A working ROI/tiling core Skill.** Either upstream ships `pathology-roi-selector/scripts/main.py` with a real method, or the Skill is dropped. A real method means: a tissue mask, region scoring from an annotation or probability map, coordinates reported at a stated level/MPP, and a documented output schema, with a smoke test. It then needs a fresh audit using real slide inputs (for example histolab's bundled sample slides). Target score ≥ 85.
2. **A slide-level modelling core Skill (new).** It covers tile-embedding extraction with a pinned encoder, then MIL aggregation (attention-MIL / CLAM-style). Splits must be patient-level and site-aware, and the Skill outputs per-slide and per-patient predictions with calibration. It must be executable (`scripts/`) and audited ≥ 85.
3. **Restore `pathml`.** Ship the six referenced files, remove the promotion block and re-audit it. Until then it can only be a supporting Skill.
4. **A stain-handling Skill.** Covers Macenko/Vahadane/Reinhard normalization and stain augmentation. The reference must be fit on training slides only, with the choice logged. Supporting role, audited ≥ 75.
5. **DICOM-WSI de-identification.** Either `pydicom` ships its advertised scripts, or `scientific/Other/dicom-anonymizer` gets re-audited under an `eval_report_*.json` name. Its current audit is `dicom-anonymizer_audit_result_v2.json`, which the builder does not detect, so it counts as unaudited. That audit must cover burned-in label/macro images and WSI-specific tags.
6. **Re-audit `histolab`, `pathml` and `pydicom` with domain-specific dynamic inputs**, replacing the shared template.
7. **Imaging-AI reporting.** Extend `reporting-guideline-compliance-checker` (91, two open P1s) to CLAIM and TRIPOD+AI, or add a dedicated Skill. It currently names TRIPOD only.

## Minimum viable composition once 1–2 and 5 land

- Core: `histolab` (QC + tiling), the new MIL Skill (central operation), and `validation-strategy-designer` (framing: patient-level, site/scanner and external validation).
- Supporting: `statistical-analysis`, `pydicom` or `dicom-anonymizer`, the stain Skill, and restored `pathml`.

Connectors as pre-filled (pubmed, literature, cancer-models) are adequate.

## Minor finding

`statistical-analysis/SKILL.md` cites `references/test_selection_guide.md`, which is not shipped (upstream defect).
