# Audits

Every audit behind this marketplace is published here — Skills that passed, Skills that failed,
earlier versions that were later fixed, and Specialist candidates that were not viable — so anyone
can see why a Skill was bundled or left out and pick up the work of improving it.

- [INDEX.md](INDEX.md) — every audited Skill with its latest score, grade, open recommendations and
  source, plus earlier audits and Specialist verdicts.
- [BACKLOG.md](BACKLOG.md) — every open recommendation from the latest audits, most severe first.

How scores and grades are computed is described in the repository
[README](../README.md#how-skills-are-validated).

## Sources and credits

- **Skills** belong to their authors. Every record names the Skill's author, source repository,
  exact commit and license. Current sources: [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills)
  (MIT) and [aipoch/medical-research-skills](https://github.com/aipoch/medical-research-skills) (MIT).
- **Modified Skills** come from [mrsonord2240/bioSkills](https://github.com/mrsonord2240/bioSkills),
  branch `openscience-fixes`, a fork of GPTomics/bioSkills. Each modified version's record says which
  upstream commit it is based on, and its `fixes.md` lists every change with how it was verified.
- **Audit method:** [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor)
  by AIPOCH (MIT).
- **Audits** are performed by Claude (Anthropic) agents following that method, commissioned and paid
  for by Samuel Nord. They are not reviewed or endorsed by the Skills' authors.
- Tools and their versions used during a run are named in that run's viewer.

## Layout

```
audits/
  INDEX.md, BACKLOG.md                  generated — do not edit
  skills/<skill-id>/<owner>-<repo>@<commit>/
    record.json                         provenance: source, author, license, method, supersedes
    report.json                         the skill-auditor report, unchanged
    viewer.md                           what was asked, the code, what ran, what it printed
    fixes.md                            modified versions only: the changes since the base commit
    scripts/                            the scripts the auditor wrote and ran
  specialists/<specialist-id>/
    AUDIT.md                            which Skills were chosen, why others were not, gate verdicts
    verdict.json                        viable / not viable and the failing gate
```

A Skill folder can hold several versions. The one no other version supersedes is the latest, and
only its recommendations appear in the backlog.

## Reading a record

- Start with `viewer.md`. Its commands and printed output are the strongest evidence; most
  sub-scores are an auditor's judgment, so a difference of a point or two is noise.
- Each input records whether its code actually executed. Tools without a Windows build were checked
  against their documented flags instead, and the viewer says so.
- Test data are synthetic and raw run outputs are not published. Local paths refer to the auditor's
  workstation.

## Contributing

1. Pick an item from [BACKLOG.md](BACKLOG.md) and read its viewer.
2. Fix the Skill in its source repository — upstream for its authors, or a pull request to
   [mrsonord2240/bioSkills](https://github.com/mrsonord2240/bioSkills) for Skills modified here.
3. Open an issue in this repository linking the change and asking for a re-audit. A re-audit adds a
   new version folder that supersedes the old one; nothing is overwritten.

After adding or changing records, run `npm run audits:index` and commit the regenerated files.
