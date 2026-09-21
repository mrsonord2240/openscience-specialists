# authoring/

Material for turning audited Skills into Specialists. It came from the Skill-refinement factory,
[mrsonord2240/optimizing-agent-science-skills](https://github.com/mrsonord2240/optimizing-agent-science-skills),
which audits, fixes and promotes Skills and no longer carries any Specialist work. The Specialist
workflow is parked, not retired. Nothing here is a Specialist release and nothing in `specialists/`
reads it. Moved 2026-09-21; the factory's git history holds everything as it was.

| Path | What |
| --- | --- |
| `CANDIDATES.md` | the candidate Specialists, their scope and boundaries, and the bioSkills folders each draws from |
| `AUTHOR_BRIEF.md` | the author agent's brief: system prompt, metadata, building the package |
| `THRESHOLD.md` | Specialist gates 1 and 4-9, plus the AIPOCH score history behind gate 2. Gates 2 and 3 stay in the factory |
| `audits/<id>/` | each candidate's `AUDIT.md` and viability `verdict.json`; `audits/INDEX.md` is generated |
| `crossref/` | what duplicates what across Skill corpora, which of two overlapping Skills a Specialist should bundle, and the marketplace intake-readiness check |
| `publish_specialist_audit.py` | copies a candidate's `AUDIT.md` from the working area into `audits/` and regenerates `audits/INDEX.md` |

Skill bytes still come from the factory's `skills/bioSkills/` export. `crossref/scripts/` reads it there.
