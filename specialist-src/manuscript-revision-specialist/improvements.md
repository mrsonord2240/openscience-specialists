# Improvements — Manuscript Submission and Peer-Review Revision Specialist (2026-09-10)

## P1: response drafting has no core-grade Skill
- The letter itself relies entirely on supporting Skills: `author-response-builder` 84 (Limited Release), `response-letter` 77, `rebuttal-letter-strategist` 77, `response-tone-polisher` 76 (the last three are POLISH_CHANGELOG scores). Triage is core (`revision-strategy-planner` 91, `paper-sprint-review` 95), so correctness rests on the prompt's Change Ledger and gates. To fix: re-audit `response-letter` with a real, non-templated test set, and close `author-response-builder`'s two P1s (the 8-section output is too verbose for simple inputs; there is no mode-count summary) to lift it to 85 or higher. Then promote one of them to core.
- 2026-09-10: `response-letter` changed from core to supporting under the revised THRESHOLD gate 2 (changelog score 77).

## P1: bundled scripts that fabricate or false-clear (checked by reading the code and running it)
- `rebuttal-letter-strategist/scripts/main.py`: the "minor" and "moderate" templates hard-code "We have revised the manuscript accordingly" / "We have now clarified this". The SKILL.md parameters (`response_type`, `evidence`) don't match the CLI (`--criticism`, `--revision`). Upstream fix: make completion phrases conditional on an explicit changes input.
- `response-tone-polisher/scripts/main.py`: `_transform_to_acceptance` prepends "We have revised the manuscript as suggested." Its replacement rules insert "we have revised", "have now expanded" and "have added appropriate caveats", and it picks phrases with `random.choice`, so output is nondeterministic. Same upstream fix is needed. If it isn't fixed, consider dropping both Skills; the prompt's fabricated-completion gate is the only safeguard right now.
- `retraction-watcher/scripts/main.py`: `get_stats` counts every reference with no hit as "clear", including references with no DOI/PMID and failed requests. The Crossref test reads `update-to`, which appears on retraction notices, not on the retracted article. The title fuzzy matching and Retraction Watch database lookup that SKILL.md describes are not implemented, and corrections are never detected. It needs an upstream fix plus an eval against known retracted DOIs and PMIDs.
- `blind-review-sanitizer/scripts/main.py`, run on a sample: the whole clause "Laboratory tests were performed … multicenter cohort" was replaced by [INSTITUTION], "2010 2015 2020" became [PHONE], "A. Chen" survived, and "[PREVIOUS WORK] (Chen et al., 2021)" still identifies the authors. In .docx mode the acknowledgments body is kept and headers, footers, comments and properties are ignored. It needs narrower rules, initials handling, and a fixture test.
- `figure-reference-checker/scripts/main.py`: `--manuscript paper.docx` searches the literal string. The regex `Fig\.?\s*(\d+)` misses "Figure 1", so on a sample it returned only ['2']. The orphan and label checks that SKILL.md claims do not exist. Candidate for removal. `scientific/Other/result-figure-consistencycheck` (77, all referenced files present) is the natural replacement once its PDF-to-Markdown input requirement fits.
- `journal-recommender/scripts/journal_ranker.py`: the double-escaped regex means it never sorts by impact factor (a 3.1 journal stays above a 10.5 one), and `--help` prints nothing because there is no `__main__`. `medical/Academic Writing/target-journal-matcher` (86) would be the better Skill once its open P0 is closed (tier classification missing from script output).

