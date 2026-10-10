---
type: location
campaign: Perils & Princesses
adventure: "The Evil Queen's Reckoning"
---

# Rosehold

**Queen Morwenna's castle**, high on the Fangtooth peaks of the White-Capped Mountains, behind a wall of ice grown through with black thorns. Before the curse it was the first headquarters of the Perils and Princesses Society. Nobody alive in the Society knows that.

> Run it from [[rosehold_runbook]] (pressure track, allies, session plan, the ending) with [[rosehold_tracker]] open. Assets and Foundry setup: [[rosehold_asset_list]].

Names the table has used for it: the Fairy Queen's stronghold, the ice wall to the north, the palace in the Fangtooth Mountains. They are all this place. The ice wall and the Barrier of Thorns are one thing: ice with thorns frozen through it.

## Levels

| Level | Note | Rooms | Floor plan |
|---|---|---|---|
| 0 | [[00_The_Thornwall]] | A1 Muster · A2 Causeway · A3 Barrier · A4 Gatehouse | `rosehold_0_thornwall` |
| 1 | [[01_The_Outer_Ward]] | B1 Court · B2 Kennels · B3 Stables · B4 Briar Court · B5 Barracks · B6 Armory · B7 Raven Tower | `rosehold_1_outer_ward` |
| 2 | [[02_The_Hall_of_the_Rose]] | C1 Oath Door · C2 Great Hall · C3 Banquet Hall · C4 Kitchens · C5 Portraits · C6 Servants' Stair · C7 Grand Stair | `rosehold_2_hall_of_the_rose` |
| −1 | [[03_The_Undercroft]] | D1 Cistern · D2 Cells · D3 Guardroom · D4 Crypt · D5 Relic Vault · D6 Frostbind Well | `rosehold_u_undercroft` |
| 3 | [[04_The_Galleries]] | E1 Mirrors · E2 Map Room · E3 Ulrik's Workshop · E4 Luminaries' Rooms · E5 Conservatory · E6 Solar · E7 Landing | `rosehold_3_galleries` |
| 4 | [[05_The_Frozen_Spire]] | F1 Stair of Vows · F2 Antechamber · F3 Throne Room · F4 Rose Window | `rosehold_4_frozen_spire` |

Floor plans are in `maps/morwennas_castle/`, each as a keyed GM copy and an unkeyed player copy. **The castle is meant to be run as a dungeon crawl: one big Foundry scene per level, linked by the stairs.** **Painted maps for all six levels were made on 2026-10-05**: 1536 px originals in `maps/morwennas_castle/painted_originals/` (with `manifest.json`), and 4× upscales in the module's `build/art/maps/`.

## How the levels connect

```text
            F3 Throne Room ── F4 Rose Window
                 │
            F2 Antechamber
                 │
            F1 Stair of Vows
                 │
 E5 ─ E6 Solar ──┘        E4 Luminaries' Rooms (warm)
  │    │                    │
 E2 ─ E1 Mirrors ───────────┘
  │    │
  └── E7 Landing ── E3 Ulrik
       │
 C6 ~ C7 Grand Stair        C4 Kitchens (warm)
  │    │                     │
 C5 ─ C2 Great Hall ─ C3 Banquet
  │    │
  │   C1 Oath Door
  │    │
  │   B1 Court ─ B2..B7        A4 Gatehouse ─ A3 Barrier ─ A2 Causeway ─ A1 Muster
  │
 D0 ─ D1 Cistern ─ D2 Cells ─ D5 Vault
            │        │          ┆ (secret)
            └────── D3 ─ D4 Crypt
                     │
                    D6 Frostbind Well
```

**Three ways in:** the gate (A2 → A3 → A4), under the wall with Bannik (to D1), or over it with Puca's catapult (to B7). **Shortcuts:** the secret passage C6 ~ C7; the secret door E5 ~ E6; the crypt's secret stair D4 ┆ D5; Nim's Poof!.

**Warm rooms:** the Kitchens (C4) and the Luminaries' Rooms (E4) are the only places a Rest is possible inside the walls.

## What is true here

- **The castle listens.** Noise, wasted time and escaped ravens raise **the Cold**.
- **Silver, fire and friendship work.** Almost everything here is thorn, ice or grief, and the party has spent ten sessions collecting exactly the right tools.
- **Morwenna founded the Society.** The banners, the round table, the pins and the oath are hers. The players do not know this going in; the castle tells them room by room.
- **She can be saved.** The four Echoes and her journal say how.
