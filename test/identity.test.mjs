import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { validateDocument } from "../scripts/lib/schema.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const identity = {
  id: "openscience-specialists",
  name: "OpenScience Specialists (Samuel Nord)",
};

const emptyMarketplace = (marketplace) => ({
  schema_version: 1,
  revision: "0",
  marketplace,
  specialists: [],
});

test("first-publish base carries this repository's identity", async () => {
  const base = JSON.parse(
    await readFile(
      path.join(root, "protocol/fixtures/valid/empty-marketplace.json"),
      "utf8",
    ),
  );
  assert.deepEqual(base.marketplace, identity);
  validateDocument("marketplace", base);
});

test("schema accepts identities the OpenScience App accepts", () => {
  validateDocument("marketplace", emptyMarketplace(identity));
  validateDocument(
    "marketplace",
    emptyMarketplace({
      id: "openscience",
      name: "OpenScience Specialist Marketplace",
    }),
  );
});

test("schema rejects identities the OpenScience App rejects", () => {
  for (const marketplace of [
    { id: "Open-Science", name: "x" },
    { id: "-leading", name: "x" },
    { id: "a".repeat(129), name: "x" },
    { id: "ok", name: "" },
    { id: "ok", name: "n".repeat(161) },
  ]) {
    assert.throws(() =>
      validateDocument("marketplace", emptyMarketplace(marketplace)),
    );
  }
});
