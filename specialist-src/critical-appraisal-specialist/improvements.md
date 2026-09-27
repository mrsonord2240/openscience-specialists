# Improvements — Biomedical Critical Appraisal Specialist (2026-09-10)

## Missing workflow steps
- **Observational risk of bias has no tool.** Both NOS Skills were dropped under gate 8: their criteria files (`references/nos_criteria.md`, `references/nos_criteria_prompts.md`) and scripts (`calculate_nos_score.py`, `format_nos_table.py`, `extract_pdf.py`) were never shipped upstream. Cohort, case-control, cross-sectional and non-randomised intervention studies get a labelled structured appraisal only. Fix this with a fixed-upstream NOS pair or an audited ROBINS-I / ROBINS-E Skill.
- **The formal risk-of-bias tools are supporting-grade.** RoB 2 and QUADAS-2 score 78 by their POLISH_CHANGELOG, so core coverage rests on the four medical reading/claim Skills. An audited RoB 2 Skill scoring 85 or more, with complete Domain 3–5 signalling questions, is the top upgrade.
- **Unaudited design-specific tools already exist in `F:\OpenScience\skills\scientific\Data Analysis`:** `probast-quality-assessment-for-prediction-model-studies`, `quadas-c-assessment-for-diagnostic-accuracy-studies`, `quapas-quality-assessment-for-prognosis-studies`. They have only legacy `*_audit_result_v1.json` files, no skill-auditor report. Audit them, then run a gate-8 file check.
- **Journal-club and peer-review deliverables:** `scientific/Academic Writing/journal-club-presenter` and `scientific/Academic Writing/peer-review` are unaudited (legacy audit files only). Once audited they would replace the ad-hoc reviewer-report and kit formats the prompt currently asks for.
- **Registry and outcome-switching check is prompt-only.** Candidates: `scientific/Data Analysis/outcome-extraction-for-clinical-trials` (unaudited) and `scientific/Evidence Insight/clinicaltrials-database` (changelog 77, supporting-eligible, but it duplicates the `clinical-trials` Connector through direct API calls).
- **No spin-detection or statistical-consistency Skill.** Checks like abstract-versus-results spin and GRIM/statcheck-style recomputation exist only as prompt gates. An executing consistency checker would turn the derivation gate into a tool result.
- **No CASP / JBI checklists and no GRADE Skill.** GRADE belongs to body-of-evidence work and is correctly routed out, but journal-club users often expect a CASP-style checklist.

## Bundled-Skill defects that matter here
- `rct-bias-assessment-rob2`: `references/rob2_guidelines.md` stubs Domains 3–5 ("Refer to standard ROB2 guidance"). Its Domain 1 algorithm misses answer combinations. `format_rob2_result` defaults missing domains to "Some concerns". The SKILL.md PDF command (`python extract_pdf.py`, output `full_text.txt`) doesn't match the script (`<pdf> [--output]`, output `<stem>_fulltext.txt`). There are no cluster or crossover variants. The prompt compensates for all of these, but an upstream fix would remove reliance on model memory of RoB 2.
- `diagnostic-study-quality-assessment-quadas-2`: comments must be in Chinese, there is no domain-level judgment or applicability section, `references/api_reference.md` is a template placeholder, and `scripts/quadas_assessment.py` is a stub.
- `retraction-watcher`: `get_stats` counts failed lookups and citations with no DOI or PMID as clear. It advertises title and fuzzy matching but doesn't implement it, and it never sets the "corrected" status. It depends on the Open Retractions endpoint, whose availability is unverified. An upstream patch should report those cases as `unknown`.
- `scientific-critical-thinking`: its default instruction to generate schematics points at a script and Skill that aren't bundled (recorded as `known_missing`).
- Audit P1s still relevant:
  - paper-to-claim-verifier issues verdicts from PMID-only input (the prompt forces "unable to verify").
  - figure-first-paper-reader lacks provisional labels for caption-only reads.
  - contradictory-findings-resolver doesn't tag assumptions and gives no per-paper citation guidance above three papers.
  - study-design-identifier and methods-reverse-engineer have no rule for obfuscated methods.
  - result-reliability-checker has no path for conference abstracts.
  - reporting-guideline-compliance-checker has no partial-results path, and its P2 notes that STARD and CARE aren't covered, which leaves a gap in diagnostic-study peer review.

## Connector gaps
- No Crossref or Retraction Watch Connector, so retraction status rests on PubMed publication types and a network-dependent script.
- Only registries the `clinical-trials` Connector exposes can be checked. ISRCTN, EU CTR, ChiCTR, ANZCTR and WHO ICTRP stay unverified, so outcome-switching checks on non-US trials are weak.
- No post-publication review source (for example PubPeer), and no access to journal peer-review histories.

## System-prompt limits
- At 21,996 characters the prompt is at the ceiling. Any new Skill needs routing text traded out of the playbook.
- The RoB 2 Domain 3–5 judgments and the QUADAS-2 applicability judgments depend on the model knowing the published tools. A bundled, complete reference would make them auditable.
- The prompt overrides QUADAS-2's language rule so output follows the user's language. If the App enforces Skill templates strictly, confirm this override.

## Builder observations
- `REF_RE` in `build_specialist.py` only detects references written with a directory prefix. `retraction-watcher` names `citation-formats.md`, `api-documentation.md`, `example-reports/` and `requirements.txt` without one, so gate 8 misses them. They were added to `known_missing` by hand.

## Evaluation this Specialist still needs
- A graded case set:
  - an RCT with documented outcome switching against its registry
  - a null-primary trial whose abstract is spun
  - a retracted paper
  - a "prospective" study that is actually a retrospective cohort
  - a diagnostic study that used case-control sampling
  - a cluster RCT (it must not receive a RoB 2 score)
  - a title-only request for a landmark trial (it must refuse to reconstruct the paper)
  - a retraction check with the network down (it must report `unknown`, not clear)
- Agreement of the Specialist's RoB 2 domain judgments with two independent human raters on 10 or more trials, plus a check that every judgment carries a quote.
