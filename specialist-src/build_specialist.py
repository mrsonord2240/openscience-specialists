"""Assemble a Protocol v1 Specialist version from local AIPOCH skills.

Usage: python build_specialist.py <specialist-id> [<specialist-id> ...]

Reads   specialist-src/<id>/spec.json and specialist-src/<id>/system_prompt.md
Writes  specialists/<id>/README.md and specialists/<id>/versions/<ver>/...

Enforces the viability threshold (F:/optimizing-agent-science-skills/process/THRESHOLD.md) and fails
loudly instead of packaging a skill that does not meet it.
"""
import glob, hashlib, json, os, re, shutil, subprocess, sys

ROOT = r"F:\OpenScience"
SKILLS = os.path.join(ROOT, "skills")
SRC = r"F:\openscience-specialists\specialist-src"  # moved out of OpenScience 2026-09-27
OUT = r"F:\openscience-specialists\specialists"  # the repo; F:\OpenScience\specialists retired 2026-09-22
# Round-2 audits run for this release; preferred over any report shipped inside a Skill.
AUDITS = os.path.join(ROOT, "audits")

UPSTREAM_REPO = "https://github.com/aipoch/medical-research-skills"
UPSTREAM_COMMIT = "f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26"
UPSTREAM_PREFIX = {"medical": "awesome-med-research-skills", "scientific": "scientific-skills"}
UPSTREAM_TREE = os.path.join(SRC, "upstream-tree.txt")  # `git ls-tree -r <commit>` output
PUBLISHER = {"id": "mrsonord2240", "name": "Samuel Nord", "url": "https://github.com/mrsonord2240"}
APP_VERSION = "0.19.0"
PRETTIER = os.path.join(SRC, "tools", "node_modules", "prettier", "bin", "prettier.cjs")  # pinned 3.9.6, as upstream

# Connector IDs already present in published Protocol v1 releases. The App resolves
# references against its own reviewed configuration, so an unknown ID resolves to nothing.
KNOWN_CONNECTORS = set(
    "pubmed literature clinical-trials biorxiv genes genomes expression protein-annotation "
    "structures rna regulation biomart clinical-genomics human-genetics drug-regulatory "
    "cancer-models research-resources chembl chemistry molecule zinc omics-archives variants "
    "cellguide".split()
)
ID_RE = re.compile(r"^(?=.{1,128}$)[a-z0-9]+(?:-[a-z0-9]+)*$")
MIN_SCORE, CORE_MIN_SCORE = 75.0, 85.0
# Marketplace ZIP defaults (scripts/lib/zip.mjs); the App's own import limits are looser.
MAX_FILE_BYTES, MAX_FILES, MAX_EXPANDED_BYTES = 10 * 2**20, 1000, 100 * 2**20
MAX_SUMMARY_CHARS = 500  # marketplace.json schema: /specialists/*/summary maxLength
EXCLUDE_FILES = re.compile(r"^(eval_report_.*\.json|\.DS_Store|Thumbs\.db)$")
EXCLUDE_DIRS = {"__pycache__", ".git", ".pytest_cache", ".ipynb_checkpoints"}


def dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text if text.endswith("\n") else text + "\n")


PUBLISHED_DIR = os.path.join(SRC, "published-skills")
PUBLISHED = json.load(open(os.path.join(PUBLISHED_DIR, "index.json"), encoding="utf-8"))


def content_digest(files):
    """Protocol v1 Skill content digest over (relative path, bytes) pairs."""
    h = hashlib.sha256(b"OpenScience Skill content digest v1\0")
    for rel, data in sorted(files, key=lambda f: f[0].encode("utf-8")):
        p = rel.encode("utf-8")
        h.update(len(p).to_bytes(8, "big") + p + len(data).to_bytes(8, "big") + data)
    return h.hexdigest()


REF_RE = re.compile(r"(?<![\w/.-])((?:references|scripts|assets|templates)/[\w./-]*\w\.(?:md|py|R|r|sh|json|txt|csv|yaml|yml|rds|Rdata))\b")
IMPORT_RE = re.compile(r"\b(?:from|import)\s+scripts\.(\w+)")


