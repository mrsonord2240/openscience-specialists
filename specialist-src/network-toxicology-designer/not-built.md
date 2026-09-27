# Not built — Network Toxicology and Pharmacology Design Specialist (2026-09-10)

The authoring run was stopped by the model's biology safety filter before it wrote anything. It was
not retried by rephrasing. `spec.json` is still the untouched skeleton.

On paper the Skills clear the score gates. Four reference-grounded planners score 89 (medical,
real audits), `ppi-network-analysis` 90, and `gokegg-analysis` 86. Two things still need work
before this is worth building:

- Change the `gokegg` id in `spec.json` to `gokegg-analysis`. The builder requires the SKILL.md name.
- Audit `diffdock-molecular-docking`, `string-database` and `ctd-api`. Both toxicology planners
  carry the same open P1 (no docking evidence threshold), so the prompt needs a hard gate that a
  docking score is never binding evidence.
