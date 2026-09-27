#!/usr/bin/env bash
# Validate every built Specialist against a clean clone of aipoch/openscience-specialist-marketplace.
# Usage: MARKETPLACE=/path/to/clone bash validate_all.sh
# The clone must have run `npm ci`. Built Specialists are copied into its specialists/ directory.
set -euo pipefail
: "${MARKETPLACE:?set MARKETPLACE to a marketplace clone}"
OUT="F:/OpenScience/specialists"
cd "$MARKETPLACE"

for d in "$OUT"/*/; do
  id=$(basename "$d")
  rm -rf "specialists/$id"
  cp -r "$d" "specialists/$id"
done

npm run --silent format:check
npm test --silent 2>&1 | tail -3
npm run --silent validate

for d in "$OUT"/*/; do
  id=$(basename "$d")
  for run in a b; do
    npm run --silent build:release -- --specialist-id "$id" --version 1.0.0 \
      --output "../build-$id-$run" > "../build-$id-$run.log"
  done
  a=$(sha256sum "../build-$id-a/specialists/$id/1.0.0/$id-1.0.0.zip" | cut -d' ' -f1)
  b=$(sha256sum "../build-$id-b/specialists/$id/1.0.0/$id-1.0.0.zip" | cut -d' ' -f1)
  [ "$a" = "$b" ] && echo "reproducible  $id  $a" || { echo "NOT REPRODUCIBLE $id"; exit 1; }
  mkdir -p F:/OpenScience/dist
  cp "../build-$id-a/specialists/$id/1.0.0/$id-1.0.0.zip" F:/OpenScience/dist/
done

# The installable ZIPs, checked against the Open Science App's own import rules.
node F:/openscience-specialists/specialist-src/preflight_app.mjs F:/OpenScience/dist/*.zip
