#!/bin/sh
# Zip the installable module: module.json plus the built packs and art.
# Run build_packs.sh first, or the zip will contain empty packs.
# The version is read from module.json so the zip name always matches.
set -e
cd "$(dirname "$0")"
test -d packs/pnp-endgame-actors || { echo "run build_packs.sh first"; exit 1; }
VERSION=$(python3 -c "import json;print(json.load(open('module.json'))['version'])")
ZIP="pnp-end-game-$VERSION.zip"
rm -f "$ZIP"
zip -r "$ZIP" module.json packs art \
  -x "*/LOCK" -x "*/LOG" -x "*/LOG.old" -x "*.DS_Store" >/dev/null
echo "wrote $ZIP"
