# Perils & Princesses: End Game

Foundry VTT module for the final arc of the Perils & Princesses campaign: the last
corrupted footholds (session 9), *The Princess and the Dragon*, and the assault on
Queen Morwenna's castle. Built for the
[perilsandprincesses](https://github.com/helloshyann/perilsandprincesses) system,
Foundry v13+.

**Install in Foundry** → Add-on Modules → Install Module → manifest URL:

```
https://synth-rabbit.github.io/perils-and-princesses-end-game/module.json
```

## What's in it

| Pack | Contents |
|---|---|
| End Game Actors | 42 NPCs and monsters: the mine and pond encounters, the four knight parties and their retinues, the Scorchwoods cast, and the castle-assault roster (Morwenna, both phases, and seven new thorn/frost adversaries) |
| End Game Scenes | 11 gridless scenes: the Scorchwoods overworld, Brokenhill Mine battlemap, and nine location backdrops |

Actor `notes` carry the run-notes: attacks, special rules, roleplay hooks, and the
house riders (Sir Damon's construct rules, Crystal Wolf pack morale, the
Frost-Crowned finale's friendship mechanic).

## Repo layout

```
module.json + pnp-end-game-<v>.zip   hosted release (GitHub Pages serves these)
build/module.json                    the manifest source of truth
build/src/{actors,scenes}/*.json     pack document sources (committed)
build/art/                           portraits, scene art, maps shipped in the zip
tools/generate_src.py                regenerates build/src from its data tables
ART_PROMPTS.md                       prompts for art that doesn't exist yet
MAPS_NEEDED.md                       battlemaps still to find/make (GM-sourced)
```

## Releasing a new version

1. Edit content in `tools/generate_src.py` (actors/scenes) or drop art into `build/art/`.
2. Bump `version` **and** the `download` URL in `build/module.json`.
3. Run:

```
sh build/release.sh
```

4. Commit and push. GitHub Pages (main branch, root) serves the new
   `module.json` and zip; Foundry sees the update at the same manifest URL.

Actor ids are deterministic (hashed from the name), so re-imports update in
place instead of duplicating.
