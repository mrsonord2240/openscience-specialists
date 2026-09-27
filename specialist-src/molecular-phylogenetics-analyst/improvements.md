# Improvements — Molecular Phylogenetics Analyst (2026-09-15)

## Workflow gaps, and the Skill that would fill each

- **No orthology step.** Everything downstream assumes the input sequences are orthologs, and hidden
  paralogy is the single most common source of the discordance this Specialist then interprets as
  ILS. `comparative-genomics/ortholog-inference` (bioSkills, unaudited) is the missing first stage and
  is the highest-value addition.
- **No sequence retrieval or FASTA hygiene step.** `sequence-io/read-sequences` and
  `sequence-manipulation/*` (bioSkills, unaudited) would cover accession fetch, deduplication,
  strand/frame checks and the taxon-name sanitation that `bio-phylo-species-trees` needs and does not
  provide.
- **No alignment-quality measurement.** `bio-alignment-multiple` names GUIDANCE2/TCS and
  `bio-alignment-trimming` names TCS masking, but no bundled Skill computes column confidence.
  `alignment/msa-statistics` and `alignment/msa-parsing` (bioSkills, unaudited) would close this.
- **No selection or ancestral-state layer.** dN/dS (PAML/HyPhy) and ancestral reconstruction are the
  two most common questions asked immediately after a tree; both are currently `route_required`.
- **No reticulation layer.** The Specialist can detect quartet asymmetry but cannot fit a network
  (PhyloNet, HyDe, QuIBL). It stops at "model the reticulation elsewhere".
- **Phylodynamics is out of reach.** `epidemiological-genomics/phylodynamics` would pair with
  `bio-phylo-divergence-dating` for measurably-evolving populations.

## Bundled-Skill audit findings that matter here

- **P1, `bio-phylo-tree-visualization` (84).** The clade-colouring recipe calls `common_ancestor` on
  an unrooted IQ-TREE `.treefile` and coloured 14 of 16 tips for a 5-taxon clade. Routed around in
  the system prompt (root first, assert the MRCA tip set, clear raw support names), but a fix to the
  Skill is the real remedy. This Skill is also the only Limited Release in the bundle at 84.
- **P1, `bio-alignment-multiple` (85).** `-super5` with `-stratified`/`-diversified`/`-replicates` is
  rejected by MUSCLE 5.3; the ensemble options belong to `-align`. Routed around, but this Skill is a
  core Skill sitting exactly on the 85 bar, so any future re-audit could drop it below the floor.
- **`bio-phylo-species-trees` (86).** No leaf-name consistency check: a renamed sample became an extra
  species at exit 0. The prompt mandates a leaf-set diff; the Skill should do it.
- **`bio-phylo-divergence-dating` (87).** Root-to-tip regression and the date-randomization test are
  declared mandatory but no code ships, so the agent writes both every time. Ship them.
- **`bio-phylo-distance-calculations` (87).** Tells the agent to estimate the gamma shape and strip
  gap columns, supplies neither, and hard-codes `alpha 0.5` in its own block.
- **`bio-phylo-modern-tree-inference` (88).** Its flag warnings are wrong on IQ-TREE 2.4.0 (`--alrt`,
  `-bb`, `-nt` all accepted) and PMSF is recommended without a command. Both are prompt-level
  workarounds that would be better fixed upstream.
- **Untested on this machine:** IQ-TREE 3 and RAxML-NG were never run (IQ-TREE 2.4.0 was), and BEAST 2
  was not re-run. Any claim about their flags rests on documentation, not execution.

## System-prompt limits

- The routing section carries eleven defect workarounds. Each one is an instruction the agent must
  remember rather than a property of the Skill; as the Skills are fixed, these should be deleted, not
  accumulated.
- Compressing to the 22,000-character target cost the per-layout figure guidance (circular vs
  unrooted vs chronogram) and the explicit tip-count thresholds; the agent must read
  `bio-phylo-tree-visualization` for those.
- The prompt states the joint SH-aLRT/UFBoot rule and the gCF thresholds numerically. If a future
  Skill revision changes them, the prompt drifts silently.

## Connector gaps

- Declared: `pubmed`, `protein-annotation`, `genes`, `genomes`. The published vocabulary has no
  connector for a sequence archive (ENA/SRA), for a curated ortholog set (OrthoDB, OMA), or for a
  taxonomy (NCBI Taxonomy) — the three retrieval needs a phylogenetics workflow actually has.
- `biorxiv` was left out deliberately: preprint retrieval adds little to a methods-driven workflow.

## The evaluation this Specialist still needs

- An end-to-end run on a real multi-locus dataset, from unaligned FASTA to a rooted, dated,
  concordance-annotated figure, scoring whether the routing order is followed and whether the
  tree-visualization P1 workaround actually fires.
- An adversarial run that asks for a "basal lineage" from an unrooted tree and one that asks for a
  transmission direction between two named individuals, to confirm the rooting and research-scope
  gates hold.
- A run on a rapid radiation with known ILS, to check the concatenation-versus-coalescent decision and
  whether gCF is reported unprompted.
- No evaluation yet covers the Specialist's own prompt; every score in the bundle is a per-Skill
  score.