## Lost or missing coverage
- Cover letter: `cover-letter-generator` was dropped under gate 8 (assets/cover_letter_template.md and references/guide.md never shipped). It is replaced by `medical/Academic Writing/cover-letter-drafter` (86, all files present). Drafter P1: no prior-submission disclosure guidance for resubmissions. Its P5 template asserts originality and author approval by default, which the prompt gates. An unaudited `scientific/Academic Writing/cover-letter-drafter` with the same ID and different content exists. If another Specialist ships that one, installing both will raise a Skill conflict.
- Word manuscripts: `arxiv-preflight` verifies references only from BibTeX and extracts only LaTeX or PDF. Most biomedical submissions are .docx with Vancouver references, so they get no automated existence check. This needs a DOCX/RIS/plain-list reference verifier.
- Bounded responses need limitation text: `medical/Academic Writing/limitation-and-risk-writer` (90) fits.
- Claim-to-source support with full text: `medical/Evidence Insight/paper-to-claim-verifier` (89) would strengthen `reference-integrity-checker`.
- Title and abstract edits for a new target: `medical/Academic Writing/title-and-abstract-optimizer` (85). Language-level revision requests: `medical/Academic Writing/medical-english-precision-editor` (91).
- Statistical-reviewer comments: no bundled Skill checks test choice or assumptions. `statistical-analysis` is already published (gate 9 byte reuse), but its source SKILL.md references a missing `references/test_selection_guide.md`; confirm against the published bytes before adding it.
- Not viable as-is: `authorship-credit-gen` (76) and `citation-formatter` (75) both lack their primary scripts under gate 8. `academic-norm-review` (78) lacks its checklist and guide.
- Unaudited but useful once audited: `peer-review-response-drafter`, `conflict-of-interest-checker` (suggested-reviewer conflicts), `resubmission-deadline-tracker`, `semantic-consistency-auditor`, `sci-paper-reviewer`, `reference-style-sync`, `journal-matchmaker`, `journal-impact-factor-trend`.
- Reporting guidelines: the bundled rules cover only CONSORT, STROBE, PRISMA and TRIPOD. The audit P2s note STARD and CARE are missing and there is no version-selection guidance. The prompt labels other guidelines as outside the rule base.
- There is no Skill for data-availability, ethics/IRB or funding-statement completeness checks.

## Bundled-Skill P1s the prompt compensates for
- `consistency-checker-across-manuscript`: it doesn't separate rounding differences from contradictions and underclassifies title-level numbers. The prompt covers both under Rigor.
- `revision-strategy-planner`: no composability with `author-response-builder` and no timeline handling. The prompt's handoff order and intake deadline cover these.
- `reporting-guideline-compliance-checker` and `reference-integrity-checker`: no partial-results path. The prompt marks items unclear or unchecked.
- `claim-strength-calibrator`: its three-layer output (Section C plus D/E) is redundant. This is cosmetic.

## Shared-ID risk
- `claim-strength-calibrator` and `reference-integrity-checker` are packaged with the published `auto-research-specialist@1.0.1` bytes (content digests 1421449d5557 and a9a06b5101b9). Any upstream change must ship in lock-step in both Specialists or under a new ID; otherwise installing both raises a Skill conflict. Their release-config descriptions differ between the two Specialists (display names match). Align them at the next release of either Specialist.

## Connector gaps
- No Connector supplies JCR metrics, acceptance rates, APCs or journal warning lists, so journal metrics stay "unverified" unless the user supplies them.
- No Crossref or Retraction Watch Connector. Retraction status depends on script network access plus `pubmed` publication types.
- No dedicated source for EQUATOR guideline versions or journal author instructions; this relies on `literature` returning official pages. Test whether `research-resources` resolves them.

## System prompt limits
- At 21,951 characters the prompt is at the target cap; any addition needs an equal cut.
- The "script limits" block is tied to the code at upstream f5ef65b9. Revise it whenever a bundled script changes, or it becomes a false warning.
- Runtime assumptions: Python 3.9+, network for `retraction-watcher` and `arxiv-preflight`, python-docx for .docx sanitization, pdftotext for PDF preflight. None are verified per runtime.

## Evaluation this Specialist still needs
- A major revision with three reviewers where several requested changes were not made. Pass: no completion claim without a ledger row, and comment and sub-point coverage equals 100%.
- Conflicting reviewers. Pass: the conflict and the chosen path appear in the Overview for the Editor.
- A .docx with author names in the header, properties, comments and "our previous study". Pass: the output says "manual verification required" and names each residual.
- A reference list containing a known retracted PMID, a DOI-less entry and a preprint. Pass: flagged, unchecked and unchecked, never "Clear".
- An observational cohort with causal wording and a STROBE check. Pass: causal verbs are flagged and every "present" item cites a location.
- A journal recommendation request. Pass: no unsourced impact factor or acceptance odds.
- A trial whose registered and reported primary outcomes differ. Pass: the discrepancy is reported with registry source and dates.
