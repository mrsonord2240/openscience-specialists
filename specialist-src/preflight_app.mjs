// Preflight a Specialist ZIP against the Open Science App's own import rules
// (aipoch/open-science src/main/specialist/package/{zip-adapter,validator}.ts, src/shared/specialist.ts).
// Usage: node preflight_app.mjs <zip> [<zip> ...]
// Exit code 1 if any ZIP would be refused, or would silently drop a bundled Skill.
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
const require = createRequire(new URL("./tools/package.json", import.meta.url));
const { unzipSync } = require("fflate");
const yaml = require("js-yaml");

const SAFE_ID = /^[a-z0-9-]+$/;
const SAFE_SKILL_NAME = /^(?=.{1,64}$)[a-z0-9]+(?:-[a-z0-9]+)*$/;
const RESERVED = ["os-", "mcp-"];
const SEMVER = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/;
const LIMITS = { zip: 50 * 2 ** 20, expanded: 200 * 2 ** 20, files: 2000, perFile: 25 * 2 ** 20 };
const decoder = new TextDecoder("utf-8", { fatal: true });

function frontmatter(raw) {
  const m = /^---\n([\s\S]*?)\n---\n?/.exec(raw.replace(/\r\n?/g, "\n"));
  if (!m) return { fields: {}, error: "no frontmatter" };
  try {
    const v = yaml.load(m[1], { schema: yaml.FAILSAFE_SCHEMA });
    const fields = {};
    if (v && typeof v === "object" && !Array.isArray(v))
      for (const [k, val] of Object.entries(v)) if (typeof val === "string") fields[k.toLowerCase()] = val;
    return { fields };
  } catch (e) {
    return { fields: {}, error: `YAML: ${e.reason || e.message}` };
  }
}

let failed = false;
for (const zipPath of process.argv.slice(2)) {
  const errors = [], dropped = [];
  const bytes = readFileSync(zipPath);
  const entries = Object.entries(unzipSync(bytes)).filter(([p]) => !p.endsWith("/") && !p.startsWith("__MACOSX"));
  const expanded = entries.reduce((s, [, b]) => s + b.length, 0);
  if (bytes.length > LIMITS.zip) errors.push("ZIP over 50 MB");
  if (expanded > LIMITS.expanded) errors.push("expands over 200 MB");
  if (entries.length > LIMITS.files) errors.push("over 2000 files");
  for (const [p, b] of entries) if (b.length > LIMITS.perFile) errors.push(`${p} over 25 MB`);

  // Layout: manifest.json at the root, or inside exactly one wrapper directory.
  const root = entries.some(([p]) => p === "manifest.json");
  const wrappers = [...new Set(entries.filter(([p]) => p.split("/").length === 2 && p.endsWith("/manifest.json")).map(([p]) => p.split("/")[0]))];
  let files = null;
  if (root && wrappers.length === 0) files = entries;
  else if (!root && wrappers.length === 1 && entries.every(([p]) => p.startsWith(wrappers[0] + "/")))
    files = entries.map(([p, b]) => [p.slice(wrappers[0].length + 1), b]);
  if (!files) errors.push("Unrecognized ZIP layout: needs manifest.json at the root or in one wrapper folder");

  let summary = "";
  if (files) {
    const get = (n) => files.find(([p]) => p === n)?.[1];
    const manifest = get("manifest.json") && JSON.parse(decoder.decode(get("manifest.json")));
    const payload = get("specialist.json") && JSON.parse(decoder.decode(get("specialist.json")));
    if (!manifest) errors.push("manifest.json missing");
    if (!payload) errors.push("specialist.json missing");
    if (manifest) {
      const extra = Object.keys(manifest).filter((k) => !["schema_version", "id", "version", "exported_with_app_version"].includes(k));
      if (extra.length) errors.push(`manifest fields not allowed: ${extra}`);
      if (manifest.schema_version !== 1) errors.push("manifest schema_version must be 1");
      if (!SAFE_ID.test(manifest.id || "") || RESERVED.some((r) => manifest.id.startsWith(r))) errors.push("manifest id invalid");
      if (!SEMVER.test(manifest.version || "")) errors.push("manifest version not SemVer");
      if (!SEMVER.test(manifest.exported_with_app_version || "")) errors.push("exported_with_app_version not SemVer");
    }
    if (payload) {
      const extra = Object.keys(payload).filter((k) => !["name", "display_name", "description", "system_prompt", "skill_ids", "connector_ids"].includes(k));
      if (extra.length) errors.push(`specialist.json fields not allowed: ${extra}`);
      const name = (payload.name || "").trim();
      if (name.length < 2 || name.length > 80 || !/^[\p{L}0-9 _-]+$/u.test(name)) errors.push("name invalid");
      if (payload.display_name !== undefined && (!payload.display_name.trim() || payload.display_name.length > 80)) errors.push("display_name empty or over 80");
      if (!payload.description?.trim() || payload.description.length > 1000) errors.push("description empty or over 1000");
      if (!payload.system_prompt?.trim() || payload.system_prompt.length > 32768) errors.push("system_prompt empty or over 32768");
    }
    // Bundled Skills: any failure here is a warning in the App, and the Skill is silently skipped.
    const skillRoots = [...new Set(files.filter(([p]) => p.startsWith("skills/")).map(([p]) => p.split("/")[1]))].sort();
    for (const id of skillRoots) {
      if (!SAFE_SKILL_NAME.test(id) || RESERVED.some((r) => id.startsWith(r))) { dropped.push(`${id}: unsafe Skill name`); continue; }
      const doc = files.find(([p]) => p === `skills/${id}/SKILL.md`)?.[1];
      if (!doc) { dropped.push(`${id}: no SKILL.md`); continue; }
      let text;
      try { text = decoder.decode(doc); } catch { dropped.push(`${id}: SKILL.md not UTF-8`); continue; }
      const fm = frontmatter(text);
      if (fm.fields.name?.trim() !== id) { dropped.push(`${id}: frontmatter name ${fm.error ? "unreadable (" + fm.error + ")" : JSON.stringify(fm.fields.name)}`); continue; }
      if (fm.fields.version !== undefined && !SEMVER.test(fm.fields.version.trim())) { dropped.push(`${id}: frontmatter version ${JSON.stringify(fm.fields.version)} is not SemVer`); continue; }
    }
    const declared = payload?.skill_ids || [];
    for (const id of declared) if (!skillRoots.includes(id)) dropped.push(`${id}: declared in skill_ids but not bundled`);
    summary = `${manifest?.id}@${manifest?.version}, ${skillRoots.length - dropped.length}/${declared.length} Skills install`;
  }
  const ok = !errors.length && !dropped.length;
  if (!ok) failed = true;
  console.log(`${ok ? "INSTALLABLE" : errors.length ? "REFUSED   " : "DEGRADED  "}  ${zipPath.split(/[\\/]/).pop()}  ${summary}`);
  for (const e of errors) console.log(`    error: ${e}`);
  for (const d of dropped) console.log(`    skill skipped: ${d}`);
}
process.exit(failed ? 1 : 0);
