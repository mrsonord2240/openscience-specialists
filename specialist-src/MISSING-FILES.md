# Missing referenced files — aipoch/medical-research-skills@f5ef65b9 (2026-09-10)

157 files referenced by 81 SKILL.md files do not exist, locally or in the upstream
commit (verified against the GitHub archive in Downloads, whose comment is the commit SHA). 80 of them
are scripts. Full table: `missing-referenced-files.csv`.

Detection: paths written as `references/…`, `scripts/…`, `assets/…`, `templates/…` with a file
extension, plus `from scripts.x import` lines. Bare filenames listed under a directory heading are
not caught, so this is a floor — agents found a few more by hand (e.g. `retraction-watcher`,
`adverse-event-narrative`).

| Skill | Collection / category | Audit score | Missing files |
| ----- | --------------------- | ----------- | ------------- |
| `research-grants` | scientific / Protocol Design | unaudited | `references/budget_preparation.md`, `references/resubmission_strategies.md`, `references/review_criteria.md`, `references/team_building.md`, `references/timeline_planning.md`, `scripts/budget_calculator.py`, `scripts/compliance_checker.py`, `scripts/deadline_tracker.py`, `scripts/generate_schematic.py` |
| `pathml` | scientific / Data Analysis | 78 (report claims 87) | `references/data_management.md`, `references/graphs.md`, `references/image_loading.md`, `references/machine_learning.md`, `references/multiparametric.md`, `references/preprocessing.md` |
| `pyhealth` | scientific / Data Analysis | 78 (report claims 86) | `references/datasets.md`, `references/medical_coding.md`, `references/models.md`, `references/preprocessing.md`, `references/tasks.md`, `references/training_evaluation.md` |
| `tooluniverse-statistical-modeling` | scientific / Data Analysis | 75 (report claims 88) | `references/bixbench_patterns.md`, `references/cox_regression.md`, `references/linear_models.md`, `references/logistic_regression.md`, `references/ordinal_logistic.md`, `references/troubleshooting.md` |
| `bmi-bsa-calculator` | scientific / Other | unaudited | `references/bsa_formulas_comparison.md`, `references/chemotherapy_dosing.md`, `references/ethnic_adjustments.md`, `references/pediatric_norms.md`, `scripts/calculator.py` |
| `hypothesis-generation` | scientific / Protocol Design | 79 (report claims 88) | `assets/FORMATTING_GUIDE.md`, `references/experimental_design_patterns.md`, `references/hypothesis_quality_criteria.md`, `references/literature_search_strategies.md`, `scripts/generate_schematic.py` |
| `linkedin-optimizer` | scientific / Academic Writing | unaudited | `references/headline-templates.md`, `references/keywords-by-specialty.json`, `references/linkedin-examples.md`, `scripts/linkedin_optimizer.py` |
| `pydicom` | scientific / Data Analysis | 78 (report claims 88) | `references/transfer_syntaxes.md`, `scripts/anonymize_dicom.py`, `scripts/dicom_to_image.py`, `scripts/extract_metadata.py` |
| `shap` | scientific / Data Analysis | 76 (report claims 87) | `references/explainers.md`, `references/plots.md`, `references/theory.md`, `references/workflows.md` |
| `citation-chasing-mapping` | scientific / Evidence Insight | 75 (report claims 89) | `references/audit-reference.md`, `references/guide.md`, `scripts/citation_mapper.py`, `scripts/main.py` |
| `citation-formatter` | scientific / Academic Writing | 75 (report claims 89) | `references/guide.md`, `scripts/citation_formatter.py`, `scripts/main.py` |
| `irb-application-assistant` | scientific / Academic Writing | 75 (report claims 89) | `references/audit-reference.md`, `references/guide.md`, `scripts/main.py` |
| `Case-control-study-quality-assessment-nos` | scientific / Data Analysis | 78 (report claims 88) | `references/nos_criteria_prompts.md`, `scripts/extract_pdf.py`, `scripts/format_nos_table.py` |
| `biopython-advanced` | scientific / Data Analysis | unaudited | `scripts/codon_usage.py`, `scripts/motif_stats.py`, `scripts/restriction_sites.py` |
| `cohort-study-quality-assessment-nos` | scientific / Data Analysis | 77 (report claims 90) | `references/nos_criteria.md`, `scripts/calculate_nos_score.py`, `scripts/extract_pdf.py` |
| `meta-screening-fulltext` | scientific / Data Analysis | 75 (report claims 88) | `references/screening_prompts.md`, `scripts/extract_pdf.py`, `scripts/query_pubmed.py` |
| `patent-landscape` | scientific / Evidence Insight | unaudited | `references/ipc-classifications.md`, `references/patent-search-strategies.md`, `scripts/patent_landscape.py` |
| `literature-management` | scientific / Other | 78 (report claims 88) | `references/examples.md`, `scripts/import_library.py`, `scripts/requirements.txt` |
| `pdf-processor` | scientific / Other | 79 (report claims 88) | `references/examples.md`, `scripts/pdf_tool.py`, `scripts/requirements.txt` |
| `abstract-summarizer` | scientific / Academic Writing | unaudited | `scripts/batch.py`, `scripts/summarizer.py` |
| `anatomy-quiz-master` | scientific / Academic Writing | unaudited | `scripts/adaptive.py`, `scripts/quiz_generator.py` |
| `authorship-credit-gen` | scientific / Academic Writing | 76 (report claims 90) | `references/guide.md`, `scripts/authorship_credit.py` |
| `cover-letter-generator` | scientific / Academic Writing | 78 (report claims 88) | `assets/cover_letter_template.md`, `references/guide.md` |
| `molecular-review-workflow` | scientific / Academic Writing | 77 (report claims 90) | `scripts/pubmed_api.py`, `scripts/validate_skill.py` |
| `personal-statement` | scientific / Academic Writing | unaudited | `references/personal-statement-examples.md`, `scripts/personal_statement_writer.py` |
| `sample-size-power-calculator` | scientific / Academic Writing | 75 (report claims 89) | `references/audit-reference.md`, `scripts/main.py` |
| `adme-property-predictor` | scientific / Data Analysis | unaudited | `scripts/adme_predictor.py`, `scripts/batch_processor.py` |
| `code-refactor-for-reproducibility` | scientific / Data Analysis | unaudited | `references/environment-setup.md`, `references/guide.md` |
| `fastqc-report-interpreter` | scientific / Data Analysis | unaudited | `references/troubleshooting.md`, `scripts/fastqc_interpreter.py` |
| `meta-abstract-screener` | scientific / Data Analysis | 77 (report claims 89) | `references/screening_prompts.md`, `scripts/screen_paper.py` |
| `cross-disciplinary-bridge-finder` | scientific / Evidence Insight | unaudited | `references/guide.md`, `scripts/interdisciplinary.py` |
| `academic-norm-review` | scientific / Other | 78 (report claims 88) | `assets/academic_compliance_checklist.md`, `references/guide.md` |
| `text-format-organizer` | scientific / Other | 78 (report claims 88) | `scripts/init_run.py`, `scripts/text_formatter.py` |
| `clinic-research-design` | scientific / Protocol Design | 78 (report claims 88) | `scripts/calculators/sample_size.py`, `scripts/main.py` |
| `model-calibration-curve` | medical / Data Analysis | 95 | `scripts/install_dependencies.R` |
| `nomogram-construction` | medical / Data Analysis | 96 | `scripts/install_dependencies.R` |
| `wgcna-analysis` | medical / Data Analysis | 90 | `references/diagnosis-report.md` |
| `adverse-event-narrative` | scientific / Academic Writing | 75 (report claims 90) | `scripts/narrative_generator.py` |
| `automated-soap-note-generator` | scientific / Academic Writing | 76 (report claims 90) | `scripts/soap_generator.py` |
| `clinical-decision-support` | scientific / Academic Writing | 77 (report claims 88) | `scripts/generate_schematic.py` |
| `digital-twin-discharge-drafter` | scientific / Academic Writing | unaudited | `scripts/discharge_drafter.py` |
| `discussion-section-architect` | scientific / Academic Writing | 76 (report claims 91) | `references/guide.md` |
| `graph-interpretation` | scientific / Academic Writing | unaudited | `scripts/graph_interpreter.py` |
| `journal-cover-prompter` | scientific / Academic Writing | unaudited | `scripts/cover_prompter.py` |
| `literature-review` | scientific / Academic Writing | 77 (report claims 88) | `scripts/generate_schematic.py` |
| `meta-manuscript-generator` | scientific / Academic Writing | 76 (report claims 90) | `references/writing-guide.md` |
| `meta-results-sensitivity-analysis` | scientific / Academic Writing | 76 (report claims 90) | `scripts/format_result.py` |
| `paper-2-web` | scientific / Academic Writing | unaudited | `scripts/generate_schematic.py` |
| `radiology-image-quiz` | scientific / Academic Writing | unaudited | `scripts/radiology_quiz.py` |
| `tone-adjuster` | scientific / Academic Writing | unaudited | `scripts/tone_adjuster.py` |
| `baseline-extraction-for-clinical-trials` | scientific / Data Analysis | unaudited | `scripts/baseline_extractor.py` |
| `biopython-phylo` | scientific / Data Analysis | unaudited | `scripts/phylo_task.py` |
| `biopython-sequence-io` | scientific / Data Analysis | unaudited | `scripts/sequence_io.py` |
| `biopython-structure` | scientific / Data Analysis | unaudited | `scripts/neighbor_search.py` |
| `forest-plot-styler` | scientific / Data Analysis | 75 (report claims 89) | `scripts/main.py` |
| `pathology-roi-selector` | scientific / Data Analysis | 75 (report claims 89) | `scripts/main.py` |
| `spatial-transcriptomics-mapper` | scientific / Data Analysis | unaudited | `scripts/generate_test_data.py` |
| `statistical-analysis` | scientific / Data Analysis | 77 (report claims 90) | `references/test_selection_guide.md` |
| `survival-analysis-km` | scientific / Data Analysis | 75 (report claims 89) | `scripts/main.py` |
| `bio-ontology-mapper` | scientific / Evidence Insight | unaudited | `scripts/mapper.py` |
| `biopython-entrez` | scientific / Evidence Insight | unaudited | `scripts/pubmed_summaries.py` |
| `citation-network` | scientific / Evidence Insight | 77 (report claims 90) | `references/README.md` |
| `diffdock-molecular-docking` | scientific / Evidence Insight | unaudited | `references/workflows_examples.md` |
| `gwas-database` | scientific / Evidence Insight | 75 (report claims 87) | `references/api_reference.md` |
| `journal-latest-issue` | scientific / Evidence Insight | 78 (report claims 88) | `scripts/journal_digest.py` |
| `key-takeaways` | scientific / Evidence Insight | unaudited | `references/guide.md` |
| `open-access-scout` | scientific / Evidence Insight | 77 (report claims 91) | `scripts/oa_scout.py` |
| `patent-claim-mapper` | scientific / Evidence Insight | unaudited | `scripts/claim_mapper.py` |
| `scientific-critical-thinking` | scientific / Evidence Insight | 78 (report claims 87) | `scripts/generate_schematic.py` |
| `article-format-adjustment` | scientific / Other | unaudited | `templates/science_format.json` |
| `buffer-calculator` | scientific / Other | unaudited | `references/troubleshooting.md` |
| `clinical-reports` | scientific / Other | 76 (report claims 88) | `scripts/generate_schematic.py` |
| `file-search` | scientific / Other | unaudited | `scripts/test_skill.py` |
| `lab-result-interpretation` | scientific / Other | 75 (report claims 91) | `references/test_metadata.json` |
| `literature-statistics` | scientific / Other | unaudited | `scripts/process_references.py` |
| `patient-consent-simplifier` | scientific / Other | 75 (report claims 89) | `scripts/consent_simplifier.py` |
| `pdf-to-ppt-pack` | scientific / Other | unaudited | `scripts/validate_skill.py` |
| `symptom-checker-triage` | scientific / Other | unaudited | `references/red_flags.md` |
| `treatment-plans` | scientific / Other | unaudited | `scripts/generate_schematic.py` |
| `basic-research-design` | scientific / Protocol Design | 77 (report claims 89) | `references/prompt_templates.md` |
| `research-proposal-generator` | scientific / Protocol Design | 79 (report claims 88) | `references/prompts.md` |
