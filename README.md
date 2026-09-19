# Perils & Princesses: End Game

Foundry VTT module for the final campaign arc, using the perilsandprincesses system on Foundry v13+. Current release: **0.6.0**.

Install/update manifest:

```
https://synth-rabbit.github.io/perils-and-princesses-end-game/module.json
```

## Contents

- 42 actors: mine/pond, Scorchwoods knight parties and cast, existing castle roster.
- 44 draggable items: campaign rewards, story tools, hoard and faire items.
- 16 gridless scene sources, including new stump entrance and conclusion backdrops; no new walls.
- 48 private GM journals, including 20 standalone scene scripts: session 10, complete adventure runbook, hunt tracker, reference material and optional faire.
- 9 individually releasable handouts, private by default.

Open **End Game GM Guide → Session 10 Prep: The Last Clear Water** to begin. The adventure runbook covers all ten locations, both key routes and possible endings. See [CHANGELOG.md](CHANGELOG.md) for corrections and remaining live setup.

Your existing Dragon’s Cave, Boneyard, Knight Camp and Gnome Village maps remain the preferred play surfaces. Pristine Pond already exists outside this module; it does not need to be recreated.

All packs are GM-only by default because story items, actors and maps contain spoilers. Grant players only the individual imported documents they should know. Existing imported world documents and PC sheets are not automatically updated by installing this module. Stable compendium IDs preserve references, but do not promise automatic in-place world replacement.

## Sources and build

`build/module.json` is the manifest source. `tools/generate_src.py` owns actor/item/scene definitions. `content/gm/` and `content/handouts/` are portable Markdown release snapshots; `tools/generate_journals.py` renders them into linked Foundry journals. Unbundled vault references become readable labels rather than broken links. The runbook is the canonical adventure guide; vault histories and private character sheets are not shipped.

Install Python dependencies from `requirements.txt`; Node/npm and macOS `sips` are also used by the existing pipeline. The pack compiler is pinned to @foundryvtt/foundryvtt-cli 3.0.4.

1. Edit generator definitions or Markdown sources; put art under `build/art/`.
2. Bump version and download URL in `build/module.json`.
3. Run `sh build/release.sh`. It regenerates tokens and sources, validates them, packs the databases and creates the versioned zip plus root manifest.
4. Review changes, commit, and push to main. GitHub Pages serves the root manifest. Starting at 0.6.0, upload the versioned zip as a GitHub Release asset using the download URL in the manifest; larger archives exceed GitHub’s repository file limit. Older hosted archives remain available.
5. Verify the hosted manifest/archive, then check actual imports in Foundry separately.

Do not delete older release archives as incidental cleanup. Source JSON is generated and committed; update its source rather than editing generated files alone.
