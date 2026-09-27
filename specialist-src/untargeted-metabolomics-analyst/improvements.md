# Improvements — Untargeted Metabolomics Analyst (2026-09-17)

## Blocking build issue (top priority, not fixable within this candidate's own folder)

- `python build_specialist.py untargeted-metabolomics-analyst` fails with: `bio-experimental-
  design-batch-design: also packaged by mass-spec-proteomics-analyst with different bytes;
  installing both raises a Skill conflict`. Root cause, confirmed by diff: `mass-spec-proteomics-
  analyst`'s already-built package
  (`F:\OpenScience\specialists\mass-spec-proteomics-analyst\versions\1.0.0\package\skills\
  bio-experimental-design-batch-design\`) ships the **pre-fix** SKILL.md (189 lines, score 82,
  from `spec.json` upstream commit `567cab000f3728427c4c8a18e36d2f794a9def7d`, which predates the
  batch-design fix-and-re-export). This candidate's `spec.json` (state already set up, not to be
  changed per the brief) correctly pins the newer commit `f5ad8c583206a9124732d9518ace53ab17a9be3b`
  where batch-design was already fixed (281 lines, score 87). The two byte sets genuinely differ —
  not a line-ending or whitespace artifact — so this is a real Skill conflict that will recur at
  publish time if both Specialists ship as-is.
- This is outside this candidate's own `specialist-src/untargeted-metabolomics-analyst/` folder to
  fix: resolving it means either (a) rebuilding `mass-spec-proteomics-analyst` against the current
  post-fix commit so both Specialists ship identical batch-design bytes, or (b) some other
  cross-candidate reconciliation decided by the session lead. Per the brief's "touch only your own
  `<id>` folders" rule, this candidate does not attempt either. **Reported here as instructed
  ("report builder bugs... instead of fixing them") — build_specialist.py's own-sibling-conflict
  check is doing exactly its job; the fix belongs to whichever round-2 batch coordinates commit
  pins across candidates that share a Skill.**
- Once resolved, re-run `python build_specialist.py untargeted-metabolomics-analyst`, then the two
  `npm run build:release` passes into `-a`/`-b` and compare SHA-256.

## Missing workflow steps / Skills that would fill them

- No isotope-tracing (SIRM/13C-MFA) Skill is bundled, by design (`CANDIDATES.md` scopes it as
  supporting-only and this candidate stays untargeted-discovery-only). If a user needs a flux claim
  rather than a pool-size claim, `bio-metabolomics-isotope-tracing` (present in the repo, not
  audited for this candidate) would fill that gap — audit it before adding.
- No SIRIUS/CSI:FingerID execution path was verified end to end in any audit (login-gated in every
  environment tested); `metabolite-annotation`'s SIRIUS section is documented but unexecuted. A
  future audit with a live SIRIUS academic account would close this.
- The orchestration Skill (`bio-workflows-metabolomics-pipeline`) has no glue code for entering at
  Stage 2 from an MS-DIAL export (P2, both pre- and post-fix). A short worked example bridging
  `msdial-preprocessing`'s parsed table into `normalization-qc`'s `filter_peaks_by_fraction()`
  would close this and is cheap to add.

## Open P1s that matter here (from the audits, routed around in the prompt but not fixed in-Skill)

- `pathway-mapping`: `SetKEGG.PathLib`/`CrossReferencing`/`Setup.KEGGReferenceMetabolome` silently
  download from `metaboanalyst.ca` even on the Local-Only ORA path's neighboring calls; only the
  `CalculateOraScore`/`CalculateQeaScore` -> `xialab.ca` POST is a P0-level disclosed leak. The
  system prompt discloses both, but the Skill text itself could be tightened to name
  `metaboanalyst.ca` alongside `xialab.ca` in its own disclosure block for parity.
- `msdial-preprocessing`: the malformed `Key=Value` silent-drop (exit 0, wrong feature count by an
  order of magnitude) is routed around in the prompt (assert feature count against expected order
  of magnitude) but is not fixed in the Skill itself — a parser that validates `Key: Value` syntax
  and errors loudly on `=` would remove the need for the workaround entirely.

## bioSkills or other listed-repo Skills that would add value once audited

- `bio-metabolomics-targeted-analysis` — would let this Specialist answer "is my targeted MRM panel
  in scope" without punting (currently `msdial-preprocessing`'s Input 6 correctly declines but has
  nowhere to route). Audit and add as supporting if scope allows.
- `bio-experimental-design-randomization-blocking` — currently redundant with `batch-design`'s more
  specific coverage per `SELECTION.md`, but would strengthen the framing/design leg if audited to a
  comparable score, giving this Specialist two design Skills the way some published Specialists
  have.

## System-prompt limits

- The prompt is single-organism/single-cohort framed; it does not address multi-cohort meta-analysis
  of metabolomics data (batch effects *between* studies, not just within one), which several users
  will eventually ask about. `multi-omics-integration/mofa-integration` is named as a related Skill
  but is not bundled here — correct per scope, but worth flagging if user demand appears.
- The prompt's MS-DIAL and xcms front-end sections assume the agent picks one; it does not give
  explicit guidance for reconciling a *replication* study that intentionally runs both front ends
  on the same raw files (a legitimate robustness check the Skills' own "Related Skills" sections
  gesture at but don't operationalize).

## Connector gaps

- `omics-archives` is declared but not `default_selected`; untargeted metabolomics repositories
  (MetaboLights, Metabolomics Workbench) are the natural target and neither is named explicitly in
  the connector vocabulary available to this candidate. If the Open Science App's connector list
  ever adds a metabolomics-specific archive ID, prefer it over the generic `omics-archives`.

## Evaluation this Specialist itself still needs

- No end-to-end run of all nine Skills chained together on one real dataset has been performed by
  any audit; each Skill was audited largely in isolation (the orchestration Skill's own audit
  chains real code across stages 1-4 and 4-5 but never a single raw-mzML-to-pathway-table run).
- No audit tested the lipidomics/metabolite-annotation boundary case (a feature that is ambiguous
  between "general metabolite" and "lipid" framing) — worth a dedicated input in a future audit
  round.
