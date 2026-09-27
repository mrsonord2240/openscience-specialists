# Not viable — Systematic Review and Meta-analysis Specialist (2026-09-10)

Not built. No package exists under `F:\OpenScience\specialists\systematic-review-meta-analysis-specialist`.
`spec.json` (15 Skills) and `system_prompt.md` (22,000 chars) are kept as a ready draft.

## Failing gates

**Gate 3 (core Skills Production Ready). This is the reason the Specialist is not viable.** Under the gate 2 score rule,
Skills in the `scientific` collection are scored by their `POLISH_CHANGELOG.md`, not by the templated
eval report. Every core Skill for framing and for the central operation falls below 85:

| Core Skill | Stage | Changelog | Templated report |
| --- | --- | --- | --- |
| `systematic-review` | framing (planning only) | 76 | 86 |
| `meta-protocol-writer` | framing | 76 | 90 |
| `prospero-registration-helper` | framing | 76 | 90 |
| `systematic-review-screener` | central: screening | 76 | 90 |
| `rct-bias-assessment-rob2` | central: risk of bias | 78 | 91 |
| `diagnostic-study-quality-assessment-quadas-2` | central: risk of bias | 78 | 91 |
| `meta-analysis` | central: pooling | 78 | 86 |

Only medical-collection Skills clear 85:

- `reporting-guideline-compliance-checker` (91). I flipped it to core as the reporting gate.
- `biomedical-search-strategy-builder` (85, supporting).

Neither covers framing or the central operation. **Gate 4** therefore fails too.

**Gate 8 (shipped means present).** Three Skills were dropped because their primary scripts or criteria were never shipped upstream:

- `meta-screening-fulltext`: `references/screening_prompts.md`, `scripts/extract_pdf.py`, `scripts/query_pubmed.py`
- `cohort-study-quality-assessment-nos`: `references/nos_criteria.md`, `scripts/calculate_nos_score.py`, `scripts/extract_pdf.py`
- `case-control-study-quality-assessment-nos`: `references/nos_criteria_prompts.md`, `scripts/extract_pdf.py`, `scripts/format_nos_table.py`

**Gate 2 residual.** `biomedical-search-strategy-builder`'s eval report still lists a P0 ("square bracket balance not
checked"). The code at `f5ef65b9` already has the fix: the report's own `meta.description` says so, and
`scripts/main.py validate` rejects an unclosed `[MeSH Terms` tag. `build_specialist.py` checks `a["p0"]`
before its gate 9 published-bytes branch, so this Skill would still fail the build.

## What would make it viable

1. **Genuine re-audits of the seven core Skills**, with real dynamic inputs and at least 85 each. Fix these defects first, all confirmed in the shipped files:
   - `systematic-review-screener`:
     - The default `--format csv` writer crashes with `ValueError: dict contains fields not in fieldnames: 'abstract'`.
     - Substring exclusions ("adults and children", "unlike previous case reports") are applied at confidence 1.0 with no review flag.
     - Records without an abstract are excluded by the language heuristic.
     - `prisma_data.json` sets `database_results` to the number of input rows and counts title/abstract passes as `qualitative_synthesis`.
   - `meta-analysis`:
     - `egger_test` returns the slope's p-value and SE from `linregress` as the intercept test. A runtime comparison shows they differ from the `intercept_stderr` test.
     - `begg_test` is not the Begg–Mazumdar statistic.
     - It only offers DerSimonian–Laird pooling with a Wald interval, and gives no prediction interval.
   - `rct-bias-assessment-rob2`:
     - `rob2_guidelines.md` has no D3–D5 algorithms.
     - The D2 Low rule accepts Y/PY on 2.3.
     - The overall rule has no route to High from multiple Some concerns.
     - It assesses per study, not per result.
   - `diagnostic-study-quality-assessment-quadas-2`:
     - It gives no domain risk-of-bias judgements or applicability concerns.
     - Comments are forced into Chinese.
     - `references/api_reference.md` is a placeholder.
   - `prospero-registration-helper`: its `{}` defaults read as declarative facts, and the timeline is hard-coded to today + 28 days.
   - `systematic-review`, `meta-protocol-writer`: re-audit with real PICOS inputs. Their pass must not depend on non-bundled integration Skills.
2. **Ship the missing files** for `meta-screening-fulltext` and the two NOS Skills, then audit them. Alternatively, supply audited replacements for full-text screening and non-randomized risk of bias (ROBINS-I/E or NOS).
3. **Clear the stale P0** on `biomedical-search-strategy-builder`, by re-auditing it or by having the builder honour the gate 9 published copy.
4. Rebuild with the kept draft, and remove the defect workarounds from the prompt once the upstream fixes land.
