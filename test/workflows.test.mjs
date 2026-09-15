import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { parse as parseYaml } from "yaml";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

test("GitHub workflows are valid YAML documents", async () => {
  const workflows = {};
  for (const name of [
    "validate.yml",
    "publish.yml",
    "verify-published.yml",
    "release.yml",
  ]) {
    const source = await readFile(
      path.join(root, ".github/workflows", name),
      "utf8",
    );
    const workflow = parseYaml(source);
    assert.equal(typeof workflow.name, "string");
    assert.equal(typeof workflow.jobs, "object");
    workflows[name] = workflow;
  }
  assert.deepEqual(workflows["validate.yml"].permissions, { contents: "read" });
  assert.deepEqual(workflows["publish.yml"].permissions, {
    contents: "read",
  });
  assert.deepEqual(workflows["publish.yml"].jobs.publish.permissions, {
    contents: "write",
  });
  assert.deepEqual(workflows["verify-published.yml"].permissions, {
    contents: "read",
  });
  assert.deepEqual(workflows["release.yml"].permissions, {
    contents: "read",
  });
  assert.deepEqual(workflows["release.yml"].jobs.release.permissions, {
    contents: "write",
  });
  assert.equal(
    workflows["release.yml"].jobs.release.environment,
    "project-release",
  );
  assert.equal(workflows["publish.yml"].jobs.publish["timeout-minutes"], 45);
  assert.deepEqual(
    Object.keys(workflows["publish.yml"].on.workflow_dispatch.inputs),
    ["specialist_id", "specialist_ids"],
  );
  assert.equal(
    workflows["publish.yml"].on.workflow_dispatch.inputs.specialist_id.required,
    false,
  );
  assert.equal(
    workflows["publish.yml"].on.workflow_dispatch.inputs.specialist_ids
      .required,
    false,
  );
  assert.equal(workflows["publish.yml"].jobs.publish.environment, "production");
  assert.deepEqual(workflows["publish.yml"].concurrency, {
    group: "openscience-specialists-publication",
    "cancel-in-progress": false,
  });
  assert.equal(
    workflows["verify-published.yml"].jobs.verify["timeout-minutes"],
    20,
  );
  assert.equal(workflows["release.yml"].jobs.release["timeout-minutes"], 10);
  assert.equal(
    workflows["verify-published.yml"].jobs.verify.environment,
    undefined,
  );
  for (const name of [
    "GH_TOKEN",
    "MARKETPLACE_SIGNING_PRIVATE_KEY_PKCS8_BASE64",
  ]) {
    assert.equal(workflows["publish.yml"].jobs.publish.env[name], undefined);
  }
  const everyWorkflow = JSON.stringify(workflows);
  assert.doesNotMatch(
    everyWorkflow,
    /AWS_|aws |s3:\/\/|s3api|cloudfront|MARKETPLACE_CDN|MARKETPLACE_BUCKET/i,
  );
  assert.equal(
    workflows["publish.yml"].jobs.publish.env.MARKETPLACE_AUTHOR_POLICY,
    "${{ vars.MARKETPLACE_AUTHOR_POLICY || 'omit' }}",
  );
  assert.equal(
    workflows["publish.yml"].jobs.publish.env
      .MARKETPLACE_MIN_OPEN_SCIENCE_VERSION,
    "${{ vars.MARKETPLACE_MIN_OPEN_SCIENCE_VERSION }}",
  );

  for (const workflow of Object.values(workflows)) {
    for (const job of Object.values(workflow.jobs)) {
      for (const step of job.steps) {
        if (step.uses) {
          assert.match(step.uses, /@[0-9a-f]{40}$/);
        }
      }
    }
  }

  const validateCommands = workflows["validate.yml"].jobs.validate.steps
    .map((step) => step.run || "")
    .join("\n");
  assert.match(validateCommands, /check:immutability/);
  assert.equal(
    workflows["validate.yml"].jobs.validate.steps.some((step) =>
      step.uses?.startsWith("raven-actions/actionlint@"),
    ),
    true,
  );

  const publishSteps = workflows["publish.yml"].jobs.publish.steps;
  const resolvePlan = publishSteps.find(
    (step) => step.name === "Resolve Specialist publication plan",
  );
  assert.match(resolvePlan.run, /resolve-publication-plan\.mjs/);
  assert.match(resolvePlan.run, /--specialist-ids/);
  const parallelBuild = publishSteps.find(
    (step) => step.name === "Build deterministic releases in parallel",
  );
  assert.match(parallelBuild.run, /--output "\$output" &/);
  assert.match(parallelBuild.run, /wait "\$\{pids\[\$index\]\}"/);
  assert.doesNotMatch(
    JSON.stringify(workflows["publish.yml"]),
    /inputs\.version|source_commit_or_tag/,
  );
  const proof = publishSteps.find(
    (step) => step.name === "Prove GitHub byte equality",
  );
  assert.match(proof.run, /raw\.githubusercontent\.com/);
  assert.match(proof.run, /gh release download/);
  const verifySteps = workflows["verify-published.yml"].jobs.verify.steps;
  assert.equal(
    verifySteps.some((step) => /CDN/i.test(step.name || "")),
    false,
  );
  const publishCommands = workflows["publish.yml"].jobs.publish.steps
    .map((step) => step.run || "")
    .join("\n");
  assert.match(publishCommands, /Publication must be dispatched from main/);
  assert.match(publishCommands, /list-release-artifacts\.mjs/);
  assert.match(publishCommands, /--marketplace dist\/base-marketplace\.json/);
  assert.match(publishCommands, /release-exists/);
  assert.match(publishCommands, /Existing GitHub Release must be public/);
  assert.match(publishCommands, /--retry-all-errors/);
  assert.match(publishCommands, /PUBLISHED_COMMIT=/);
  assert.match(
    publishCommands,
    /MARKETPLACE_AUTHOR_POLICY must be omit or include/,
  );
  assert.match(
    publishCommands,
    /Author publication requires a valid minimum Open Science SemVer/,
  );
  assert.match(
    publishCommands,
    /--author-policy "\$MARKETPLACE_AUTHOR_POLICY"/,
  );
  assert.match(
    publishCommands,
    /raw="https:\/\/raw\.githubusercontent\.com\/\$\{GITHUB_REPOSITORY\}\/\$\{PUBLISHED_COMMIT\}\/"/,
  );
  assert.doesNotMatch(publishCommands, /git fetch[^\n]+\|\| true/);

  const prepareCommands = workflows["publish.yml"].jobs.publish.steps.find(
    (step) => step.name === "Prepare candidate Marketplace",
  ).run;
  assert.match(
    prepareCommands,
    /gh release download "\$tag"[\s\S]{0,240}--skip-existing/,
  );

  const verificationCommands = workflows[
    "verify-published.yml"
  ].jobs.verify.steps
    .map((step) => step.run || "")
    .join("\n");
  assert.match(verificationCommands, /--history true/);
  assert.match(verificationCommands, /verify:history/);

  const releaseCommands = workflows["release.yml"].jobs.release.steps
    .map((step) => step.run || "")
    .join("\n");
  assert.match(releaseCommands, /Tag .* does not match project version/);
  assert.match(releaseCommands, /SEMVER_PATTERN/);
  assert.match(releaseCommands, /scripts\/lib\/common\.mjs/);
  assert.match(releaseCommands, /Project releases require an annotated tag/);
  assert.match(releaseCommands, /git merge-base --is-ancestor/);
  assert.match(releaseCommands, /gh release create/);
  assert.match(releaseCommands, /--verify-tag/);
  assert.match(releaseCommands, /--generate-notes/);
  assert.match(releaseCommands, /release_args\+=\(--prerelease\)/);
  assert.match(releaseCommands, /--title "OpenScience Specialists \$tag"/);
});