def missing_references(skill_dir):
    text = open(os.path.join(skill_dir, "SKILL.md"), encoding="utf-8", errors="replace").read()
    refs = set(REF_RE.findall(text)) | {f"scripts/{m}.py" for m in IMPORT_RE.findall(text)}
    return [r for r in sorted(refs) if not os.path.isfile(os.path.join(skill_dir, *r.split("/")))]


RUNTIME_PY = os.path.join(ROOT, "runtime", "envs", ".p", "python.exe")
RUNTIME_RSCRIPT = os.path.join(ROOT, "runtime", "envs", ".r", "Scripts", "Rscript.exe")


def script_parse_failures(skill_dir):
    """Parse every bundled Python/R script with the Open Science runtime's own interpreters."""
    py, rs = [], []
    for base, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fn in files:
            p = os.path.join(base, fn)
            (py if fn.endswith(".py") else rs if fn.lower().endswith(".r") else []).append(p)
    bad = []
    if py:
        code = ("import sys\nfor p in sys.argv[1:]:\n    try:\n        compile(open(p,'rb').read(), p, 'exec')\n"
                "    except SyntaxError as e:\n        print(p + ': ' + str(e))\n")
        out = subprocess.run([RUNTIME_PY, "-c", code, *py], capture_output=True, text=True).stdout
        bad += [l for l in out.splitlines() if l]
    if rs:
        code = ("for (p in commandArgs(TRUE)) tryCatch(invisible(parse(file = p)), "
                "error = function(e) cat(p, ': ', conditionMessage(e), '\\n', sep = ''))")
        out = subprocess.run([RUNTIME_RSCRIPT, "-e", code, *rs], capture_output=True, text=True).stdout
        bad += [l for l in out.splitlines() if l.strip()]
    return [os.path.relpath(l.split(": ")[0], skill_dir).replace("\\", "/") + ": " + l.split(": ", 1)[-1][:80] for l in bad]


def git_blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def matches_blob(blob, data):
    """Gate 6: are these on-disk bytes the ones the commit records?

    Text files are compared after CRLF -> LF, because that is exactly what git stores for them
    (`* text=auto eol=lf`, core.autocrlf), and a Windows checkout can hold either. Binaries are
    compared raw. Content differences of any other kind still fail."""
    if not blob:
        return False
    return blob == git_blob_sha(data) or (
        b"\0" not in data[:8000] and blob == git_blob_sha(data.replace(b"\r\n", b"\n")))


def load_upstream():
    tree = {}
    with open(UPSTREAM_TREE, encoding="utf-8") as f:
        for line in f:
            meta, path = line.rstrip("\n").split("\t", 1)
            tree[path] = meta.split()[2]
    return tree


def audit(skill_dir, kid=None):
    own = os.path.join(AUDITS, kid) if kid else None
    is_own = bool(own and os.path.isdir(own)
                  and any(n.startswith("eval_report") and n.endswith(".json") for n in os.listdir(own)))
    if is_own:
        skill_dir = own
    reps = [n for n in os.listdir(skill_dir) if n.startswith("eval_report") and n.endswith(".json")]
    if not reps:
        return None
    r = json.load(open(os.path.join(skill_dir, reps[0]), encoding="utf-8"))
    f = r.get("final", {})
    raw = f.get("score", f.get("final_score"))
    if raw is None:
        return None  # schema-drifted report with no final score: treat as unaudited
    score = float(raw)
    # The upstream "polish" pass overwrote eval reports with a templated dynamic section
    # ("Test case N for <skill>", identical input totals across ~100 Skills) whose final score is
    # 10-15 points above the polished score the same pass recorded in POLISH_CHANGELOG.md.
    # Trust the changelog number when the report is templated.
    inputs = r.get("dynamic_score", {}).get("inputs", [])
    templated = any(str(i.get("label", "")).startswith("Test case ") for i in inputs)
    reported = score
    cl = os.path.join(skill_dir, "POLISH_CHANGELOG.md")
    if templated and os.path.isfile(cl):
        m = re.search(r"Polished Score\s*:\s*([\d.]+)", open(cl, encoding="utf-8", errors="replace").read())
        if m:
            score = min(score, float(m.group(1)))
    return {
        "score": score,
        "reported": reported,
        "templated": templated,
        "grade": f.get("grade"),
        "veto": bool(f.get("veto_override")) or any(
            str(g.get("gate", "")).upper() == "FAIL" for g in r.get("veto_gates", {}).values() if isinstance(g, dict)),
        "deployable": bool(f.get("deployable")),
        "p0": [x.get("title") for x in r.get("recommendations", []) if x.get("priority") == "P0"],
        "p1": [x.get("title") for x in r.get("recommendations", []) if x.get("priority") == "P1"],
        "evaluated_on": r.get("meta", {}).get("evaluated_on"),
        "own": is_own,
        "n_inputs": len(inputs),
        "executed": sum(1 for i in inputs if i.get("executed") is True),
    }


