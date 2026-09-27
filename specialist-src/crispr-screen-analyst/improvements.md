# Improvements — CRISPR Screen Analyst (2026-09-17)

- **Missing workflow step: sequencing-depth/library-QC gate before counting.** The bundled
  `bio-crispr-screens-screen-qc` covers post-count QC well, but nothing in this bundle catches a
  bad FASTQ (adapter contamination, wrong trim length) before `mageck count` runs. A lightweight
  `sequencing-qc`/`fastqc`-style Skill (not in this candidate's draw list) would close that gap.
- **`bio-crispr-screens-mageck-analysis`'s permutation-round instability (P1, this audit).** Routed
  around in the prompt, but the underlying fix belongs upstream: `mageck-analysis` and
  `bio-workflows-crispr-screen-pipeline` should cross-reference the caveat directly in both
  SKILL.md files rather than relying on this Specialist's prompt to carry it.
- **`bio-crispr-screens-base-editing-analysis`'s `find_be_spacers()` bare `KeyError` (P1).** A
  one-line fix (`if not candidates: return pd.DataFrame(columns=[...])`) would remove the need for
  the prompt-level workaround entirely. Worth a fix-and-reaudit pass in a future round.
- **`bio-crispr-screens-prime-editing-screens`'s undocumented `input/` directory (P1).** Same
  category: SKILL.md's own heredoc recipe should `mkdir input` before writing the batch CSV, or the
  worked example should pass `--input-dir .` explicitly. Currently the Specialist prompt carries the
  fix, which works but is fragile against SKILL.md updates.
- **`bio-crispr-screens-batch-correction`'s zero-variance guide-drop filter (P2-adjacent).** The
  ~294/71,090 guide drop on real TKOv3 data is expected NaN-guard behavior, not a defect, but no
  Skill or audit has verified this scales sanely on a smaller custom library (e.g. a 5,000-guide
  focused library) where the same absolute filter could drop a much larger fraction. Worth a
  targeted audit input.
- **Unaudited but relevant bioSkills not bundled:** `crispr-screens/combinatorial-screens` (Cas12a
  multiplex / paralog GI scoring) and `crispr-screens/perturb-seq-analysis` (single-cell CRISPR)
  were excluded per `SELECTION.md` for scope/audit reasons, but a future round-3 pass that audits
  them would let this Specialist cover combinatorial and single-cell screens without duplicating
  `single-cell-transcriptomics-analyst`'s scope. `experimental-design/power-analysis` and
  `randomization-blocking` remain unaudited; a pre-screen sample-size Skill would strengthen the
  design stage.
- **System-prompt limits.** The prompt is 22,504 characters, ~2% over the 14,000–22,000 target
  band. Every cut beyond this point started trading a named failure mode or a P1 route-around for
  character budget; a future pass could split "Rigor And Critical Thinking" and "Troubleshooting
  Playbook" more cleanly to remove the remaining ~500 characters of overlap between them.
- **Connector gaps.** No `research-resources` or `omics-archives` connector is declared; a user
  wanting to pull a public DepMap/Project Score reference panel for Chronos priors or JACKS
  `--reffile` transfer has no in-scope Connector to do so and must be told to fetch it externally.
- **Evaluation this Specialist still needs.** No end-to-end eval has run the full prompt against a
  real multi-stage scenario (e.g. a cancer-line drug-modifier screen requiring CN correction, batch
  correction, and cross-method consensus in one request) to confirm the routing logic holds up
  when three or four Skills chain together rather than being exercised one at a time, which is how
  the underlying Skill audits tested them.
