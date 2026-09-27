# Improvements — Research Grant Proposal Specialist (2026-09-10)

## Top priorities

1. **Audited full-proposal drafting Skill (≥ 85).** Gate 2 now scores `grant-proposal-assistant` at 76 (polish changelog; its report claimed 91), so it can only be a supporting scaffold. The Research Strategy (Significance, Innovation, Approach) is written by prompt reasoning over templates. Build or audit a Skill that drafts per-aim Approach text (rationale, design, controls, power, pitfalls, milestones) from an aims page plus an evidence ledger.
2. **Audited mock-review Skill (≥ 85) on the current review framework.** `grant-mock-reviewer` scores 76. Its script scores by keyword counts (base 5, ±0.5/0.3 per matched word) and maps scores to a hard-coded percentile table. Its rubric reference carries approximate IC paylines and claims criterion scores are "combined algorithmically" into Overall Impact, which is wrong. The validation stage has no core Skill. It needs a reasoning-based reviewer keyed to the current NIH factor framework and to the NSF criteria.
3. **Funding-notice verification Skill or Connector.** Every agency rule (page limits, review criteria, caps, biosketch format, clinical-trial allowance, AI-use policy) is time-sensitive, and no declared Connector returns funder rules. The prompt falls back to asking the user to paste the notice. A Skill or Connector that fetches the NIH Guide, grants.gov, or NSF solicitations and PAPPG text with a version and access date would close the biggest verification gap.

## Missing workflow steps

- **Data management and sharing plan.** No Skill covers it, although both NIH and NSF require one. It is currently a checklist-only `route_required`.
- **Letters of support and collaboration.** No Skill covers them. Any future Skill must emit templates for the signatory and never assert commitments.
- **Biosketch and other support.** `scientific/Academic Writing/nih-biosketch-builder` is unaudited, and its description cites the "2022 OMB-approved" format, which is likely stale because NIH and NSF have since moved to common forms generated in SciENcv. Audit it and update it against the current format before bundling.
- **Timeline and Gantt.** `scientific/Evidence Insight/grant-gantt-chart-gen` is unaudited. It ships `scripts/main.py` with no missing references, so it is a good audit candidate for the aims-by-years feasibility check.
- **Opportunity search and fit.** `scientific/Evidence Insight/grant-funding-scout` and `funding-trend-forecaster` are unaudited. Both would need Connector-backed data rather than memory to be safe.
- **Competing-hypothesis generation from preliminary observations.** `hypothesis-generation` was dropped under gate 8 because its `references/` (3 files), `assets/FORMATTING_GUIDE.md`, and `scripts/generate_schematic.py` were never shipped upstream, and it mandates a non-bundled `scientific-schematics` Skill. `aim-and-hypothesis-designer` covers aim-level hypotheses only.
- **Executable power calculation.** Only the planning-only `sample-size-and-power-planning-assistant` is bundled. `sample-size-basic` (76 on the changelog; its report claims 90) was not added: its script does not match its SKILL.md (it has no Cohen's d or paired t-test input), and its survival formula computes events as (z_a+z_b)²/(0.5·ln(HR)²), half the Schoenfeld 1:1 value. Fix it before adding an execution step. `sample-size-power-calculator` scores 75 on the changelog, so it is supporting-only at best.
- **NSFC.** `nsfc-grant-writer` was removed. Its `references/writing-guide.md` says to "generate plausible preliminary work" (with "specific data if possible") when the user supplies only a hypothesis, which directly violates the runtime contract. Its `template.md` has lost the Chinese outline headings that the Skill says must be preserved exactly. It also scores 75 on the changelog, below the level where it could anchor a workflow. It needs an upstream fix before reinstatement.
- **`research-grants`** (unaudited) also fails gate 8, with 5 missing references and a missing `scripts/budget_calculator.py`.

## Bundled-Skill defects that matter here

- `grant-specific-aims-writer` P1: `references/budget_templates.md` is out of scope and full of illustrative salaries, fringe rates, and costs. The prompt forbids using it, but the file still ships. The same file also ships in `grant-proposal-assistant`. Both Skills ship an identical `scripts/main.py` that hard-codes R01 "$500K/year", R21 "$275K total", R03 "$100K/year", and page limits as facts.
- `grant-specific-aims-writer` P1: NSF Broader Impacts is under-weighted in the Skill. The prompt makes a BI placeholder `blocked`. The upstream SKILL.md is also titled "Grant Proposal Assistant", a copy-paste error that invites routing confusion.
- `aim-and-hypothesis-designer` P1: it has no structured clarification protocol. The prompt injects a 2–4 question rule, but the Skill itself should carry it.
- `grant-budget-justification`: its SKILL.md parameters (`--input`, `--justification-type`, `--agency`) do not exist in the script. The script only produces output with `--demo`, which uses fictitious personnel and costs. The prompt forbids `--demo`. The script should be rewritten to read user JSON or CSV.
- `novelty-vs-feasibility-assessor` P1: saturation and precedent judgments come from training knowledge without labels. The prompt requires `unverified` labels.
- `feasibility-aware-study-planner` P1: it defines no minimum input set. The prompt requires data or sample access, capacity, and time horizon before running.
- `grant-proposal-assistant` and `grant-mock-reviewer` references assert stale specifics: NIH biosketch "5 pages", NSF biosketch "2 pages", "highlight changes in margins" for A1 applications, and a five-criterion scoring layout. The notice gate covers these, but the references should be dated or removed.

## System-prompt limits

- At 21,999 characters the prompt is at the ceiling. Per-agency detail (ERC, UKRI, Wellcome, DoD CDMRP, foundations) is reduced to "structure from the pasted call only".
- The NIH simplified-framework and AI-use statements are deliberately generic and must be verified. They are not asserted with notice numbers.
- Resubmission handling is a single workflow step. A resubmission-introduction Skill that maps summary-statement critiques to changes would be better. `rebuttal-letter-strategist` is journal-oriented and scores 77.

## Connector gaps

- No funder-rules Connector (NIH Guide, grants.gov, NSF PAPPG and solicitations, NSFC guide).
- No NIH RePORTER or NSF award-search Connector for checking funded-project overlap, which is a core novelty check for grants. `clinical-trials` covers registered trials only.
- `research-resources` semantics are assumed (resource identifiers). Confirm what the App's Connector actually returns.

## Evaluation this Specialist still needs

- Adversarial cases: a hypothesis with no data asking for a full aims page (it must produce placeholders, not invented figures); a request for a funding probability; a reviewer uploading someone else's application; a budget request with no costs; an NSF summary with no Broader Impacts; an R21 carrying three dependent aims.
- Notice-verification behavior: check that every page limit or criterion in the output carries an identifier and access date or an `unverified_from_memory` tag.
- Scoring discipline: check that no script-derived score, percentile, or payline appears in any mock review.
- Routing: settled aims should enter at Stage 2 without rerunning Stage 0 or 1; a vague idea should trigger the 2–4 clarification questions.
