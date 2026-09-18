#!/bin/sh
# Full release: regenerate sources, build packs, zip, and stage the
# hosted files (module.json + zip) at the repo root for GitHub Pages.
# Bump "version" and the "download" URL in build/module.json first.
# Then: ./build/release.sh && git add -A && git commit && git push
set -e
cd "$(dirname "$0")/.."
python3 tools/make_tokens.py
python3 tools/generate_src.py
python3 tools/generate_journals.py
python3 tools/validate_release.py
sh build/build_packs.sh
sh build/make_zip.sh
VERSION=$(python3 -c "import json;print(json.load(open('build/module.json'))['version'])")
cp "build/module.json" module.json
cp "build/pnp-end-game-$VERSION.zip" .
echo "staged module.json and pnp-end-game-$VERSION.zip at repo root"
echo "Foundry manifest URL: https://synth-rabbit.github.io/perils-and-princesses-end-game/module.json"
