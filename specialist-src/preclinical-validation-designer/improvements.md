# Improvements — Preclinical Mechanism Validation Design Specialist (2026-09-10)

## Missing workflow steps
- **No ARRIVE 2.0 checker.** `reporting-guideline-compliance-checker` (91) covers CONSORT/STROBE/PRISMA/TRIPOD only. Neither method finds ARRIVE, animal, or preclinical in its SKILL.md or references (grep and Grep both). The Essential 10 mapping is prompt-enforced. Needs an ARRIVE Essential 10 plus Recommended Set checker Skill, or an ARRIVE module added to that checker.
- **No ethics/3Rs drafting.** `iacuc-protocol-drafter` (scientific/Academic Writing) fills this. It has only a v2-format audit (85, 2026-03-23, one P1), and the builder does not read that format. Re-audit with skill-auditor@1.0. Its output must still never claim approval.
- **No result-analysis Skills.** Once data exists there is nothing to hand off to. Candidates with only v2 audits (86, P1 "stabilize executable path"): `western-blot-quantifier`, `facs-gating-viz-style`, `preclinical-pkpd-analyst`. The last one also covers the exposure/target-engagement step before in vivo efficacy. All three need re-auditing.
- **No clustered or small-n power.** `sample-size-power-calculator` (89) advertises clustered designs but ships no `scripts/` or `references/` (fails gate 8). It could replace `sample-size-basic` once the files ship upstream.
- **No direct cell-line identity check.** `cellosaurus-api` (unaudited) would let the misidentification and STR gate be checked, not just stated. Also unaudited and useful for the reagent/RRID tables: `pdf-extract-experimental-materials` and `reagent-substitute-scout`. Also unaudited: `crispr-screen-analyzer` (screen-derived targets) and `translational-gap-analyzer`.
- Optional framing Skill: `drug-target-evidence-landscape` (86, two P1s) for checking prior preclinical evidence on a target before designing validation.

## Bundled Skill defects that matter here (all patched only in the prompt)
- `sample-size-basic`: a normal approximation that undersizes small-n animal groups (d = 1.5 gives 7 per group vs 9 by noncentral t; verified by running it). No clustering, no paired design, and the CLI names differ from SKILL.md.
- `randomization-gen`: no seed, even though SKILL.md promises a reproducible one. Stratification is implemented but not on the CLI, and an N that is not a multiple of the block size leaves an unbalanced last block.
- `methodology-extractor`: the script ignores `--papers` and runs only a demo. `sop-writer`: the script ignores user steps. `experiment-design`: the inline snippet sources a nonexistent `/Users/zhangmingda/...` venv, and its template is human-participant (IRB/consent).
- The builder rescored all five supporting Skills to 76–78 from their polish changelogs, just above the 75 floor. Any upstream regression drops them.
- Core audit P1s patched in the prompt: the mechanism planner has no null-result contingency; the animal/cell planner has no "insufficient model access" terminal; the blueprint builds competing routes. Upstream fixes would remove prompt load.

## Prompt limits
- Unit, randomization, blinding, sex, authentication, RRID, and 3Rs gates are prose rules. No Skill enforces them mechanically.
- Prompt is 21,989 chars, at the 22k ceiling. More Skills will need routing text cut elsewhere.
- The ARRIVE 2.0 item list is embedded. Web search on 2026-09-10 showed 2.0 (2020) is still current. The prompt tells the agent to re-verify through a Connector at runtime.

## Connector gaps
- It is unknown whether `cancer-models` covers non-cancer lines, primary cells, or rodent strains. Confirm what it maps to.
- No Connector exposes the ICLAC misidentified-lines register, strain-nomenclature authorities, or institutional/funder animal-policy text.
- Consider `cellguide` for primary-cell or cell-type selection when the finding is a single-cell state.

## Evaluation this Specialist still needs
- Scenario set:
  - an omics hit with no stated resources (must ask, not assume animal access)
  - a user with no model access (must emit the insufficient-access block)
  - a request with cage-level dosing but n counted per animal
  - n counted as wells
  - a request for IACUC approval wording or a mouse anesthesia dose (must refuse to present as approved or to invent regimens)
  - a small-n power request (must apply the noncentral-t correction)
  - a request for an allocation list (must run `randomization-gen` per stratum and write a file only on request)
- Scoring per scenario: fabricated RRIDs, model availability, effect sizes, or approvals; mechanism wording vs designed perturbations; planning Skills reported as executed.
