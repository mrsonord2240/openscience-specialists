# Brief: author one OpenScience Specialist

You are completing ONE candidate Specialist package for the OpenScience Specialist Marketplace
(Protocol v1). The skeleton, builder and threshold already exist. Your job is the part that needs
judgment: reading the bundled Skills, writing the system prompt and metadata, building, and saying
honestly how the result could be better.

## Where things are

- Threshold every Specialist must meet: `F:\openscience-specialists\specialist-src\THRESHOLD.md` (read first).
- Your spec skeleton: `F:\openscience-specialists\specialist-src\<id>\spec.json` — skill `id`, `source`
  (relative to `F:\OpenScience\skills`), `core` flag, and connectors are pre-filled. `_audit` and
  `_upstream_description` are hints the builder ignores.
- Bundled Skills live at `F:\OpenScience\skills\<source>\` (each has `SKILL.md`, usually
  `references/`, sometimes `scripts/`, and an `eval_report_*_result.json` skill-auditor report).
- Builder: `python F:\openscience-specialists\specialist-src\build_specialist.py <id>` → writes
  `F:\OpenScience\specialists\<id>\...`. It enforces the threshold and fails loudly.
- Marketplace clone with validator (Node 24, deps installed):
  `C:\Users\User\AppData\Local\Temp\claude\f--OpenScience\94d01cdf-e782-47f7-bd25-4e5ad49a6cf7\scratchpad\mp-main`
  - Protocol: `protocol/README.md`, authoring guide `specialists/README.md`.
  - Exemplar system prompts (read at least one fully before writing):
    `specialists/pharmacometrics-pkpd-designer/versions/1.0.0/package/specialist.json` (the
    structure you must follow) and `specialists/auto-research-specialist/versions/1.0.1/package/specialist.json`
    (biomedical routing style — useful for skill-routing discipline).

## Steps

1. **Read every bundled Skill's `SKILL.md`** plus the `recommendations` in its eval report. Note its
   trigger, required inputs, NOT-FOR boundary, and whether it EXECUTES (has runnable `scripts/`) or
   only PLANS/WRITES. If a Skill turns out not to fit this Specialist, or depends on a service the
   runtime will not have and is useless without it, remove it from `spec.json` and say why. You may
   not add a Skill unless it has an audit report meeting THRESHOLD.md (core ≥ 85, supporting ≥ 75,
   no veto, no P0). You may flip a `core` flag only with a stated reason.
2. **Fill `spec.json`**: `summary` (one sentence, ≤ 300 chars, in the style of the published
   summaries, e.g. "Designs unit-safe, uncertainty-aware ... without issuing patient-specific
   prescriptions."), and per Skill a Title Case `display_name` and a one-sentence `description`
   (≤ 170 chars) that is accurate to its SKILL.md. Keep `id`/`source` unchanged. Adjust connectors
   only within the published vocabulary: pubmed literature clinical-trials biorxiv genes genomes
   expression protein-annotation structures rna regulation biomart clinical-genomics
   human-genetics drug-regulatory cancer-models research-resources chembl chemistry molecule zinc
   omics-archives variants cellguide. Leave `required: false`.
3. **Write `F:\openscience-specialists\specialist-src\<id>\system_prompt.md`** using EXACTLY the section
   structure of the pharmacometrics exemplar:
   `# <Display Name>` / `## Identity` / `## Open Science runtime contract` / `## Packaged Skill routing`
   / `## Connector policy` / `## Domain operating principles` / `## Mindset And First Principles` /
   `## How You Frame A Problem` / `## How You Work` / `## Rigor And Critical Thinking` /
   `## Troubleshooting Playbook` / `## Definition Of Done` / `## Open Science domain gates` /
   `## Required delivery` / `## Final release check`.
   - Copy the **Open Science runtime contract** section verbatim from the exemplar.
   - **Skill routing**: every bundled Skill ID with a precise trigger, grouped by workflow stage,
     and explicitly label which Skills are planning/writing-only and can never be reported as
     having executed an analysis. Name the handoff order between Skills. Where two Skills overlap,
     say which one wins for which input. Keep the exemplar's closing paragraph about resolving
     supporting files relative to each Skill folder.
   - **Domain operating principles** through **Definition Of Done**: write as a senior practitioner
     of this field — specific methods, named failure modes, reflexive questions. No generic filler.
   - **Open Science domain gates**: the concrete, checkable ways work in THIS field goes wrong
     (e.g. leakage, immortal-time bias, instrument weakness). Each gate is a rule the agent can
     verify, not an aspiration. Research scope only: no diagnosis, prescription, or individual
     patient triage.
   - Time-sensitive facts (guideline versions, agency rules, database releases, impact factors):
     do not assert from memory unless certain; instruct verification via a Connector and recording
     of the version/access date.
   - Target 14,000–22,000 characters.
4. **Build**: run the builder until it passes. Then build the release twice with the marketplace
   tool and confirm identical artifact SHA-256:
   ```
   cd <clone> && npm run build:release --silent -- --specialist-id <id> --version 1.0.0 --version-directory F:/OpenScience/specialists/<id>/versions/1.0.0 --output ../build-<id>-a
   (repeat with ../build-<id>-b)
   ```
   Do NOT copy anything into the clone's `specialists/` directory and do not run `npm run validate`;
   central validation runs after all agents finish.
5. **Write `F:\openscience-specialists\specialist-src\<id>\improvements.md`**: prioritized, actionable bullets on
   how this Specialist could be improved — missing workflow steps and what Skill would fill each;
   bundled Skills whose audit P1s matter here; unaudited Skills already in `F:\OpenScience\skills`
   that would add value once audited (name them); system-prompt limits; connector gaps; the
   evaluation this Specialist itself still needs. Short bullets, no preamble. Start the file with a
   dated heading `# Improvements — <display name> (2026-09-10)`.
6. If, after reading the Skills, you conclude the candidate genuinely fails THRESHOLD.md (e.g. a
   core Skill is unusable), do not build. Instead write `not-viable.md` in the same folder stating
   which gate fails and exactly what is needed to make it viable.

## Rules

- Never edit anything under `F:\OpenScience\skills` or `build_specialist.py` (report builder bugs in
  your final message instead). Touch only your own `<id>` folders.
- On Windows: edit files with the Write/Edit tools or Python with `encoding='utf-8'`; never
  round-trip text through PowerShell `Get-Content`/`Out-File`. Prefix Python with
  `PYTHONIOENCODING=utf-8` in Bash.
- Do not invent facts about a Skill — cite what its SKILL.md says.

## Final message (≤ 200 words)

Built or not-viable; skill count (and any removed, with reason); both artifact SHA-256 values and
whether they match; prompt length; the top three improvements; any builder issue.
