#!/bin/sh
# Compile pack source JSON into the LevelDB packs Foundry v11+ needs.
# Run from this directory (or via release.sh). Requires node; uses npx so
# nothing is installed globally.
set -e
cd "$(dirname "$0")"
# Remove stale packs first so a renamed or dropped pack can't survive
# into the release zip.
rm -rf packs
for p in actors scenes; do
  [ -d "src/$p" ] || continue
  npx --yes @foundryvtt/foundryvtt-cli@latest package pack "pnp-endgame-$p" \
    --id pnp-end-game --type Module --in "src/$p" --out packs
done