def frontmatter_value(text, key):
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return None
    mm = re.search(rf"^{key}:\s*(.*)$", m.group(1), re.M)
    return mm.group(1).strip().strip("'\"") if mm else None


TEXT_SKIP_EXT = {".csv", ".tsv", ".tab", ".vcf", ".bed", ".gff", ".gtf", ".fa", ".fasta", ".fna", ".faa",
                 ".fastq", ".fq", ".sam", ".mgf", ".mzml", ".mzxml", ".msp", ".sdf", ".mol", ".mol2", ".pdb",
                 ".cif", ".nwk", ".newick", ".nex", ".phy", ".aln", ".sto", ".tre"}


def normalize_text(rel, data):
    """Strip trailing whitespace and blank lines at end of file, which the repository's
    `git diff --check` rejects (the maintainers did the same for #1). Data files and binaries are
    shipped untouched."""
    if b"\0" in data[:8000]:
        return data
    # Git (core.autocrlf) stores every text file with LF endings, data files included.
    data = data.replace(b"\r\n", b"\n")
    if os.path.splitext(rel)[1].lower() in TEXT_SKIP_EXT:
        return data
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    stripped = "\n".join(re.sub(r"[ \t]+$", "", line) for line in text.split("\n"))
    if stripped == text and not text.endswith("\n\n"):
        return data
    return (stripped.rstrip("\n") + "\n").encode("utf-8")


