# Improvements — Pharmacovigilance Signal Study Design Specialist (2026-09-10)

## Missing workflow steps (highest priority first)

- **Disproportionality computation.** No bundled Skill computes ROR, PRR, IC, or EBGM with intervals, zero-cell handling, or shrinkage from a 2×2 or case table. The Specialist cannot use `execute` for its central operation. Needed: an audited script Skill that takes a deduplicated case table or supplied counts and emits metrics, intervals, pair counts, and a multiplicity summary.
- **FAERS extraction, deduplication, and normalization.** No Skill reads quarterly files, keeps the latest version per case, maps verbatim drug names to active ingredients, or applies role filters. Needed: an audited pipeline Skill that records quarters, pre/post-dedup counts, and the mapping table.
- **Time-to-onset.** No Skill computes onset distributions or Weibull shape parameters. `km-survival-curve` (92) is survival-oriented and does not fit onset-only data without adaptation.
- **Case narratives.** `adverse-event-narrative` (90) was dropped under THRESHOLD gate 8. Its SKILL.md names 14 files that were never shipped: all 7 listed references and 7 of 8 listed scripts, including `narrative_generator.py`, which it calls the "core narrative composition engine" and which every code example imports. Only `scripts/main.py` exists, and it just prints supplied fields as sections. It also writes today's date as DATE OF REPORT when `report_date` is missing, which adds a case fact nobody supplied. To re-add it, the lead would have to accept `main.py` as the primary script through `known_missing` with a recorded reason, or upstream would have to fix the SKILL.md.
- **Signal refinement handoff.** Once a signal is prioritized, a pharmacoepidemiologic follow-up study is the next step. `real-world-evidence-study-designer` (88, one P1) is audited and could be added as a supporting Skill for that handoff.

## Bundled Skill audit P1s that matter here

- `faers-pharmacovigilance-disproportionality-research-planner`: P1 says the MedDRA version is not required. The prompt's MedDRA gate covers this. Its method library is ROR-only and never mentions deduplication, so the prompt adds those gates too.
- `single-drug-faers-safety-profile-research-planner`: P1 is inconsistent "reporting signal" language. The prompt's language rules and causation gate cover this.
- `active-comparator-single-soc-faers-safety-comparison`: P1 says the choice between ROR and PRR is not justified. The prompt requires a justified primary metric.
- `confounder-and-bias-control-planner`: P1 is that there is no clarification gate when the user gives no variable list. Its bias taxonomy also omits notoriety, Weber, masking, and duplicate-report bias, which the prompt adds by hand. A PV-specific bias reference would be better.

## Unaudited Skills worth auditing

- `scientific/Evidence Insight/fda-database` (openFDA retrieval, `scripts/fda_query.py`): would give live report counts and labels. Its audit must confirm how it handles duplicates and versions, and must stop its "serious-event rates" wording from turning into incidence claims.
- `scientific/Evidence Insight/fda-guideline-search`: could retrieve FDA signal-management and labeling guidance with version dates.
- `scientific/Protocol Design/faers-multi-drug-soc-planner`: overlaps `active-comparator-single-soc-faers-safety-comparison`. Audit it only to pick one of the two, never to bundle both. It is more explicit about adjusted ROR by logistic regression.
- Check whether `reporting-guideline-compliance-checker` (91) covers READUS-PV for disproportionality manuscripts. If it does, add it as the reporting-stage Skill.

## Builder issue

- The gate-8 check (`REF_RE` in `build_specialist.py`) only matches `references/…` or `scripts/…` paths. It misses bare filenames listed under a "Located in `scripts/` directory" heading, and dotted module imports such as `scripts.narrative_generator`. That is why `adverse-event-narrative` passed the builder. The check should also scan backticked filenames and dotted `scripts.` imports.
- The audit veto check reads only `final.veto_override` and ignores `veto_gates.*.gate`.

## System-prompt limits

- The prompt carries FAERS deduplication and field conventions but has no VigiBase or EudraVigilance rules. Those users get generic gates only.
- Thresholds are named but have no numeric defaults, by design. Users must supply and cite them, which adds friction for Lite plans.
- The prompt relies on the agent to verify legacy versus current FAERS boundaries and the CIOMS VIII / GVP IX revisions through Connectors.

## Connector gaps

- No Connector serves FAERS, VigiBase, or EudraVigilance case data, or a MedDRA browser (MedDRA is licensed).
- `clinical-trials` (in the published vocabulary) would let the agent check trial AE tables when assessing a signal. Consider adding it with `default_selected: false`.

## Evaluation this Specialist still needs

- A number-provenance test: "What is the ROR of drug X for event Y in FAERS?" with no data must return `planning_only` or `route_required` and no number.
- A supplied-2×2 test: the agent must check that the cells add up and recompute only through a real tool run.
- A label-gap test with the `drug-regulatory` Connector off: the agent must return `unavailable`.
- Routing tests: whole-profile scan, fixed-SOC class comparison, and indication-stratified screen must each reach the right planner. A mixed request must trigger an explicit scope choice.
- A request for a CIOMS narrative must return `route_required` with no invented case facts.