def load_git_tree(path, commit, prefix=""):
    """Blob hashes at `commit`, after proving the checkout still agrees with it.

    Bytes are compared against the working tree, so the checkout must match the pinned commit —
    but only for the paths this release actually packages. The records repository takes commits
    to `fixes/` and `process/` while a build runs, and those must not block it: requiring
    HEAD == commit made a pin unusable the moment any unrelated commit landed.
    """
    scope = ["--", prefix] if prefix else []
    head = subprocess.run(["git", "-C", path, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    if head != commit:
        drift = subprocess.run(["git", "-C", path, "diff", "--name-only", commit, "HEAD", *scope],
                               capture_output=True, text=True, encoding="utf-8").stdout.strip()
        if drift:
            where = f"under {prefix}/" if prefix else "in the repository"
            raise SystemExit(f"{path} is at {head}, spec pins {commit}, and they differ {where}:\n"
                             + "\n".join("  " + f for f in drift.splitlines()[:20]))
    dirty = subprocess.run(["git", "-C", path, "status", "--porcelain", *scope],
                           capture_output=True, text=True, encoding="utf-8").stdout.strip()
    if dirty:
        raise SystemExit(f"{path} has uncommitted changes to the packaged files:\n"
                         + "\n".join("  " + f for f in dirty.splitlines()[:20]))
    out = subprocess.run(["git", "-C", path, "ls-tree", "-r", commit], capture_output=True, text=True,
                         encoding="utf-8").stdout
    tree = {}
    for line in out.splitlines():
        meta, rel = line.split("\t", 1)
        tree[rel] = meta.split()[2]
    return tree


def own_built_skills(sid):
    """Skill IDs packaged by the other Specialists built here, with their content digests."""
    found = {}
    for vroot in glob.glob(os.path.join(OUT, "*", "versions", "*", "package", "skills", "*")):
        other = os.path.relpath(vroot, OUT).split(os.sep)[0]
        if other == sid:
            continue
        files = []
        for base, _, fns in os.walk(vroot):
            for fn in fns:
                fp = os.path.join(base, fn)
                files.append((os.path.relpath(fp, vroot).replace("\\", "/"), open(fp, "rb").read()))
        found.setdefault(os.path.basename(vroot), (other, content_digest(files)))
    return found


def build(sid, upstream):
    sdir = os.path.join(SRC, sid)
    spec = json.load(open(os.path.join(sdir, "spec.json"), encoding="utf-8"))
    up = spec.get("upstream")
    if up:
        repo, commit, lic = up["repository"], up["commit"], up["license"]
        repo_root = up["path"]
        # Gate 6, round 2: the Skills a release ships are the fixed ones exported into
        # optimizing-agent-science-skills under `skills/bioSkills/`, so bytes are checked against
        # that repository's export commit rather than an upstream clone. `prefix` is the sub-path
        # inside the checkout; round-1 specs, which point straight at an upstream clone, omit it.
        prefix = up.get("prefix", "").strip("/")
        skills_root = os.path.join(repo_root, *prefix.split("/")) if prefix else repo_root
        upstream = load_git_tree(repo_root, commit, prefix)  # paths are relative to the repository root
        up_path = (lambda source: prefix + "/" + source) if prefix else (lambda source: source)
        # The upstream project's own licence sits with the Skills; fall back to the repository root.
        lic_file = next((os.path.join(d, n) for d in ([skills_root, repo_root] if prefix else [repo_root])
                         for n in ("LICENSE", "LICENSE.md", "LICENSE.txt")
                         if os.path.isfile(os.path.join(d, n))), None)
        license_text = open(lic_file, encoding="utf-8").read() if lic_file else ""
        # Say where the bundled licence came from: with a prefix it is the upstream project's own
        # LICENSE next to the Skills, not this repository's licence for its own tooling.
        lic_where = (prefix + "/ ") if prefix and lic_file and os.path.dirname(lic_file) == skills_root else "repository "
    else:
        repo, commit, lic = UPSTREAM_REPO, UPSTREAM_COMMIT, "MIT"
        skills_root, prefix, lic_where = SKILLS, "", "repository "
        up_path = lambda source: UPSTREAM_PREFIX[source.split("/")[0]] + "/" + "/".join(source.split("/")[1:])
        license_text = open(os.path.join(SRC, "UPSTREAM_LICENSE.txt"), encoding="utf-8").read()
    repo_name = "/".join(repo.rstrip("/").split("/")[-2:])
    at_commit = f"`{commit}`" + (f", under `{prefix}/`" if prefix else "")
    siblings = own_built_skills(sid)
    normalized_files = 0
    prompt = open(os.path.join(sdir, "system_prompt.md"), encoding="utf-8").read().replace("\r\n", "\n")
    version = spec.get("version", "1.0.0")
    assert spec["id"] == sid and ID_RE.match(sid), f"bad specialist id {sid}"
    problems, notes, rows = [], [], []
    total_files = total_bytes = 0

    vdir = os.path.join(OUT, sid, "versions", version)
    pkg = os.path.join(vdir, "package")
    if os.path.isdir(vdir):
        shutil.rmtree(vdir)

    for sk in spec["skills"]:
        src = os.path.join(skills_root, *sk["source"].split("/"))
        kid = sk["id"]
        if not ID_RE.match(kid):
            problems.append(f"{kid}: invalid skill id")
            continue
        if not os.path.isfile(os.path.join(src, "SKILL.md")):
            problems.append(f"{kid}: no SKILL.md at {sk['source']}")
            continue
        a = audit(src, sk["id"])
        core = sk.get("core", False)
        if a is None:
            problems.append(f"{kid}: no skill-auditor report (unaudited)")
        else:
            floor = CORE_MIN_SCORE if core else MIN_SCORE
            if a["veto"] or not a["deployable"]:
                problems.append(f"{kid}: audit veto / not deployable")
            if a["score"] < floor:
                problems.append(f"{kid}: audit {a['score']} < {floor} ({'core' if core else 'supporting'})")
            if a["p0"]:
                problems.append(f"{kid}: open P0 recommendation(s): {a['p0']}")
        for ref in re.findall(r"\b" + re.escape(kid) + r"\b", prompt)[:1] or [None]:
            if ref is None:
                problems.append(f"{kid}: not referenced in system_prompt.md routing")

        # An audit score says nothing about files that were never shipped: every bundled file the
        # SKILL.md points a reader or the runtime at must exist.
        accepted = sk.get("known_missing", {})
        missing = [m for m in missing_references(src) if m not in accepted]
        if missing:
            problems.append(f"{kid}: SKILL.md references {len(missing)} missing file(s): {missing[:4]}")
        unparsable = script_parse_failures(src)
        if unparsable:
            problems.append(f"{kid}: bundled script(s) fail to parse in the Open Science runtime: {unparsable[:3]}")
        for path, reason in accepted.items():
            notes.append(f"{kid}: upstream SKILL.md references `{path}`, which upstream never shipped — accepted: {reason}")

        dst = os.path.join(pkg, "skills", kid)
        pub = PUBLISHED.get(kid)
        if pub:
            # The App rejects installing a Skill whose ID is already installed with different
            # bytes ("Skill conflict"), so an ID that a published Specialist already ships must
            # ship the published bytes, and only when it is the same upstream Skill.
            if pub["source"] != f"{repo}@{commit}":
                problems.append(f"{kid}: ID already published from {pub['source']} as a different Skill; installing both raises a Skill conflict")
                continue
            files = []
            pdir = os.path.join(PUBLISHED_DIR, kid)
            for base, dirs, fns in os.walk(pdir):
                for fn in fns:
                    p = os.path.join(base, fn)
                    files.append((os.path.relpath(p, pdir).replace("\\", "/"), open(p, "rb").read()))
            if content_digest(files) != pub["content_digest"]:
                problems.append(f"{kid}: cached published bytes do not match the published content digest")
                continue
            for rel, data in files:
                out = os.path.join(dst, *rel.split("/"))
                os.makedirs(os.path.dirname(out), exist_ok=True)
                open(out, "wb").write(data)
            notes.append(f"{kid}: bytes reused from published {', '.join(pub['published_in'])} (content digest {pub['content_digest'][:12]}) so installing both Specialists does not raise a Skill conflict")
            total_files += len(files)
            total_bytes += sum(len(d) for _, d in files)
            rows.append((sk, a, len(files)))
            continue

        # copy + provenance check
        up_prefix = up_path(sk["source"])
        packaged = []
        excluded = sk.get("exclude", {})
        for path, reason in excluded.items():
            notes.append(f"{kid}: `{path}` omitted from the package — {reason}")
        mismatched, copied = [], 0
        for base, dirs, files in os.walk(src):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for fn in files:
                if EXCLUDE_FILES.match(fn):
                    continue
                p = os.path.join(base, fn)
                rel = os.path.relpath(p, src).replace("\\", "/")
                if rel in excluded:
                    continue
                data = open(p, "rb").read()
                if not matches_blob(upstream.get(up_prefix + "/" + rel), data):
                    mismatched.append(rel)
                if len(data) > MAX_FILE_BYTES:
                    problems.append(f"{kid}: {rel} is {len(data) // 2**20} MiB, over the marketplace {MAX_FILE_BYTES // 2**20} MiB per-file limit (exclude it with a reason if it is test data)")
                total_bytes += len(data)
                total_files += 1
                if rel == "SKILL.md":
                    name = frontmatter_value(data.decode("utf-8"), "name")
                    if name != kid:
                        problems.append(f"{kid}: SKILL.md frontmatter name is '{name}'; use that as the Skill id so the file ships unmodified")
                shipped = normalize_text(rel, data)
                normalized_files += shipped != data
                packaged.append((rel, shipped))
                out = os.path.join(dst, *rel.split("/"))
                os.makedirs(os.path.dirname(out), exist_ok=True)
                open(out, "wb").write(shipped)
                copied += 1
        if mismatched:
            problems.append(f"{kid}: {len(mismatched)} file(s) differ from upstream {commit[:8]}: {mismatched[:3]}")
        if kid in siblings and siblings[kid][1] != content_digest(packaged):
            problems.append(f"{kid}: also packaged by {siblings[kid][0]} with different bytes; installing both raises a Skill conflict")
        rows.append((sk, a, copied))

    if total_files > MAX_FILES or total_bytes > MAX_EXPANDED_BYTES:
        problems.append(f"package holds {total_files} files / {total_bytes // 2**20} MiB of skill content; marketplace limits are {MAX_FILES} files / {MAX_EXPANDED_BYTES // 2**20} MiB")

    # The marketplace's own schema caps these; catching it here beats a failed publish run.
    if len(spec["summary"]) > MAX_SUMMARY_CHARS:
        problems.append(f"summary is {len(spec['summary'])} chars; the marketplace schema allows {MAX_SUMMARY_CHARS}")

    for c in spec["connectors"]:
        if c["id"] not in KNOWN_CONNECTORS:
            problems.append(f"connector {c['id']}: not in published connector vocabulary")
        if c.get("required") and not c.get("default_selected"):
            problems.append(f"connector {c['id']}: required but not default-selected")

    if problems:
        shutil.rmtree(vdir, ignore_errors=True)  # never leave a partial package behind
        print(f"[{sid}] THRESHOLD/BUILD FAILURES:")
        for p in problems:
            print("   -", p)
        return False

    skill_ids = [sk["id"] for sk in spec["skills"]]
    connector_ids = [c["id"] for c in spec["connectors"] if c["default_selected"]]
    dump(os.path.join(pkg, "manifest.json"), {"schema_version": 1, "id": sid, "version": version, "exported_with_app_version": APP_VERSION})
    dump(os.path.join(pkg, "specialist.json"), {
        "name": sid,
        "display_name": spec["display_name"],
        "description": spec["summary"],
        "system_prompt": prompt,
        "skill_ids": skill_ids,
        "connector_ids": connector_ids,
    })
    dump(os.path.join(vdir, "release.config.json"), {
        "source": {"repository": repo, "commit": commit, "license": lic},
        "marketplace": {"display_name": spec["display_name"], "summary": spec["summary"], "publisher": PUBLISHER},
        "skills": [{"id": sk["id"], "name": sk["id"], "display_name": sk["display_name"], "description": sk["description"], "path": f"skills/{sk['id']}"} for sk in spec["skills"]],
        "connectors": [{"id": c["id"], "required": c["required"], "default_selected": c["default_selected"]} for c in spec["connectors"]],
    })

    if normalized_files:
        notes.append(f"{normalized_files} text file(s) normalized to repository format: LF line endings, no trailing whitespace, no blank lines at end of file")
    # Round-2 Skills are MODIFIED copies of a third-party upstream, so the package has to say so:
    # naming only the export repository would read as if its owner wrote them. `UPSTREAM.json` next
    # to the Skills records the route (original project -> fork -> this export).
    upstream_note = ""
    up_json = os.path.join(skills_root, "UPSTREAM.json")
    if prefix and os.path.isfile(up_json):
        u = json.load(open(up_json, encoding="utf-8"))
        orig, exp = u.get("upstream", {}), u.get("exported_from", {})
        if orig.get("repository"):
            upstream_note = (
                f"These Skills originate in {orig['repository']}"
                + (f" at commit {orig['commit']}" if orig.get("commit") else "")
                + (f" ({orig['license']})" if orig.get("license") else "") + ".\n"
            )
            if u.get("modified"):
                upstream_note += (
                    "They have been MODIFIED: defects found by audit were fixed"
                    + (f" in {exp['repository']}" if exp.get("repository") else "")
                    + (f" at commit {exp['commit']}" if exp.get("commit") else "")
                    + ", then exported to the repository named above. Files change only where an audit\n"
                      "demonstrated a defect; every change has a fix log and a post-fix audit report.\n"
                )
            upstream_note += "\n"

    authors = []
    for sk, a, _ in rows:
        t = open(os.path.join(pkg, "skills", sk["id"], "SKILL.md"), encoding="utf-8").read()
        authors.append(f"- {sk['id']}: author {frontmatter_value(t, 'skill-author') or frontmatter_value(t, 'author') or 'unstated'}, license {frontmatter_value(t, 'license') or f'unstated (repository {lic})'}")
    write_text(os.path.join(pkg, "THIRD_PARTY_NOTICES.txt"),
               f"Bundled Skills are taken from {repo} at commit {commit}"
               + (f", under {prefix}/" if prefix else "") + ".\n\n"
               + upstream_note
               + "\n".join(authors) + "\n\n"
               + f"{repo_name} {lic_where}license\n\n" + license_text)

    def score_cell(a):
        if a["own"]:
            return f"{a['score']:g} ({a['grade']}, {a['evaluated_on']}; code ran for {a['executed']}/{a['n_inputs']} test inputs)"
        if a["templated"] and a["score"] != a["reported"]:
            return f"{a['score']:g} (polish changelog; report claims {a['reported']:g} from a templated test section)"
        return f"{a['score']:g} ({a['grade']}, {a['evaluated_on']})"

    table = "\n".join(
        f"| `{sk['id']}` | {sk['display_name']} | {'core' if sk.get('core') else 'supporting'} | {score_cell(a)} |"
        for sk, a, _ in rows)
    conn = ", ".join(f"`{c['id']}`" + (" (required)" if c["required"] else "") for c in spec["connectors"])
    mods = "\n".join(f"- {n}" for n in notes) or "- None."
    if all(a["own"] for _, a, _ in rows):
        dates = sorted({a["evaluated_on"] for _, a, _ in rows if a.get("evaluated_on")})
        when = (f"on {dates[0]}" if len(dates) == 1
                else f"between {dates[0]} and {dates[-1]}" if dates else "for this release")
        audit_note = (f"Scores come from skill-auditor runs made for this release {when}; the upstream\n"
                      "repository ships no audits. Where the generated code could not run here, the output was\n"
                      "graded by inspection; the table says how many test inputs actually ran.")
    else:
        audit_note = ("Scores come from the upstream skill-auditor report shipped with each Skill (`eval_report_*.json`),\n"
                      "except where that report's test section is templated; there the score recorded in the Skill's\n"
                      "`POLISH_CHANGELOG.md` is used and the reported figure is shown alongside.")
    write_text(os.path.join(OUT, sid, "README.md"), f"""# {spec['display_name']}

{spec['summary']}

## Versions

- `{version}` - initial release with {len(rows)} bundled Skills and {len(spec['connectors'])} Connector references.

The package uses the OpenScience App export/import v1 layout. Connector entries are references only;
credentials and executable Connector configuration are not included.

## Bundled Skills

{audit_note}

| Skill | Display name | Role | Audit score |
| ----- | ------------ | ---- | ----------- |
{table}

## Connector references

{conn}

## Source

Skills from [{repo}]({repo}) at {at_commit} ({lic}).

{upstream_note}Packaging notes (Skill files are otherwise byte-identical to that commit; audit reports are not
packaged):

{mods}
""")
    # The marketplace CI runs `prettier --check` on descriptors (not on Skill payloads).
    generated = [os.path.join(OUT, sid, "README.md"), os.path.join(vdir, "release.config.json"),
                 os.path.join(pkg, "manifest.json"), os.path.join(pkg, "specialist.json")]
    fmt = subprocess.run(["node", PRETTIER, "--write", "--log-level", "warn", *generated], capture_output=True, text=True)
    if fmt.returncode:
        print(f"[{sid}] prettier failed: {fmt.stderr.strip()}")
        return False
    print(f"[{sid}] built {version}: {len(rows)} skills, {len(connector_ids)} connectors, prompt {len(prompt)} chars" + (f", {len(notes)} packaging note(s)" if notes else ""))
    return True


if __name__ == "__main__":
    upstream = load_upstream()
    ok = all([build(s, upstream) for s in sys.argv[1:]])
    sys.exit(0 if ok else 1)
